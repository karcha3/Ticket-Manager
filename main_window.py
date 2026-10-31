"""Main application window: toolbar, per-venue tabs, ticket table, export."""

from PySide6.QtCore import Qt, QSettings, QThread, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QLineEdit, QLabel,
    QTabWidget, QAbstractItemView, QMessageBox, QFileDialog,
    QDialog, QVBoxLayout, QHBoxLayout, QApplication
)

import threading

import google_sync
from database import Database
from styles import build_stylesheet, build_palette
from ticket_dialog import TicketDialog
from ui_loader import load_ui

APP_NAME = "Ticket Manager"
ORG_NAME = "LocalTools"
TAB_ALL = "All Venues"

# (key, header label) — id is kept in column 0's item data, not shown.
COLUMNS = [
    ("id", "ID"),
    ("first_name", "First Name"),
    ("last_name", "Last Name"),
    ("venue_type", "Venue Type"),
    ("ticket_type", "Ticket Type"),
    ("venue_name", "Venue / Event"),
    ("location", "Location"),
    ("date", "Date"),
    ("time", "Time"),
    ("seat", "Seat / Section"),
    ("price", "Price"),
    ("status", "Status"),
]


class _Worker(QThread):
    """Runs one slow task (network) off the window thread and reports the result."""
    done = Signal(object, object)   # (result, error)

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def run(self):
        try:
            self.done.emit(self._fn(), None)
        except Exception as exc:  # noqa: BLE001
            self.done.emit(None, exc)


class _WebSignInDialog(QDialog):
    """Shown while the user signs in to Google in their web browser."""

    def __init__(self, parent, session):
        super().__init__(parent)
        self.setWindowTitle("Sign in with Google")
        self.setMinimumWidth(460)
        self.cancelled = threading.Event()
        self._session = session
        layout = QVBoxLayout(self)
        text = QLabel("Your web browser should have opened so you can sign in to Google and allow "
                      "access. When you are done, come back to this window.<br><br>"
                      "If nothing opened, click <b>Open the page</b> or copy this link into your "
                      "browser:")
        text.setTextFormat(Qt.TextFormat.RichText)
        text.setWordWrap(True)
        link = QLineEdit(session.url)
        link.setReadOnly(True)
        row = QHBoxLayout()
        open_btn = QPushButton("Open the page")
        open_btn.clicked.connect(session.open_browser)
        copy_btn = QPushButton("Copy link")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(session.url))
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        row.addStretch(1)
        for w in (open_btn, copy_btn, cancel_btn):
            row.addWidget(w)
        layout.addWidget(text)
        layout.addWidget(link)
        layout.addLayout(row)

    def reject(self):            # Cancel button, Esc, or closing the window
        self.cancelled.set()
        super().reject()

    def finished_signing_in(self):   # close without counting it as a cancel
        super().accept()


