# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ticketdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateEdit,
    QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)

class Ui_TicketDialog(object):
    def setupUi(self, TicketDialog):
        if not TicketDialog.objectName():
            TicketDialog.setObjectName(u"TicketDialog")
        TicketDialog.resize(460, 640)
        TicketDialog.setModal(True)
        self.outerLayout = QVBoxLayout(TicketDialog)
        self.outerLayout.setSpacing(14)
        self.outerLayout.setObjectName(u"outerLayout")
        self.outerLayout.setContentsMargins(24, 24, 24, 20)
        self.titleLabel = QLabel(TicketDialog)
        self.titleLabel.setObjectName(u"titleLabel")

        self.outerLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(TicketDialog)
        self.subtitleLabel.setObjectName(u"subtitleLabel")

        self.outerLayout.addWidget(self.subtitleLabel)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(10)
        self.firstNameLabel = QLabel(TicketDialog)
        self.firstNameLabel.setObjectName(u"firstNameLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.firstNameLabel)

        self.firstNameEdit = QLineEdit(TicketDialog)
        self.firstNameEdit.setObjectName(u"firstNameEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.firstNameEdit)

        self.lastNameLabel = QLabel(TicketDialog)
        self.lastNameLabel.setObjectName(u"lastNameLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lastNameLabel)

        self.lastNameEdit = QLineEdit(TicketDialog)
        self.lastNameEdit.setObjectName(u"lastNameEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lastNameEdit)

        self.venueTypeLabel = QLabel(TicketDialog)
        self.venueTypeLabel.setObjectName(u"venueTypeLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.venueTypeLabel)

        self.venueTypeCombo = QComboBox(TicketDialog)
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.addItem("")
        self.venueTypeCombo.setObjectName(u"venueTypeCombo")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.venueTypeCombo)

        self.ticketTypeLabel = QLabel(TicketDialog)
        self.ticketTypeLabel.setObjectName(u"ticketTypeLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.ticketTypeLabel)

        self.ticketTypeCombo = QComboBox(TicketDialog)
        self.ticketTypeCombo.addItem("")
        self.ticketTypeCombo.addItem("")
        self.ticketTypeCombo.addItem("")
        self.ticketTypeCombo.addItem("")
        self.ticketTypeCombo.addItem("")
        self.ticketTypeCombo.addItem("")
        self.ticketTypeCombo.addItem("")
        self.ticketTypeCombo.addItem("")
        self.ticketTypeCombo.setObjectName(u"ticketTypeCombo")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.ticketTypeCombo)

        self.venueNameLabel = QLabel(TicketDialog)
        self.venueNameLabel.setObjectName(u"venueNameLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.venueNameLabel)

        self.venueNameCombo = QComboBox(TicketDialog)
        self.venueNameCombo.setObjectName(u"venueNameCombo")
        self.venueNameCombo.setEditable(True)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.venueNameCombo)

        self.locationLabel = QLabel(TicketDialog)
        self.locationLabel.setObjectName(u"locationLabel")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.locationLabel)

        self.locationEdit = QLineEdit(TicketDialog)
        self.locationEdit.setObjectName(u"locationEdit")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.locationEdit)

        self.dateLabel = QLabel(TicketDialog)
        self.dateLabel.setObjectName(u"dateLabel")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.dateLabel)

        self.dateRow = QHBoxLayout()
        self.dateRow.setSpacing(6)
        self.dateRow.setObjectName(u"dateRow")
        self.dateEdit = QDateEdit(TicketDialog)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setCalendarPopup(True)

        self.dateRow.addWidget(self.dateEdit)

        self.dateCalendarButton = QToolButton(TicketDialog)
        self.dateCalendarButton.setObjectName(u"dateCalendarButton")

        self.dateRow.addWidget(self.dateCalendarButton)


        self.formLayout.setLayout(6, QFormLayout.ItemRole.FieldRole, self.dateRow)

        self.timeLabel = QLabel(TicketDialog)
        self.timeLabel.setObjectName(u"timeLabel")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.timeLabel)

        self.timeRow = QHBoxLayout()
        self.timeRow.setSpacing(6)
        self.timeRow.setObjectName(u"timeRow")
        self.timeCombo = QComboBox(TicketDialog)
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.addItem("")
        self.timeCombo.setObjectName(u"timeCombo")
        self.timeCombo.setEditable(True)

        self.timeRow.addWidget(self.timeCombo)

        self.timeClockButton = QToolButton(TicketDialog)
        self.timeClockButton.setObjectName(u"timeClockButton")

        self.timeRow.addWidget(self.timeClockButton)


        self.formLayout.setLayout(7, QFormLayout.ItemRole.FieldRole, self.timeRow)

        self.seatLabel = QLabel(TicketDialog)
        self.seatLabel.setObjectName(u"seatLabel")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.seatLabel)

        self.seatEdit = QLineEdit(TicketDialog)
        self.seatEdit.setObjectName(u"seatEdit")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.seatEdit)

        self.priceLabel = QLabel(TicketDialog)
        self.priceLabel.setObjectName(u"priceLabel")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.priceLabel)

        self.priceSpin = QDoubleSpinBox(TicketDialog)
        self.priceSpin.setObjectName(u"priceSpin")
        self.priceSpin.setMaximum(1000000.000000000000000)
        self.priceSpin.setDecimals(2)

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.priceSpin)

        self.statusLabel = QLabel(TicketDialog)
        self.statusLabel.setObjectName(u"statusLabel")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.statusLabel)

        self.statusCombo = QComboBox(TicketDialog)
        self.statusCombo.addItem("")
        self.statusCombo.addItem("")
        self.statusCombo.addItem("")
        self.statusCombo.addItem("")
        self.statusCombo.setObjectName(u"statusCombo")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.statusCombo)

        self.notesLabel = QLabel(TicketDialog)
        self.notesLabel.setObjectName(u"notesLabel")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.notesLabel)

        self.notesEdit = QTextEdit(TicketDialog)
        self.notesEdit.setObjectName(u"notesEdit")
        self.notesEdit.setMaximumSize(QSize(16777215, 70))

        self.formLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.notesEdit)


        self.outerLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(TicketDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.outerLayout.addWidget(self.buttonBox)


        self.retranslateUi(TicketDialog)

        QMetaObject.connectSlotsByName(TicketDialog)
    # setupUi

    def retranslateUi(self, TicketDialog):
        TicketDialog.setWindowTitle(QCoreApplication.translate("TicketDialog", u"Ticket", None))
        self.titleLabel.setText(QCoreApplication.translate("TicketDialog", u"New Ticket", None))
        self.subtitleLabel.setText(QCoreApplication.translate("TicketDialog", u"Fill in the ticket details below.", None))
        self.firstNameLabel.setText(QCoreApplication.translate("TicketDialog", u"First Name*", None))
        self.firstNameEdit.setPlaceholderText(QCoreApplication.translate("TicketDialog", u"e.g. Ada", None))
        self.lastNameLabel.setText(QCoreApplication.translate("TicketDialog", u"Last Name*", None))
        self.lastNameEdit.setPlaceholderText(QCoreApplication.translate("TicketDialog", u"e.g. Lovelace", None))
        self.venueTypeLabel.setText(QCoreApplication.translate("TicketDialog", u"Venue Type", None))
        self.venueTypeCombo.setItemText(0, QCoreApplication.translate("TicketDialog", u"Concert", None))
        self.venueTypeCombo.setItemText(1, QCoreApplication.translate("TicketDialog", u"Theater", None))
        self.venueTypeCombo.setItemText(2, QCoreApplication.translate("TicketDialog", u"Sports", None))
        self.venueTypeCombo.setItemText(3, QCoreApplication.translate("TicketDialog", u"Conference", None))
        self.venueTypeCombo.setItemText(4, QCoreApplication.translate("TicketDialog", u"Cinema", None))
        self.venueTypeCombo.setItemText(5, QCoreApplication.translate("TicketDialog", u"Festival", None))
        self.venueTypeCombo.setItemText(6, QCoreApplication.translate("TicketDialog", u"Exhibition", None))
        self.venueTypeCombo.setItemText(7, QCoreApplication.translate("TicketDialog", u"Comedy Show", None))
        self.venueTypeCombo.setItemText(8, QCoreApplication.translate("TicketDialog", u"Other", None))

        self.ticketTypeLabel.setText(QCoreApplication.translate("TicketDialog", u"Ticket Type", None))
        self.ticketTypeCombo.setItemText(0, QCoreApplication.translate("TicketDialog", u"Standard", None))
        self.ticketTypeCombo.setItemText(1, QCoreApplication.translate("TicketDialog", u"VIP", None))
        self.ticketTypeCombo.setItemText(2, QCoreApplication.translate("TicketDialog", u"Early Bird", None))
        self.ticketTypeCombo.setItemText(3, QCoreApplication.translate("TicketDialog", u"Group", None))
        self.ticketTypeCombo.setItemText(4, QCoreApplication.translate("TicketDialog", u"Student", None))
        self.ticketTypeCombo.setItemText(5, QCoreApplication.translate("TicketDialog", u"Season Pass", None))
        self.ticketTypeCombo.setItemText(6, QCoreApplication.translate("TicketDialog", u"Backstage", None))
        self.ticketTypeCombo.setItemText(7, QCoreApplication.translate("TicketDialog", u"Other", None))

        self.venueNameLabel.setText(QCoreApplication.translate("TicketDialog", u"Venue / Event Name", None))
        self.locationLabel.setText(QCoreApplication.translate("TicketDialog", u"Location", None))
        self.locationEdit.setPlaceholderText(QCoreApplication.translate("TicketDialog", u"City / address", None))
        self.dateLabel.setText(QCoreApplication.translate("TicketDialog", u"Date", None))
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("TicketDialog", u"yyyy-MM-dd", None))
        self.dateCalendarButton.setText(QCoreApplication.translate("TicketDialog", u"\U0001f4c5", None))
