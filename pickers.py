"""Small popup widgets: a calendar date-picker and a dial-based time-picker,
opened from the 📅 and 🕐 buttons next to the date/time fields."""

from PySide6.QtCore import Qt, QTime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCalendarWidget,
    QDial, QPushButton
)


class CalendarPopup(QWidget):
    """A small popup showing a QCalendarWidget. Clicking a date applies it
    to the given QDateEdit and closes the popup."""

    def __init__(self, anchor_widget, date_edit):
        super().__init__(anchor_widget.window(), Qt.Popup)
        self.setObjectName("pickerPopup")
        self.date_edit = date_edit

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setSelectedDate(date_edit.date())
        self.calendar.clicked.connect(self._pick)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addWidget(self.calendar)

    def _pick(self, date):
        self.date_edit.setDate(date)
        self.close()

    def show_below(self, button):
        self.move(button.mapToGlobal(button.rect().bottomLeft()))
        self.show()


class TimePopup(QWidget):
    """A small popup with an hour dial and a minute dial — a 'clock style'
    time selector. Turning the dials updates a live HH:MM label; Done
    applies the value to the given time QComboBox and closes the popup."""

    def __init__(self, anchor_widget, time_combo):
        super().__init__(anchor_widget.window(), Qt.Popup)
        self.setObjectName("pickerPopup")
        self.time_combo = time_combo

        current = QTime.fromString(time_combo.currentText().strip(), "HH:mm")
        if not current.isValid():
            current = QTime.currentTime()

        self.time_label = QLabel(current.toString("HH:mm"), self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setObjectName("timePopupLabel")

        self.hour_dial = QDial(self)
        self.hour_dial.setRange(0, 23)
        self.hour_dial.setWrapping(True)
        self.hour_dial.setNotchesVisible(True)
        self.hour_dial.setValue(current.hour())
        self.hour_dial.valueChanged.connect(self._update_label)

        self.minute_dial = QDial(self)
        self.minute_dial.setRange(0, 59)
        self.minute_dial.setSingleStep(1)
        self.minute_dial.setWrapping(True)
        self.minute_dial.setNotchesVisible(True)
        self.minute_dial.setValue(current.minute())
        self.minute_dial.valueChanged.connect(self._update_label)

        hour_col = QVBoxLayout()
        hour_col.addWidget(self.hour_dial)
        hour_col.addWidget(_centered_label("Hour"))

        minute_col = QVBoxLayout()
        minute_col.addWidget(self.minute_dial)
        minute_col.addWidget(_centered_label("Minute"))

        dials_row = QHBoxLayout()
        dials_row.setSpacing(16)
        dials_row.addLayout(hour_col)
        dials_row.addLayout(minute_col)

        done_btn = QPushButton("Done", self)
        done_btn.setObjectName("primaryButton")
        done_btn.setCursor(Qt.PointingHandCursor)
        done_btn.clicked.connect(self._apply)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)
        layout.addWidget(self.time_label)
        layout.addLayout(dials_row)
        layout.addWidget(done_btn)

    def _update_label(self):
        h = self.hour_dial.value()
        m = self.minute_dial.value()
        self.time_label.setText(f"{h:02d}:{m:02d}")

    def _apply(self):
        h = self.hour_dial.value()
        m = self.minute_dial.value()
        self.time_combo.setCurrentText(f"{h:02d}:{m:02d}")
        self.close()

    def show_below(self, button):
        self.move(button.mapToGlobal(button.rect().bottomLeft()))
        self.show()


def _centered_label(text):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    return label
