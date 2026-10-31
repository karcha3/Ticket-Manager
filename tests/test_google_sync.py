"""Tests for Google sign-in and Drive sync, against a fake Google server on this computer."""
import http.server
import json
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest
import urllib.parse
import urllib.request
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database  # noqa: E402
import google_sync as gs  # noqa: E402

CID = "123-abc.apps.googleusercontent.com"
SECRET = "GOCSPX-testsecret123"
STATE = {}


class FakeGoogle(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, obj=None, raw=None):
        body = raw if raw is not None else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.path == "/token":
            f = urllib.parse.parse_qs(body.decode())
            if f["grant_type"][0] == "authorization_code":
                STATE["code_verifier"] = f["code_verifier"][0]
                if f["client_id"][0] != CID:
                    return self._send(401, {"error": "invalid_client"})
                return self._send(200, {"access_token": "AT1", "refresh_token": "RT1", "expires_in": 3600})
            if STATE.get("bad_refresh"):
                return self._send(400, {"error": "invalid_grant"})
            return self._send(200, {"access_token": "AT2", "expires_in": 3600})
        if self.path == "/revoke":
            return self._send(200, {})
        if self.path.startswith("/upload/files?uploadType=multipart"):
            assert b"appDataFolder" in body
            STATE["file"] = body.split(b"Content-Type: application/json\r\n\r\n")[-1].rsplit(b"\r\n--", 1)[0]
            return self._send(200, {"id": "F1"})
        self._send(404, {})

    def do_PATCH(self):
        STATE["file"] = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self._send(200, {})

    def do_GET(self):
        assert self.headers["Authorization"].startswith("Bearer ")
        if self.path.startswith("/drive/files?"):
            return self._send(200, {"files": [{"id": "F1"}] if STATE.get("file") else []})
        if self.path.startswith("/drive/files/F1?alt=media"):
            return self._send(200, raw=STATE["file"])
        self._send(404, {})


def ticket(first):
    return dict(first_name=first, last_name="X", venue_type="Concert", ticket_type="Standard",
                venue_name="V", location="", date="2026-01-01", time="19:00", seat="",
                price=5, status="Active", notes="")


class GoogleTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FakeGoogle)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        STATE.clear()
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        for name, value in (("app_data_dir", lambda: self.dir),
                            ("TOKEN_URL", self.base + "/token"), ("REVOKE_URL", self.base + "/revoke"),
                            ("DRIVE_API", self.base + "/drive"), ("UPLOAD_API", self.base + "/upload")):
            p = mock.patch.object(gs, name, value)
            p.start()
            self.addCleanup(p.stop)

    def browser(self, session, tail="?code=abc&state=STATE", delay=0.3):
        """Pretends to be the user's browser coming back from Google."""
        q = urllib.parse.parse_qs(urllib.parse.urlparse(session.url).query)
        redirect = q["redirect_uri"][0]
        self.assertTrue(redirect.startswith("http://127.0.0.1:"))
        url = redirect + "/" + tail.replace("STATE", q["state"][0])
        threading.Timer(delay, lambda: urllib.request.urlopen(url).read()).start()
        return q

    def sign_in(self):
        gs.set_client(CID, SECRET)
        s = gs.WebSignIn()
        self.browser(s)
        s.wait(timeout=10)


class CredentialTests(GoogleTestCase):
    def test_credentials_are_checked_and_trimmed(self):
        self.assertFalse(gs.is_configured())
        with self.assertRaises(ValueError):
            gs.set_client("nope", SECRET)
        with self.assertRaises(ValueError):
            gs.set_client(CID, "x")
        gs.set_client("  " + CID + " ", "  " + SECRET + "\n")
        self.assertEqual(gs.get_client(), (CID, SECRET))

    @unittest.skipIf(os.name == "nt", "file permissions work differently on Windows")
    def test_credential_file_is_private(self):
        gs.set_client(CID, SECRET)
        self.assertEqual(os.stat(os.path.join(self.dir, "google_client.json")).st_mode & 0o777, 0o600)

    def test_sign_in_needs_credentials(self):
        with self.assertRaises(gs.GoogleError):
            gs.WebSignIn()

    def test_changing_credentials_signs_out(self):
        self.sign_in()
        self.assertTrue(gs.is_signed_in())
        gs.set_client("999-zzz.apps.googleusercontent.com", SECRET)
        self.assertFalse(gs.is_signed_in())