#if QT_CONFIG(tooltip)
        self.dateCalendarButton.setToolTip(QCoreApplication.translate("TicketDialog", u"Pick a date", None))
#endif // QT_CONFIG(tooltip)
        self.timeLabel.setText(QCoreApplication.translate("TicketDialog", u"Time", None))
        self.timeCombo.setItemText(0, QCoreApplication.translate("TicketDialog", u"00:00", None))
        self.timeCombo.setItemText(1, QCoreApplication.translate("TicketDialog", u"00:30", None))
        self.timeCombo.setItemText(2, QCoreApplication.translate("TicketDialog", u"01:00", None))
        self.timeCombo.setItemText(3, QCoreApplication.translate("TicketDialog", u"01:30", None))
        self.timeCombo.setItemText(4, QCoreApplication.translate("TicketDialog", u"02:00", None))
        self.timeCombo.setItemText(5, QCoreApplication.translate("TicketDialog", u"02:30", None))
        self.timeCombo.setItemText(6, QCoreApplication.translate("TicketDialog", u"03:00", None))
        self.timeCombo.setItemText(7, QCoreApplication.translate("TicketDialog", u"03:30", None))
        self.timeCombo.setItemText(8, QCoreApplication.translate("TicketDialog", u"04:00", None))
        self.timeCombo.setItemText(9, QCoreApplication.translate("TicketDialog", u"04:30", None))
        self.timeCombo.setItemText(10, QCoreApplication.translate("TicketDialog", u"05:00", None))
        self.timeCombo.setItemText(11, QCoreApplication.translate("TicketDialog", u"05:30", None))
        self.timeCombo.setItemText(12, QCoreApplication.translate("TicketDialog", u"06:00", None))
        self.timeCombo.setItemText(13, QCoreApplication.translate("TicketDialog", u"06:30", None))
        self.timeCombo.setItemText(14, QCoreApplication.translate("TicketDialog", u"07:00", None))
        self.timeCombo.setItemText(15, QCoreApplication.translate("TicketDialog", u"07:30", None))
        self.timeCombo.setItemText(16, QCoreApplication.translate("TicketDialog", u"08:00", None))
        self.timeCombo.setItemText(17, QCoreApplication.translate("TicketDialog", u"08:30", None))
        self.timeCombo.setItemText(18, QCoreApplication.translate("TicketDialog", u"09:00", None))
        self.timeCombo.setItemText(19, QCoreApplication.translate("TicketDialog", u"09:30", None))
        self.timeCombo.setItemText(20, QCoreApplication.translate("TicketDialog", u"10:00", None))
        self.timeCombo.setItemText(21, QCoreApplication.translate("TicketDialog", u"10:30", None))
        self.timeCombo.setItemText(22, QCoreApplication.translate("TicketDialog", u"11:00", None))
        self.timeCombo.setItemText(23, QCoreApplication.translate("TicketDialog", u"11:30", None))
        self.timeCombo.setItemText(24, QCoreApplication.translate("TicketDialog", u"12:00", None))
        self.timeCombo.setItemText(25, QCoreApplication.translate("TicketDialog", u"12:30", None))
        self.timeCombo.setItemText(26, QCoreApplication.translate("TicketDialog", u"13:00", None))
        self.timeCombo.setItemText(27, QCoreApplication.translate("TicketDialog", u"13:30", None))
        self.timeCombo.setItemText(28, QCoreApplication.translate("TicketDialog", u"14:00", None))
        self.timeCombo.setItemText(29, QCoreApplication.translate("TicketDialog", u"14:30", None))
        self.timeCombo.setItemText(30, QCoreApplication.translate("TicketDialog", u"15:00", None))
        self.timeCombo.setItemText(31, QCoreApplication.translate("TicketDialog", u"15:30", None))
        self.timeCombo.setItemText(32, QCoreApplication.translate("TicketDialog", u"16:00", None))
        self.timeCombo.setItemText(33, QCoreApplication.translate("TicketDialog", u"16:30", None))
        self.timeCombo.setItemText(34, QCoreApplication.translate("TicketDialog", u"17:00", None))
        self.timeCombo.setItemText(35, QCoreApplication.translate("TicketDialog", u"17:30", None))
        self.timeCombo.setItemText(36, QCoreApplication.translate("TicketDialog", u"18:00", None))
        self.timeCombo.setItemText(37, QCoreApplication.translate("TicketDialog", u"18:30", None))
        self.timeCombo.setItemText(38, QCoreApplication.translate("TicketDialog", u"19:00", None))
        self.timeCombo.setItemText(39, QCoreApplication.translate("TicketDialog", u"19:30", None))
        self.timeCombo.setItemText(40, QCoreApplication.translate("TicketDialog", u"20:00", None))
        self.timeCombo.setItemText(41, QCoreApplication.translate("TicketDialog", u"20:30", None))
        self.timeCombo.setItemText(42, QCoreApplication.translate("TicketDialog", u"21:00", None))
        self.timeCombo.setItemText(43, QCoreApplication.translate("TicketDialog", u"21:30", None))
        self.timeCombo.setItemText(44, QCoreApplication.translate("TicketDialog", u"22:00", None))
        self.timeCombo.setItemText(45, QCoreApplication.translate("TicketDialog", u"22:30", None))
        self.timeCombo.setItemText(46, QCoreApplication.translate("TicketDialog", u"23:00", None))
        self.timeCombo.setItemText(47, QCoreApplication.translate("TicketDialog", u"23:30", None))

        self.timeClockButton.setText(QCoreApplication.translate("TicketDialog", u"\U0001f550", None))
