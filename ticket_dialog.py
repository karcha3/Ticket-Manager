"""Add / edit ticket dialog, built from ui/ticketdialog.ui."""

from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtWidgets import (
    QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QTextEdit,
    QDialogButtonBox, QLabel, QMessageBox, QDialog, QToolButton
)

from ui_loader import load_ui
from pickers import CalendarPopup, TimePopup


class TicketDialog:
    """Wraps the QDialog loaded from ticketdialog.ui and exposes a simple
    get_data() / exec() interface, matching what MainWindow expects.

    Pass `ticket` to edit an existing ticket in place, `prefill` to start a
    new ticket pre-filled with another ticket's data (used for duplicating),
    or neither for a blank ticket.
    """

    def __init__(self, parent=None, ticket=None, prefill=None,
                 known_venues=None, default_venue=None):
        self.ticket = ticket
        self.ui = load_ui("ticketdialog.ui", parent)

        # Grab widgets defined in the .ui file by objectName.
        self.title_label = self.ui.findChild(QLabel, "titleLabel")
        self.subtitle_label = self.ui.findChild(QLabel, "subtitleLabel")
        self.first_name = self.ui.findChild(QLineEdit, "firstNameEdit")
        self.last_name = self.ui.findChild(QLineEdit, "lastNameEdit")
        self.venue_type = self.ui.findChild(QComboBox, "venueTypeCombo")
        self.ticket_type = self.ui.findChild(QComboBox, "ticketTypeCombo")
        self.venue_name = self.ui.findChild(QComboBox, "venueNameCombo")
        self.location = self.ui.findChild(QLineEdit, "locationEdit")
        self.date_edit = self.ui.findChild(QDateEdit, "dateEdit")
        self.date_calendar_button = self.ui.findChild(QToolButton, "dateCalendarButton")
        self.time_combo = self.ui.findChild(QComboBox, "timeCombo")
        self.time_clock_button = self.ui.findChild(QToolButton, "timeClockButton")
        self.seat = self.ui.findChild(QLineEdit, "seatEdit")
        self.price = self.ui.findChild(QDoubleSpinBox, "priceSpin")
        self.status = self.ui.findChild(QComboBox, "statusCombo")
        self.notes = self.ui.findChild(QTextEdit, "notesEdit")
        self.button_box = self.ui.findChild(QDialogButtonBox, "buttonBox")

        for btn in (self.date_calendar_button, self.time_clock_button):
            btn.setCursor(Qt.PointingHandCursor)

        # Sensible defaults for a brand-new ticket.
        self.date_edit.setDate(QDate.currentDate())
        self.time_combo.setCurrentText("19:00")

        # Populate the venue dropdown with venues already used, so the user
        # can quickly pick an existing one or type a brand-new name.
        if known_venues:
            self.venue_name.addItems(known_venues)
        self.venue_name.setCurrentText("")

        if ticket:
            title = "Edit Ticket"
            self._populate(ticket)
        elif prefill:
            title = "Duplicate Ticket"
            self.subtitle_label.setText("Creating a copy — adjust anything you need, then save.")
            self._populate(prefill)
        else:
            title = "New Ticket"
            if default_venue:
                self.venue_name.setCurrentText(default_venue)

        self.ui.setWindowTitle(title)
        self.title_label.setText(title)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.ui.reject)
        self.date_calendar_button.clicked.connect(self._open_calendar_popup)
        self.time_clock_button.clicked.connect(self._open_time_popup)
        self._calendar_popup = None
        self._time_popup = None

    def _open_calendar_popup(self):
        self._calendar_popup = CalendarPopup(self.ui, self.date_edit)
        self._calendar_popup.show_below(self.date_calendar_button)

    def _open_time_popup(self):
        self._time_popup = TimePopup(self.ui, self.time_combo)
        self._time_popup.show_below(self.time_clock_button)

    def _populate(self, t):
        self.first_name.setText(t.get("first_name", ""))
        self.last_name.setText(t.get("last_name", ""))
        if t.get("venue_type"):
            self.venue_type.setCurrentText(t.get("venue_type"))
        if t.get("ticket_type"):
            self.ticket_type.setCurrentText(t.get("ticket_type"))
        self.venue_name.setCurrentText(t.get("venue_name", "") or "")
        self.location.setText(t.get("location", ""))
        d = t.get("date")
        if d:
            qd = QDate.fromString(d, "yyyy-MM-dd")
            if qd.isValid():
                self.date_edit.setDate(qd)
        tm = t.get("time")
        if tm:
            qt = QTime.fromString(tm, "HH:mm")
            if qt.isValid():
                self.time_combo.setCurrentText(qt.toString("HH:mm"))
        self.seat.setText(t.get("seat", ""))
        self.price.setValue(t.get("price") or 0.0)
        if t.get("status"):
            self.status.setCurrentText(t.get("status"))
        self.notes.setPlainText(t.get("notes", "") or "")

    def _on_accept(self):
        if not self.first_name.text().strip() or not self.last_name.text().strip():
            QMessageBox.warning(self.ui, "Missing Information",
                                 "First name and last name are required.")
            return
        self.ui.accept()

    def exec(self):
        return self.ui.exec()

    @property
    def Accepted(self):
        return QDialog.Accepted

    def get_data(self) -> dict:
        # Normalize free-typed time text into HH:mm where possible.
        time_text = self.time_combo.currentText().strip()
        qt = QTime.fromString(time_text, "HH:mm")
        time_value = qt.toString("HH:mm") if qt.isValid() else time_text

        return {
            "first_name": self.first_name.text().strip(),
            "last_name": self.last_name.text().strip(),
            "venue_type": self.venue_type.currentText().strip(),
            "ticket_type": self.ticket_type.currentText().strip(),
            "venue_name": self.venue_name.currentText().strip(),
            "location": self.location.text().strip(),
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "time": time_value,
            "seat": self.seat.text().strip(),
            "price": self.price.value(),
            "status": self.status.currentText(),
            "notes": self.notes.toPlainText().strip(),
        }
