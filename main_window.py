"""Main application window: toolbar, per-venue tabs, ticket table, export."""

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QLineEdit, QLabel,
    QTabWidget, QAbstractItemView, QMessageBox, QFileDialog
)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings(ORG_NAME, APP_NAME)
        self.db = Database()
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
