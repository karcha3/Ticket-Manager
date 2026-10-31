"""Light & dark QSS themes for the Ticket Manager app."""

from PySide6.QtGui import QColor, QPalette


def build_palette(dark: bool) -> QPalette:
    """A matching QPalette. The stylesheet alone does not reach every
    widget (dials, header sort arrows, spin box arrows, native dialogs),
    so without this they keep light-theme colors on a dark window."""
    if dark:
        c = dict(window="#1b1d23", base="#262a33", alt="#1f222a", text="#e7e9ee",
                 dim="#9096a3", button="#262a33", accent="#7c8cff",
                 border="#333844", tip="#262a33")
    else:
        c = dict(window="#f4f5f8", base="#ffffff", alt="#f7f8fb", text="#1e2028",
                 dim="#666c7a", button="#ffffff", accent="#5865f2",
                 border="#e1e3ea", tip="#ffffff")
    p = QPalette()
    p.setColor(QPalette.Window, QColor(c["window"]))
    p.setColor(QPalette.WindowText, QColor(c["text"]))
    p.setColor(QPalette.Base, QColor(c["base"]))
    p.setColor(QPalette.AlternateBase, QColor(c["alt"]))
    p.setColor(QPalette.Text, QColor(c["text"]))
    p.setColor(QPalette.Button, QColor(c["button"]))
    p.setColor(QPalette.ButtonText, QColor(c["text"]))
    p.setColor(QPalette.BrightText, QColor("#ffffff"))
    p.setColor(QPalette.Highlight, QColor(c["accent"]))
    p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    p.setColor(QPalette.ToolTipBase, QColor(c["tip"]))
    p.setColor(QPalette.ToolTipText, QColor(c["text"]))
    p.setColor(QPalette.PlaceholderText, QColor(c["dim"]))
    p.setColor(QPalette.Link, QColor(c["accent"]))
    p.setColor(QPalette.Mid, QColor(c["border"]))
    p.setColor(QPalette.Dark, QColor(c["border"]))
    p.setColor(QPalette.Light, QColor(c["base"]))
    for role in (QPalette.WindowText, QPalette.Text, QPalette.ButtonText):
        p.setColor(QPalette.Disabled, role, QColor(c["dim"]))
    return p


