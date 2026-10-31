"""Sign in with Google and sync through Google Drive's hidden app-data folder.

Each user brings their own Google Cloud OAuth client (type "Desktop app") and enters its
Client ID and secret in the app. Sign-in happens in the user's web browser: the app opens
Google's sign-in page, and Google sends the browser back to a temporary address on this
computer (127.0.0.1) that only this app listens on.

The app can only see files it created itself (scope drive.appdata); it cannot read the
rest of the user's Drive. This module is network code only: it never touches the ticket
database.
"""

import base64
import hashlib
import http.server
import json
import os
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

from resources import app_data_dir

SCOPE = "https://www.googleapis.com/auth/drive.appdata"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
DRIVE_API = "https://www.googleapis.com/drive/v3"
UPLOAD_API = "https://www.googleapis.com/upload/drive/v3"
FILE_NAME = "ticket-manager-sync.json"
MAX_BYTES = 20_000_000


class GoogleError(RuntimeError):
    """An error reported by Google. `code` is Google's short error name."""
    def __init__(self, message, code=""):
        super().__init__(message)
        self.code = code


class SignInRequired(GoogleError):
    """The saved sign-in no longer works; the user must sign in again."""


class SignInCancelled(GoogleError):
    pass


# ---------------------------------------------------------------- stored credentials
def _path(name: str) -> str:
    return os.path.join(app_data_dir(), name)


def _write_private(path: str, obj: dict):
    # Only the current user may read these files (on Linux/macOS).
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f)


def get_client():
    """Returns (client_id, client_secret); empty strings if not set."""
    try:
        with open(_path("google_client.json"), encoding="utf-8") as f:
            d = json.load(f)
        return str(d.get("client_id", "")), str(d.get("client_secret", ""))
    except (OSError, ValueError):
        return "", ""


def is_configured() -> bool:
    cid, secret = get_client()
    return bool(cid and secret)


def set_client(client_id: str, client_secret: str):
    cid, secret = client_id.strip(), client_secret.strip()
    if ".apps.googleusercontent.com" not in cid:
        raise ValueError("That does not look like a Google Client ID. It should end with "
                         ".apps.googleusercontent.com")
    if len(secret) < 8 or " " in secret:
        raise ValueError("That does not look like a Google client secret.")
    if (cid, secret) != get_client():
        _remove(_path("google_token.json"))      # a different client means a new sign-in
    _write_private(_path("google_client.json"), {"client_id": cid, "client_secret": secret})


def is_signed_in() -> bool:
    return os.path.exists(_path("google_token.json"))


def _remove(path: str):
    try:
        os.remove(path)
    except OSError:
        pass


def _load_token() -> dict:
    with open(_path("google_token.json"), encoding="utf-8") as f:
        return json.load(f)


def _save_token(tok: dict):
    _write_private(_path("google_token.json"), tok)


# ---------------------------------------------------------------- HTTP helpers
_BAD_CLIENT = ("Google did not accept the Client ID or secret. Check that you created an OAuth "
               "client of type \"Desktop app\" and copied both values exactly.")


def _post_form(url: str, fields: dict) -> dict:
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode())
        except Exception:  # noqa: BLE001
            err = {}
        code = str(err.get("error", ""))
        if code == "invalid_grant":
            raise SignInRequired("Your Google sign-in expired. Please sign in again.", code) from None
        if code in ("invalid_client", "unauthorized_client"):
            raise GoogleError(_BAD_CLIENT, code) from None
        raise GoogleError(err.get("error_description") or code or f"Google returned error {e.code}",
                          code) from None


