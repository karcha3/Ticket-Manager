"""Small helper for loading Qt Designer .ui files at runtime with QUiLoader."""

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader

from resources import resource_path


def load_ui(filename: str, parent=None):
    """Load a .ui file from the ui/ folder and return the top-level widget."""
    path = resource_path("ui", filename)
    loader = QUiLoader()
    ui_file = QFile(path)
    if not ui_file.open(QIODevice.ReadOnly):
        raise IOError(f"Could not open UI file: {path}")
    widget = loader.load(ui_file, parent)
    ui_file.close()
    if widget is None:
        raise RuntimeError(f"Failed to load UI file: {path} ({loader.errorString()})")
    return widget