def build_stylesheet(dark: bool) -> str:
    if dark:
        bg = "#1b1d23"
        bg_elevated = "#22252d"
        bg_card = "#262a33"
        border = "#333844"
        text = "#e7e9ee"
        text_dim = "#9096a3"
        accent = "#7c8cff"
        accent_hover = "#8f9dff"
        danger = "#ff6b6b"
        alt_row = "#1f222a"
        select_bg = "#343b52"
        header_bg = "#20232b"
        tab_bg = "#20232b"
    else:
        bg = "#f4f5f8"
        bg_elevated = "#ffffff"
        bg_card = "#ffffff"
        border = "#e1e3ea"
        text = "#1e2028"
        text_dim = "#666c7a"
        accent = "#5865f2"
        accent_hover = "#6f7bf5"
        danger = "#e5484d"
        alt_row = "#f7f8fb"
        select_bg = "#e4e7ff"
        header_bg = "#eef0f6"
        tab_bg = "#eef0f6"

    return f"""
    QWidget#central {{ background: {bg}; }}
    QMainWindow {{ background: {bg}; }}
    QWidget#bodyWidget {{ background: {bg}; }}

    QLabel {{ color: {text}; font-size: 13px; }}
    QLabel#logoLabel {{ color: {text}; font-size: 17px; font-weight: 700; }}
    QLabel#titleLabel {{ color: {text}; font-size: 18px; font-weight: 700; }}
    QLabel#subtitleLabel {{ color: {text_dim}; font-size: 12px; margin-bottom: 4px; }}
    QLabel#statusLabel {{ color: {text_dim}; font-size: 12px; }}

    QFrame#topBar {{
        background: {bg_elevated};
        border-bottom: 1px solid {border};
    }}
    QFrame#statusBarFrame {{
        background: {bg_elevated};
        border-top: 1px solid {border};
    }}

    QLineEdit, QComboBox, QDateEdit, QTimeEdit, QDoubleSpinBox, QTextEdit {{
        background: {bg_card};
        color: {text};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 7px 10px;
        font-size: 13px;
        selection-background-color: {accent};
    }}
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus,
    QDoubleSpinBox:focus, QTextEdit:focus {{
        border: 1px solid {accent};
    }}
    QLineEdit#searchEdit {{
        padding: 10px 14px;
        font-size: 13px;
        border-radius: 10px;
    }}

    QComboBox::drop-down {{ border: none; width: 22px; }}
    QComboBox QAbstractItemView {{
        background: {bg_card};
        color: {text};
        border: 1px solid {border};
        selection-background-color: {select_bg};
        selection-color: {text};
        outline: none;
    }}

    QDateEdit::drop-down, QTimeEdit::drop-down {{ border: none; width: 22px; }}
    QCalendarWidget QWidget {{ background: {bg_card}; color: {text}; }}
    QCalendarWidget QAbstractItemView:enabled {{
        color: {text}; background: {bg_card}; selection-background-color: {accent};
    }}

    QPushButton#primaryButton, QPushButton#addButton {{
        background: {accent};
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 9px 18px;
        font-size: 13px;
        font-weight: 600;
    }}
    QPushButton#primaryButton:hover, QPushButton#addButton:hover {{ background: {accent_hover}; }}

    QPushButton#secondaryButton, QPushButton#editButton,
    QPushButton#themeButton, QPushButton#exportButton, QPushButton#duplicateButton {{
        background: transparent;
        color: {text};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 9px 16px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton#secondaryButton:hover, QPushButton#editButton:hover,
    QPushButton#themeButton:hover, QPushButton#exportButton:hover,
    QPushButton#duplicateButton:hover {{
        background: {bg_card}; border: 1px solid {accent};
    }}

    QPushButton#dangerButton, QPushButton#deleteButton {{
        background: transparent;
        color: {danger};
        border: 1px solid {danger};
        border-radius: 8px;
        padding: 9px 16px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton#dangerButton:hover, QPushButton#deleteButton:hover {{
        background: {danger}; color: #ffffff;
    }}

    QDialogButtonBox QPushButton {{
        min-width: 100px;
        padding: 8px 16px;
        border-radius: 8px;
        border: 1px solid {border};
        background: {bg_card};
        color: {text};
    }}
    QDialogButtonBox QPushButton:default {{
        background: {accent};
        color: #ffffff;
        border: none;
        font-weight: 600;
    }}
    QDialogButtonBox QPushButton:default:hover {{ background: {accent_hover}; }}

    QDialog {{ background: {bg_elevated}; }}

    QTabWidget#venueTabs::pane {{
        border: 1px solid {border};
        border-radius: 10px;
        background: {bg_card};
        top: -1px;
    }}
    QTabBar::tab {{
        background: {tab_bg};
        color: {text_dim};
        padding: 9px 18px;
        margin-right: 4px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-size: 13px;
        font-weight: 500;
    }}
    QTabBar::tab:selected {{
        background: {accent};
        color: #ffffff;
        font-weight: 600;
    }}
    QTabBar::tab:!selected:hover {{
        background: {select_bg};
        color: {text};
    }}

    QTableWidget {{
        background: {bg_card};
        alternate-background-color: {alt_row};
        color: {text};
        border: none;
        gridline-color: {border};
        font-size: 13px;
    }}
    QTableWidget::item {{
        padding: 8px 6px;
        border: none;
    }}
    QTableWidget::item:selected {{
        background: {select_bg};
        color: {text};
    }}
    QHeaderView::section {{
        background: {header_bg};
        color: {text_dim};
        padding: 10px 6px;
        border: none;
        border-bottom: 1px solid {border};
        font-weight: 600;
        font-size: 12px;
    }}
    QTableCornerButton::section {{ background: {header_bg}; border: none; }}

    QScrollBar:vertical {{
        background: transparent; width: 10px; margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {border}; border-radius: 5px; min-height: 24px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {text_dim}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 0; }}
    QScrollBar::handle:horizontal {{ background: {border}; border-radius: 5px; min-width: 24px; }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

    QMessageBox {{ background: {bg_elevated}; }}
    QMessageBox QLabel {{ color: {text}; }}
    QFileDialog {{ background: {bg_elevated}; color: {text}; }}

    QToolButton {{
        background: {bg_card};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 6px 8px;
        font-size: 14px;
    }}
    QToolButton:hover {{ border: 1px solid {accent}; background: {select_bg}; }}

    QPushButton:disabled {{
        color: {text_dim};
        border: 1px solid {border};
        background: transparent;
    }}

    QMessageBox QPushButton {{
        min-width: 80px;
        padding: 7px 16px;
        border-radius: 8px;
        border: 1px solid {border};
        background: {bg_card};
        color: {text};
    }}
    QMessageBox QPushButton:hover {{ border: 1px solid {accent}; }}
    QMessageBox QPushButton:default {{
        background: {accent};
        color: #ffffff;
        border: none;
        font-weight: 600;
    }}

    QMenu {{
        background: {bg_card};
        color: {text};
        border: 1px solid {border};
        padding: 4px;
    }}
    QMenu::item {{ padding: 6px 22px; border-radius: 6px; }}
    QMenu::item:selected {{ background: {select_bg}; color: {text}; }}
    QMenu::item:disabled {{ color: {text_dim}; }}
    QMenu::separator {{ height: 1px; background: {border}; margin: 4px 6px; }}

    QToolTip {{
        background: {bg_card};
        color: {text};
        border: 1px solid {border};
        padding: 4px 6px;
    }}

    QCalendarWidget QToolButton {{
        background: transparent;
        color: {text};
        border: none;
        padding: 4px 8px;
    }}
    QCalendarWidget QToolButton:hover {{ background: {select_bg}; border-radius: 6px; }}
    QCalendarWidget QMenu {{ background: {bg_card}; color: {text}; }}
    QCalendarWidget QSpinBox {{ background: {bg_card}; color: {text}; }}

    QAbstractScrollArea::corner {{ background: {bg_card}; }}

    QWidget#pickerPopup {{
        background: {bg_elevated};
        border: 1px solid {border};
        border-radius: 12px;
    }}
    QLabel#timePopupLabel {{
        color: {text};
        font-size: 22px;
        font-weight: 700;
    }}
    QDial {{
        background: transparent;
    }}
    """