#if QT_CONFIG(tooltip)
        self.timeClockButton.setToolTip(QCoreApplication.translate("TicketDialog", u"Pick a time", None))
#endif // QT_CONFIG(tooltip)
        self.seatLabel.setText(QCoreApplication.translate("TicketDialog", u"Seat / Section", None))
        self.seatEdit.setPlaceholderText(QCoreApplication.translate("TicketDialog", u"e.g. Row B, Seat 12", None))
        self.priceLabel.setText(QCoreApplication.translate("TicketDialog", u"Price", None))
        self.priceSpin.setPrefix(QCoreApplication.translate("TicketDialog", u"$ ", None))
        self.statusLabel.setText(QCoreApplication.translate("TicketDialog", u"Status", None))
        self.statusCombo.setItemText(0, QCoreApplication.translate("TicketDialog", u"Active", None))
        self.statusCombo.setItemText(1, QCoreApplication.translate("TicketDialog", u"Used", None))
        self.statusCombo.setItemText(2, QCoreApplication.translate("TicketDialog", u"Cancelled", None))
        self.statusCombo.setItemText(3, QCoreApplication.translate("TicketDialog", u"Refunded", None))

        self.notesLabel.setText(QCoreApplication.translate("TicketDialog", u"Notes", None))
        self.notesEdit.setPlaceholderText(QCoreApplication.translate("TicketDialog", u"Optional notes...", None))
    # retranslateUi