class SignInTests(GoogleTestCase):
    def test_successful_sign_in(self):
        gs.set_client(CID, SECRET)
        s = gs.WebSignIn()
        q = self.browser(s)
        self.assertTrue(s.url.startswith("https://accounts.google.com/"))
        self.assertEqual((q["code_challenge_method"], q["scope"], q["access_type"]),
                         (["S256"], [gs.SCOPE], ["offline"]))
        s.wait(timeout=10)
        self.assertTrue(gs.is_signed_in())
        self.assertTrue(STATE["code_verifier"])

    def test_wrong_state_is_refused(self):
        gs.set_client(CID, SECRET)
        s = gs.WebSignIn()
        self.browser(s, "?code=abc&state=WRONG")
        with self.assertRaises(gs.GoogleError):
            s.wait(timeout=10)
        self.assertFalse(gs.is_signed_in())

    def test_denied_access(self):
        gs.set_client(CID, SECRET)
        s = gs.WebSignIn()
        self.browser(s, "?error=access_denied&state=STATE")
        with self.assertRaisesRegex(gs.GoogleError, "cancelled or not allowed"):
            s.wait(timeout=10)

    def test_cancel(self):
        gs.set_client(CID, SECRET)
        s = gs.WebSignIn()
        stop = threading.Event()
        threading.Timer(0.4, stop.set).start()
        with self.assertRaises(gs.SignInCancelled):
            s.wait(stop, timeout=10)

    def test_timeout(self):
        gs.set_client(CID, SECRET)
        with self.assertRaisesRegex(gs.GoogleError, "timed out"):
            gs.WebSignIn().wait(timeout=1)

    def test_a_stray_browser_request_does_not_end_the_wait(self):
        gs.set_client(CID, SECRET)
        s = gs.WebSignIn()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(s.url).query)
        red = q["redirect_uri"][0]
        threading.Timer(0.2, lambda: urllib.request.urlopen(red + "/favicon.ico").read()).start()
        threading.Timer(0.6, lambda: urllib.request.urlopen(red + "/?code=z&state=" + q["state"][0]).read()).start()
        s.wait(timeout=10)
        self.assertTrue(gs.is_signed_in())

    def test_wrong_client_id_gives_a_helpful_message(self):
        gs.set_client("999-zzz.apps.googleusercontent.com", SECRET)
        s = gs.WebSignIn()
        self.browser(s)
        with self.assertRaisesRegex(gs.GoogleError, "Desktop app"):
            s.wait(timeout=10)


class DriveTests(GoogleTestCase):
    def test_two_devices_sync_through_drive(self):
        self.sign_in()
        a = database.Database(os.path.join(self.dir, "a.db"))
        b = database.Database(os.path.join(self.dir, "b.db"))
        self.addCleanup(a.close)
        self.addCleanup(b.close)
        ann = a.add_ticket(ticket("Ann"))
        a.add_ticket(ticket("Bob"))
        self.assertIsNone(gs.download())                     # nothing stored yet
        _, doc = a.merge_doc(None)
        gs.upload(doc)                                       # creates the file
        _, doc = b.merge_doc(gs.download())
        gs.upload(doc)                                       # updates the file
        self.assertEqual(sorted(r["first_name"] for r in b.get_all_tickets()), ["Ann", "Bob"])
        time.sleep(0.01)
        a.delete_ticket(ann)
        _, doc = a.merge_doc(gs.download())
        gs.upload(doc)
        b.merge_doc(gs.download())
        self.assertEqual([r["first_name"] for r in b.get_all_tickets()], ["Bob"])

    def test_expired_access_token_is_refreshed(self):
        self.sign_in()
        tok = gs._load_token()
        tok["expires_at"] = 0
        gs._save_token(tok)
        gs.download()
        self.assertEqual(gs._load_token()["access_token"], "AT2")

    def test_expired_sign_in_asks_to_sign_in_again(self):
        self.sign_in()
        tok = gs._load_token()
        tok["expires_at"] = 0
        gs._save_token(tok)
        STATE["bad_refresh"] = True
        with self.assertRaises(gs.SignInRequired):
            gs.download()
        self.assertFalse(gs.is_signed_in())

    def test_sign_out_removes_the_token(self):
        self.sign_in()
        gs.sign_out()
        self.assertFalse(gs.is_signed_in())


if __name__ == "__main__":
    unittest.main()
