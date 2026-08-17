# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindowContent(object):
    def setupUi(self, central):
        if not central.objectName():
            central.setObjectName(u"central")
        central.resize(1180, 700)
        self.rootLayout = QVBoxLayout(central)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.topBar = QFrame(central)
        self.topBar.setObjectName(u"topBar")
        self.topBar.setMinimumSize(QSize(0, 64))
        self.topBar.setMaximumSize(QSize(16777215, 64))
        self.topBarLayout = QHBoxLayout(self.topBar)
        self.topBarLayout.setSpacing(10)
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.topBarLayout.setContentsMargins(24, 8, 24, 8)
        self.logoLabel = QLabel(self.topBar)
        self.logoLabel.setObjectName(u"logoLabel")

        self.topBarLayout.addWidget(self.logoLabel)

        self.topBarSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBarLayout.addItem(self.topBarSpacer)

        self.exportButton = QPushButton(self.topBar)
        self.exportButton.setObjectName(u"exportButton")

        self.topBarLayout.addWidget(self.exportButton)

        self.themeButton = QPushButton(self.topBar)
        self.themeButton.setObjectName(u"themeButton")

        self.topBarLayout.addWidget(self.themeButton)


        self.rootLayout.addWidget(self.topBar)

        self.bodyWidget = QWidget(central)
        self.bodyWidget.setObjectName(u"bodyWidget")
        self.bodyLayout = QVBoxLayout(self.bodyWidget)
        self.bodyLayout.setSpacing(14)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(24, 18, 24, 18)
        self.headerRow = QHBoxLayout()
        self.headerRow.setSpacing(10)
        self.headerRow.setObjectName(u"headerRow")
        self.searchEdit = QLineEdit(self.bodyWidget)
        self.searchEdit.setObjectName(u"searchEdit")

        self.headerRow.addWidget(self.searchEdit)

        self.addButton = QPushButton(self.bodyWidget)
        self.addButton.setObjectName(u"addButton")

        self.headerRow.addWidget(self.addButton)

        self.editButton = QPushButton(self.bodyWidget)
        self.editButton.setObjectName(u"editButton")

        self.headerRow.addWidget(self.editButton)

        self.duplicateButton = QPushButton(self.bodyWidget)
        self.duplicateButton.setObjectName(u"duplicateButton")

        self.headerRow.addWidget(self.duplicateButton)

        self.deleteButton = QPushButton(self.bodyWidget)
        self.deleteButton.setObjectName(u"deleteButton")

        self.headerRow.addWidget(self.deleteButton)


        self.bodyLayout.addLayout(self.headerRow)

        self.venueTabs = QTabWidget(self.bodyWidget)
        self.venueTabs.setObjectName(u"venueTabs")
        self.venueTabs.setDocumentMode(True)

        self.bodyLayout.addWidget(self.venueTabs)


        self.rootLayout.addWidget(self.bodyWidget)

        self.statusBarFrame = QFrame(central)
        self.statusBarFrame.setObjectName(u"statusBarFrame")
        self.statusBarFrame.setMinimumSize(QSize(0, 34))
        self.statusBarFrame.setMaximumSize(QSize(16777215, 34))
        self.statusBarLayout = QHBoxLayout(self.statusBarFrame)
        self.statusBarLayout.setObjectName(u"statusBarLayout")
        self.statusBarLayout.setContentsMargins(20, 4, 20, 4)
        self.statusLabel = QLabel(self.statusBarFrame)
        self.statusLabel.setObjectName(u"statusLabel")

        self.statusBarLayout.addWidget(self.statusLabel)

        self.statusBarSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.statusBarLayout.addItem(self.statusBarSpacer)


        self.rootLayout.addWidget(self.statusBarFrame)


        self.retranslateUi(central)

        QMetaObject.connectSlotsByName(central)
    # setupUi

    def retranslateUi(self, central):
        self.logoLabel.setText(QCoreApplication.translate("MainWindowContent", u"\U0001f39f  Ticket Manager", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindowContent", u"\u2b07  Export CSV", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindowContent", u"\u2600  Light Mode", None))
        self.searchEdit.setPlaceholderText(QCoreApplication.translate("MainWindowContent", u"\U0001f50e  Search by name, venue, location, status...", None))
        self.addButton.setText(QCoreApplication.translate("MainWindowContent", u"+  Add Ticket", None))
        self.editButton.setText(QCoreApplication.translate("MainWindowContent", u"Edit", None))
        self.duplicateButton.setText(QCoreApplication.translate("MainWindowContent", u"\u29c9  Duplicate", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindowContent", u"Delete", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindowContent", u"0 tickets", None))
        pass
    # retranslateUi