# ---------------------------------------------------------------- sign in (web browser)
class WebSignIn:
    """One browser sign-in. Create it, call open_browser(), then wait() (blocking)."""

    def __init__(self):
        if not is_configured():
            raise GoogleError("Enter your Google Client ID and secret first.")
        self._cid, self._secret = get_client()
        self._verifier = secrets.token_urlsafe(64)
        challenge = base64.urlsafe_b64encode(
            hashlib.sha256(self._verifier.encode()).digest()).rstrip(b"=").decode()
        self._state = secrets.token_urlsafe(16)
        self._result = {}
        result = self._result

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                if "code" in q or "error" in q:
                    result["q"] = q
                body = (b"<html><body style='font-family:sans-serif'><h2>Ticket Manager</h2>"
                        b"<p>You can close this tab and return to the app.</p></body></html>")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        # Only this computer can connect to this address.
        self._server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        self._server.timeout = 1
        self._redirect = f"http://127.0.0.1:{self._server.server_port}"
        self.url = AUTH_URL + "?" + urllib.parse.urlencode({
            "response_type": "code", "client_id": self._cid, "redirect_uri": self._redirect,
            "scope": SCOPE, "state": self._state, "code_challenge": challenge,
            "code_challenge_method": "S256", "access_type": "offline", "prompt": "consent"})

    def open_browser(self):
        if self.url.startswith("https://"):
            webbrowser.open(self.url)

    def close(self):
        try:
            self._server.server_close()
        except OSError:
            pass

    def wait(self, cancelled=None, timeout: int = 300):
        """Waits until the user finishes in the browser, then saves the sign-in."""
        deadline = time.time() + timeout
        try:
            while "q" not in self._result and time.time() < deadline:
                if cancelled is not None and cancelled.is_set():
                    raise SignInCancelled("Sign-in cancelled.")
                self._server.handle_request()
        finally:
            self.close()
        q = self._result.get("q")
        if not q:
            raise GoogleError("Sign-in timed out. Please try again.")
        if q.get("state", [""])[0] != self._state:
            raise GoogleError("Sign-in failed (the response did not match the request).")
        if "error" in q or "code" not in q:
            raise GoogleError("Sign-in was cancelled or not allowed.")
        tok = _post_form(TOKEN_URL, {
            "code": q["code"][0], "client_id": self._cid, "client_secret": self._secret,
            "redirect_uri": self._redirect, "grant_type": "authorization_code",
            "code_verifier": self._verifier})
        if "refresh_token" not in tok:
            raise GoogleError("Google did not return a sign-in token. Remove the app's access in "
                              "your Google account settings and try again.")
        _save_token({"refresh_token": tok["refresh_token"], "access_token": tok.get("access_token", ""),
                     "expires_at": time.time() + int(tok.get("expires_in", 3600))})


def sign_out():
    if is_signed_in():
        try:
            _post_form(REVOKE_URL, {"token": _load_token().get("refresh_token", "")})
        except Exception:  # noqa: BLE001 - best effort
            pass
        _remove(_path("google_token.json"))


def _access_token() -> str:
    if not is_signed_in():
        raise SignInRequired("Please sign in with Google first.")
    tok = _load_token()
    if tok.get("access_token") and tok.get("expires_at", 0) - 60 > time.time():
        return tok["access_token"]
    cid, secret = get_client()
    try:
        new = _post_form(TOKEN_URL, {"client_id": cid, "client_secret": secret,
                                     "refresh_token": tok["refresh_token"],
                                     "grant_type": "refresh_token"})
    except SignInRequired:
        _remove(_path("google_token.json"))
        raise
    tok["access_token"] = new["access_token"]
    tok["expires_at"] = time.time() + int(new.get("expires_in", 3600))
    _save_token(tok)
    return tok["access_token"]


# ---------------------------------------------------------------- Drive (app-data folder)
def _call(method: str, url: str, data: bytes = None, ctype: str = None) -> bytes:
    headers = {"Authorization": "Bearer " + _access_token()}
    if ctype:
        headers["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as e:
        raise GoogleError(f"Google Drive error {e.code}. If this is 403, make sure the Google Drive "
                          f"API is enabled in your Google Cloud project.") from None


def _find_id():
    q = urllib.parse.urlencode({
        "spaces": "appDataFolder", "pageSize": 10, "fields": "files(id)",
        "q": f"name = '{FILE_NAME}' and trashed = false"})
    files = json.loads(_call("GET", f"{DRIVE_API}/files?{q}").decode()).get("files", [])
    return files[0]["id"] if files else None


def download():
    """Returns the sync document stored in Drive (a dict), or None if there is none yet."""
    file_id = _find_id()
    if not file_id:
        return None
    raw = _call("GET", f"{DRIVE_API}/files/{file_id}?alt=media")
    if len(raw) > MAX_BYTES:
        raise GoogleError("The sync data in Google Drive is too large.")
    return json.loads(raw.decode("utf-8")) if raw.strip() else None


def upload(doc: dict):
    data = json.dumps(doc, ensure_ascii=False).encode("utf-8")
    file_id = _find_id()
    if file_id:
        _call("PATCH", f"{UPLOAD_API}/files/{file_id}?uploadType=media", data, "application/json")
        return
    boundary = "tm" + secrets.token_hex(8)
    meta = json.dumps({"name": FILE_NAME, "parents": ["appDataFolder"]})
    body = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n"
            f"--{boundary}\r\nContent-Type: application/json\r\n\r\n").encode() \
        + data + f"\r\n--{boundary}--".encode()
    _call("POST", f"{UPLOAD_API}/files?uploadType=multipart", body,
          f"multipart/related; boundary={boundary}")
