"""Path helpers that work both when running from source and when frozen
into a standalone .exe with PyInstaller.

- resource_path(...)  -> read-only files bundled with the app (ui/, assets/)
- app_data_dir()      -> a writable, per-user folder for the database
"""

import os
import sys


def resource_path(*parts) -> str:
    """Resolve a path to a bundled, read-only resource (e.g. a .ui file or
    an icon). Works whether running from source or from a PyInstaller
    onefile/onedir build.
    """
    if getattr(sys, "frozen", False):
        # PyInstaller onefile extracts bundled data next to sys._MEIPASS;
        # onedir builds keep it next to the executable.
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


def app_data_dir() -> str:
    """A writable, per-user folder to store the ticket database in. Using
    this (instead of the install location) means the app keeps working -
    and keeps its data - even when installed somewhere read-only like
    Program Files.
    """
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    data_dir = os.path.join(base, "TicketManager")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir
