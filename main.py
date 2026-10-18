#!/usr/bin/env python3
"""
Ticket Manager — entry point.

Run with:
    pip install -r requirements.txt
    python main.py

This project can also be opened directly in Qt Creator via
ticket_manager.pyproject. The UI layout lives in ui/mainwindow.ui and
ui/ticketdialog.ui and can be edited visually with Qt Creator's built-in
Designer.
"""

import sys

from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QApplication

from main_window import MainWindow, APP_NAME, ORG_NAME
from resources import resource_path


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    # Fusion draws consistently under custom themes (the default Windows
    # style ignores parts of the dark palette).
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setWindowIcon(QIcon(resource_path("assets", "icon.png")))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