class _CredentialsDialog(QDialog):
    """Asks for the user's own Google Cloud Client ID and secret."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Google credentials")
        self.setMinimumWidth(480)
        cid, secret = google_sync.get_client()
        layout = QVBoxLayout(self)
        info = QLabel(
            "To sync with Google you need your own free Google Cloud credentials: an OAuth "
            "client of type <b>Desktop app</b>. Step-by-step guide: "
            "<a href='https://github.com/karcha3/Ticket-Manager/blob/main/GOOGLE-SETUP.md'>"
            "GOOGLE-SETUP.md</a>")
        info.setTextFormat(Qt.TextFormat.RichText)
        info.setOpenExternalLinks(True)
        info.setWordWrap(True)
        self.id_edit = QLineEdit(cid)
        self.id_edit.setPlaceholderText("Client ID (ends with .apps.googleusercontent.com)")
        self.secret_edit = QLineEdit(secret)
        self.secret_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.secret_edit.setPlaceholderText("Client secret")
        row = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        row.addStretch(1)
        row.addWidget(save_btn)
        row.addWidget(cancel_btn)
        for w in (info, self.id_edit, self.secret_edit):
            layout.addWidget(w)
        layout.addLayout(row)

    def values(self):
        return self.id_edit.text(), self.secret_edit.text()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings(ORG_NAME, APP_NAME)
        self.db = Database()
        self._workers = []
        self._on_ok = None
        self._on_error = None
        self._signin_dialog = None
        self.setWindowTitle(APP_NAME)
        self.resize(1180, 700)
        self.setMinimumSize(900, 560)

        self.tab_tables = {}    # tab name -> QTableWidget
        self.tab_data = {}      # tab name -> full (unfiltered) ticket list
        self.tab_filtered = {}  # tab name -> currently displayed ticket list
        self.all_tickets = []

        self._build_ui()
        self._reload_and_refresh()

        dark = self.settings.value("dark_mode", True, type=bool)
        self.apply_theme(dark)

    # ---------------------------------------------------------- UI build
    def _build_ui(self):
        self.content = load_ui("mainwindow.ui")
        self.setCentralWidget(self.content)

        self.theme_button = self.content.findChild(QPushButton, "themeButton")
        self.export_button = self.content.findChild(QPushButton, "exportButton")
        self.search_edit = self.content.findChild(QLineEdit, "searchEdit")
        self.add_button = self.content.findChild(QPushButton, "addButton")
        self.edit_button = self.content.findChild(QPushButton, "editButton")
        self.duplicate_button = self.content.findChild(QPushButton, "duplicateButton")
        self.delete_button = self.content.findChild(QPushButton, "deleteButton")
        self.tab_widget = self.content.findChild(QTabWidget, "venueTabs")
        self.status_label = self.content.findChild(QLabel, "statusLabel")

        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.export_button.setCursor(Qt.PointingHandCursor)
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.edit_button.setCursor(Qt.PointingHandCursor)
        self.duplicate_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setCursor(Qt.PointingHandCursor)

        self.theme_button.clicked.connect(self._toggle_theme)
        self.export_button.clicked.connect(self._export_csv)

        # "Import CSV" button, placed just left of "Export CSV"
        self.import_button = QPushButton("⬆  Import CSV")
        self.import_button.setObjectName("exportButton")  # reuse its style
        self.import_button.setCursor(Qt.PointingHandCursor)
        self.import_button.clicked.connect(self._import_csv)
        top_layout = self.export_button.parentWidget().layout()
        top_layout.insertWidget(top_layout.indexOf(self.export_button), self.import_button)

        # "Sync" button: click to sync, right-click for options
        self.sync_button = QPushButton("☁  Sync")
        self.sync_button.setObjectName("exportButton")
        self.sync_button.setCursor(Qt.PointingHandCursor)
        self.sync_button.setToolTip("Click to sync. Right-click for options.")
        self.sync_button.clicked.connect(self._sync_now)
        self.sync_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sync_button.customContextMenuRequested.connect(self._sync_menu)
        top_layout.insertWidget(top_layout.indexOf(self.import_button), self.sync_button)
        self.search_edit.textChanged.connect(self._apply_search_filter)
        self.add_button.clicked.connect(self._add_ticket)
        self.edit_button.clicked.connect(self._edit_selected)
        self.duplicate_button.clicked.connect(self._duplicate_selected)
        self.delete_button.clicked.connect(self._delete_selected)
        self.tab_widget.currentChanged.connect(lambda _i: self._update_status_bar_for_current_tab())

    def _create_table(self):
        table = QTableWidget(0, len(COLUMNS) - 1)
        table.setObjectName("ticketTable")
        table.setHorizontalHeaderLabels([label for _key, label in COLUMNS[1:]])
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setHighlightSections(False)
        table.setSortingEnabled(True)
        table.doubleClicked.connect(self._edit_selected)
        return table

    # ---------------------------------------------------------- data / tabs
    def _reload_and_refresh(self):
        self.all_tickets = self.db.get_all_tickets()
        self._rebuild_tabs()

    def _rebuild_tabs(self):
        current_text = None
        idx = self.tab_widget.currentIndex()
        if idx >= 0:
            current_text = self.tab_widget.tabText(idx)

        self.tab_widget.blockSignals(True)
        while self.tab_widget.count():
            self.tab_widget.removeTab(0)
        self.tab_tables.clear()
        self.tab_data.clear()
        self.tab_filtered.clear()

        venues = sorted(
            {(t.get("venue_name") or "").strip() for t in self.all_tickets
             if (t.get("venue_name") or "").strip()},
            key=str.lower
        )
        tab_defs = [(TAB_ALL, list(self.all_tickets))]
        for v in venues:
            tab_defs.append((v, [t for t in self.all_tickets
                                  if (t.get("venue_name") or "").strip() == v]))

        for name, tickets in tab_defs:
            table = self._create_table()
            container = QWidget()
            lay = QVBoxLayout(container)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.addWidget(table)
            self.tab_widget.addTab(container, name)
            self.tab_tables[name] = table
            self.tab_data[name] = tickets

        restore_idx = 0
        if current_text:
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == current_text:
                    restore_idx = i
                    break
        self.tab_widget.setCurrentIndex(restore_idx)
        self.tab_widget.blockSignals(False)

        self._apply_search_filter()

    def _populate_tab_table(self, table: QTableWidget, tickets: list):
        table.setSortingEnabled(False)
        table.setRowCount(0)
        for t in tickets:
            row = table.rowCount()
            table.insertRow(row)
            values = [
                t.get("first_name", ""),
                t.get("last_name", ""),
                t.get("venue_type", ""),
                t.get("ticket_type", ""),
                t.get("venue_name", ""),
                t.get("location", ""),
                t.get("date", ""),
                t.get("time", ""),
                t.get("seat", ""),
                f"${t.get('price', 0):,.2f}",
                t.get("status", ""),
            ]
            dim = t.get("status") in ("Cancelled", "Refunded")
            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if col == 0:
                    item.setData(Qt.UserRole, t["id"])
                if dim:
                    item.setForeground(QColor("#9096a3"))
                table.setItem(row, col, item)
        table.setSortingEnabled(True)

    # ---------------------------------------------------------- search
    def _apply_search_filter(self):
        text = self.search_edit.text().strip().lower()
        for name, table in self.tab_tables.items():
            tickets = self.tab_data.get(name, [])
            if text:
                filtered = [t for t in tickets
                            if text in " ".join(str(v).lower() for v in t.values())]
            else:
                filtered = tickets
            self.tab_filtered[name] = filtered
            self._populate_tab_table(table, filtered)
        self._update_status_bar_for_current_tab()

    def _update_status_bar_for_current_tab(self):
        idx = self.tab_widget.currentIndex()
        if idx < 0:
            self.status_label.setText("0 tickets")
            return
        name = self.tab_widget.tabText(idx)
        tickets = self.tab_filtered.get(name, self.tab_data.get(name, []))
        count = len(tickets)
        total = sum(t.get("price", 0) or 0 for t in tickets
                    if t.get("status") not in ("Cancelled", "Refunded"))
        noun = "ticket" if count == 1 else "tickets"
        self.status_label.setText(
            f'{count} {noun} in "{name}"   •   Active value: ${total:,.2f}'
        )

    # ---------------------------------------------------------- selection helpers
    def _current_table(self):
        idx = self.tab_widget.currentIndex()
        if idx < 0:
            return None
        name = self.tab_widget.tabText(idx)
        return self.tab_tables.get(name)

    def _selected_ticket_id(self):
        table = self._current_table()
        if table is None:
            return None
        row = table.currentRow()
        if row < 0:
            return None
        item = table.item(row, 0)
        if item is None:
            return None
        return item.data(Qt.UserRole)

    # ---------------------------------------------------------- actions
    def _add_ticket(self):
        idx = self.tab_widget.currentIndex()
        default_venue = None
        if idx > 0:
            default_venue = self.tab_widget.tabText(idx)
        known_venues = self.db.get_distinct_venues()
        dialog = TicketDialog(self, known_venues=known_venues, default_venue=default_venue)
        if dialog.exec() == dialog.Accepted:
            self.db.add_ticket(dialog.get_data())
            self._reload_and_refresh()
            self.search_edit.clear()

    def _edit_selected(self):
        ticket_id = self._selected_ticket_id()
        if ticket_id is None:
            QMessageBox.information(self, "No Selection", "Select a ticket to edit first.")
            return
        ticket = next((t for t in self.all_tickets if t["id"] == ticket_id), None)
        if not ticket:
            return
        known_venues = self.db.get_distinct_venues()
        dialog = TicketDialog(self, ticket=ticket, known_venues=known_venues)
        if dialog.exec() == dialog.Accepted:
            self.db.update_ticket(ticket_id, dialog.get_data())
            self._reload_and_refresh()

    def _duplicate_selected(self):
        ticket_id = self._selected_ticket_id()
        if ticket_id is None:
            QMessageBox.information(self, "No Selection", "Select a ticket to duplicate first.")
            return
        ticket = next((t for t in self.all_tickets if t["id"] == ticket_id), None)
        if not ticket:
            return
        known_venues = self.db.get_distinct_venues()
        dialog = TicketDialog(self, prefill=ticket, known_venues=known_venues)
        if dialog.exec() == dialog.Accepted:
            self.db.add_ticket(dialog.get_data())
            self._reload_and_refresh()

    def _delete_selected(self):
        ticket_id = self._selected_ticket_id()
        if ticket_id is None:
            QMessageBox.information(self, "No Selection", "Select a ticket to delete first.")
            return
        ticket = next((t for t in self.all_tickets if t["id"] == ticket_id), None)
        name = f'{ticket.get("first_name","")} {ticket.get("last_name","")}'.strip() if ticket else ""
        reply = QMessageBox.question(
            self, "Delete Ticket",
            f'Are you sure you want to delete the ticket for "{name}"?\nThis cannot be undone.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.delete_ticket(ticket_id)
            self._reload_and_refresh()

    def _export_csv(self):
        idx = self.tab_widget.currentIndex()
        name = self.tab_widget.tabText(idx) if idx >= 0 else TAB_ALL
        tickets = self.tab_filtered.get(name, self.tab_data.get(name, []))
        if not tickets:
            QMessageBox.information(self, "Nothing to Export",
                                     "There are no tickets to export in the current view.")
            return
        safe_name = name.replace(" ", "_").replace("/", "-")
        suggested = "tickets_all.csv" if name == TAB_ALL else f"tickets_{safe_name}.csv"
        path, _ = QFileDialog.getSaveFileName(self, "Export Tickets to CSV", suggested,
                                               "CSV Files (*.csv)")
        if not path:
            return
        try:
            self.db.export_csv(path, tickets)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Export Failed", f"Could not export tickets:\n{exc}")
            return
        QMessageBox.information(self, "Export Complete",
                                 f"Exported {len(tickets)} ticket(s) to:\n{path}")

    def _import_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Tickets from CSV", "",
                                               "CSV Files (*.csv)")
        if not path:
            return
        try:
            added, skipped, invalid = self.db.import_csv(path)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Import Failed", f"Could not import tickets:\n{exc}")
            return
        self._reload_and_refresh()
        QMessageBox.information(
            self, "Import Complete",
            f"Imported {added} ticket(s).\n"
            f"Skipped {skipped} already in the app.\n"
            f"Ignored {invalid} invalid row(s).")

    # ---------------------------------------------------------- sync
    def _sync_mode(self):
        return self.settings.value("sync_mode", "", type=str)

    def _sync_menu(self, pos):
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        menu.addAction("Sync now", self._sync_now)
        if google_sync.is_signed_in():
            menu.addAction("Sign out of Google", self._google_sign_out)
        else:
            menu.addAction("Sign in with Google…", self._google_sign_in)
        menu.addAction("Google credentials…", self._google_credentials)
        menu.addAction("Use a sync file instead…", lambda: self._sync_file(choose=True))
        if self._sync_mode():
            menu.addAction("Stop syncing", self._sync_stop)
        menu.exec(self.sync_button.mapToGlobal(pos))

    def _sync_stop(self, _checked=False):
        self.settings.remove("sync_path")
        self.settings.remove("sync_mode")
        QMessageBox.information(self, "Sync", "Syncing is turned off. Your tickets were not changed.")

    def _sync_now(self, _checked=False):
        mode = self._sync_mode()
        path = self.settings.value("sync_path", "", type=str)
        if mode == "google" and google_sync.is_signed_in():
            return self._google_sync()
        if path and mode in ("", "file"):
            return self._sync_file()
        box = QMessageBox(self)
        box.setWindowTitle("Sync")
        box.setText("How do you want to sync your tickets?")
        google_btn = box.addButton("Sign in with Google", QMessageBox.ButtonRole.AcceptRole)
        file_btn = box.addButton("Use a sync file", QMessageBox.ButtonRole.ActionRole)
        box.addButton(QMessageBox.StandardButton.Cancel)
        box.exec()
        if box.clickedButton() is google_btn:
            self._google_sign_in()
        elif box.clickedButton() is file_btn:
            self._sync_file(choose=True)

    # --- sync through a file in a cloud folder
    def _sync_file(self, choose=False):
        path = self.settings.value("sync_path", "", type=str)
        if choose or not path:
            QMessageBox.information(
                self, "Choose Sync File",
                "Pick a sync file in a folder that your cloud service keeps in sync "
                "(for example a Google Drive for desktop folder).\n\n"
                "If you already created the file on another device, select that file.")
            path, _ = QFileDialog.getSaveFileName(
                self, "Choose Sync File", "ticket-manager-sync.json", "Sync file (*.json)",
                options=QFileDialog.Option.DontConfirmOverwrite)
            if not path:
                return
            self.settings.setValue("sync_path", path)
            self.settings.setValue("sync_mode", "file")
        try:
            changed = self.db.sync_with_file(path)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Sync Failed", f"Could not sync:\n{exc}")
            return
        self._reload_and_refresh()
        QMessageBox.information(self, "Sync Complete",
                                f"Sync finished. {changed} ticket(s) were updated from the sync file.")

    # --- sync through Google Drive (network work runs in a background thread)
    def _run(self, fn, on_ok, on_error=None):
        """Run fn() in the background, then call on_ok(result) in the window thread."""
        self.sync_button.setEnabled(False)
        self._on_ok = on_ok
        self._on_error = on_error
        self._workers = [w for w in self._workers if w.isRunning()]
        worker = _Worker(fn)
        worker.done.connect(self._worker_done)
        self._workers.append(worker)
        worker.start()

    def _worker_done(self, result, error):
        self.sync_button.setEnabled(True)
        if error is not None:
            if self._on_error:
                self._on_error(error)
            else:
                QMessageBox.critical(self, "Google Sync", str(error))
            return
        self._on_ok(result)

    def _google_credentials(self, _checked=False):
        dlg = _CredentialsDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return False
        try:
            google_sync.set_client(*dlg.values())
        except ValueError as exc:
            QMessageBox.warning(self, "Google credentials", str(exc))
            return False
        return True

    def _google_sign_in(self, _checked=False):
        if not google_sync.is_configured() and not self._google_credentials():
            return
        try:
            session = google_sync.WebSignIn()
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Google Sync", str(exc))
            return
        dlg = _WebSignInDialog(self, session)
        self._signin_dialog = dlg
        session.open_browser()
        self._run(lambda: session.wait(dlg.cancelled), self._after_google_sign_in,
                  self._signin_failed)
        dlg.open()

    def _close_signin_dialog(self):
        dlg, self._signin_dialog = self._signin_dialog, None
        if dlg is not None:
            dlg.finished_signing_in()

    def _signin_failed(self, error):
        self._close_signin_dialog()
        if not isinstance(error, google_sync.SignInCancelled):
            QMessageBox.critical(self, "Google Sync", str(error))

    def _after_google_sign_in(self, _result):
        self._close_signin_dialog()
        self.settings.setValue("sync_mode", "google")
        self._google_sync()

    def _google_sync(self):
        self._run(google_sync.download, self._google_downloaded)

    def _google_downloaded(self, doc):
        try:
            changed, out = self.db.merge_doc(doc)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Sync Failed", f"Could not sync:\n{exc}")
            return
        self._reload_and_refresh()
        self._run(lambda: google_sync.upload(out),
                  lambda _r: QMessageBox.information(
                      self, "Sync Complete",
                      f"Sync finished. {changed} ticket(s) were updated from Google Drive."))

    def _google_sign_out(self, _checked=False):
        self._run(google_sync.sign_out, self._after_google_sign_out)

    def _after_google_sign_out(self, _result):
        if self._sync_mode() == "google":
            self.settings.remove("sync_mode")
        QMessageBox.information(self, "Google",
                                "You are signed out of Google. Your tickets were not changed.")

    # ---------------------------------------------------------- theming
    def _toggle_theme(self):
        currently_dark = self.settings.value("dark_mode", True, type=bool)
        self.apply_theme(not currently_dark)

    def apply_theme(self, dark: bool):
        self.settings.setValue("dark_mode", dark)
        self.theme_button.setText("☀  Light Mode" if dark else "🌙  Dark Mode")
        app = QApplication.instance()
        # Make the window title bar follow the theme too (needs Qt 6.8+;
        # older versions simply skip this).
        try:
            app.styleHints().setColorScheme(
                Qt.ColorScheme.Dark if dark else Qt.ColorScheme.Light)
        except AttributeError:
            pass
        app.setPalette(build_palette(dark))
        app.setStyleSheet(build_stylesheet(dark))

    # ---------------------------------------------------------- lifecycle
    def closeEvent(self, event):
        self.db.close()
        event.accept()
