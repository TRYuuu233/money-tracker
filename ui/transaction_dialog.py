"""
Money Tracker — Transaction Dialog
Clean, properly-structured dialog using the same layout approach as module_dialog.
No manual setGeometry, no animation gap that bleeds underlying widgets through.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QDoubleValidator

from .styles import INCOME_SOURCES, EXPENSE_SOURCES, THEME
from .effects import shake_widget
from common.locale import L
from PyQt6.QtCore import pyqtSignal


class _CloseButton(QFrame):
    """Reliable × close button using Python-driven hover (avoids CSS :hover rendering bug)."""
    clicked = pyqtSignal()

    _BG_NORM  = "#C0392B"
    _BG_HOVER = "#E74C3C"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(34, 34)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self._lbl = QLabel("✕")
        self._lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self._lbl)
        self._set_hover(False)

    def _set_hover(self, hovered: bool):
        bg = self._BG_HOVER if hovered else self._BG_NORM
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border-radius: 10px;
            }}
        """)
        self._lbl.setStyleSheet(
            "font-size: 18px; font-weight: 900; color: #FFFFFF;"
            " background: transparent; border: none;"
        )

    def enterEvent(self, event):
        self._set_hover(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._set_hover(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class TransactionDialog(QDialog):
    """
    Income / expense recording dialog.
    Uses proper outer QVBoxLayout on self (same as module_dialog/settings_dialog)
    so no transparency gap ever exposes the underlying main window.
    """

    def __init__(self, trans_type: str = "income",
                 module_name: str = "", parent=None):
        super().__init__(parent)
        self.trans_type  = trans_type
        self.module_name = module_name
        self._setup_ui()

    def _setup_ui(self):
        t = THEME
        is_income = self.trans_type == "income"
        accent    = t["income"]   if is_income else t["expense"]
        accent_bg = t["income_soft"] if is_income else t["expense_soft"]
        title_txt = L("tx_income_title") if is_income else L("tx_expense_title")
        type_icon = "↗" if is_income else "↙"

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedWidth(420)

        # ── Proper outer layout on self ───────────────────────────
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("txCard")
        card.setStyleSheet(f"""
            QFrame#txCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #18181F, stop:1 #0F0F15);
                border: 1px solid {accent}44;
                border-radius: 26px;
            }}
        """)
        outer.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(36, 32, 36, 32)
        layout.setSpacing(20)

        # ── Header ────────────────────────────────────────────────
        header = QHBoxLayout()

        icon_badge = QLabel(type_icon)
        icon_badge.setFixedSize(44, 44)
        icon_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_badge.setStyleSheet(f"""
            QLabel {{
                background: {accent_bg};
                color: {accent};
                border: 1px solid {accent}44;
                border-radius: 14px;
                font-size: 22px; font-weight: 900;
            }}
        """)
        header.addWidget(icon_badge)
        header.addSpacing(14)

        title_stack = QVBoxLayout()
        title_stack.setSpacing(2)
        title_lbl = QLabel(title_txt)
        title_lbl.setStyleSheet(
            f"font-size:22px; font-weight:800; color:{accent}; background:transparent;"
        )
        title_stack.addWidget(title_lbl)

        if self.module_name:
            sub_lbl = QLabel(f"{L('ledger_label')}{self.module_name}")
            sub_lbl.setStyleSheet("font-size:12px; color:#606074; background:transparent;")
            title_stack.addWidget(sub_lbl)

        header.addLayout(title_stack)
        header.addStretch()

        # Close button — Python-driven hover (avoids CSS :hover rendering bug on Windows)
        close_btn = _CloseButton(parent=self)
        close_btn.clicked.connect(self.reject)
        header.addWidget(close_btn)
        layout.addLayout(header)

        # ── Amount input ──────────────────────────────────────────
        amt_cap = QLabel(L("amount_caption"))
        amt_cap.setStyleSheet(
            "font-size:10px; font-weight:700; letter-spacing:1.5px; color:#404050; background:transparent;"
        )
        layout.addWidget(amt_cap)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setValidator(QDoubleValidator(0, 999_999_999, 2))
        self.amount_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.amount_input.setStyleSheet(f"""
            QLineEdit {{
                font-size: 40px; font-weight: 800;
                color: {accent};
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 14px;
                padding: 14px 18px;
                min-height: 72px;
            }}
            QLineEdit:focus {{
                border: 1.5px solid {accent}88;
                background: rgba(255,255,255,0.05);
            }}
        """)
        layout.addWidget(self.amount_input)

        # ── Category combo ────────────────────────────────────────
        cat_cap = QLabel(L("category_caption"))
        cat_cap.setStyleSheet(
            "font-size:10px; font-weight:700; letter-spacing:1.5px; color:#404050; background:transparent;"
        )
        layout.addWidget(cat_cap)

        self.source_combo = QComboBox()
        self.source_combo.setEditable(True)
        sources = INCOME_SOURCES if self.trans_type == "income" else EXPENSE_SOURCES
        self.source_combo.addItems([""] + sources)
        self.source_combo.lineEdit().setPlaceholderText(L("category_placeholder"))
        self.source_combo.setStyleSheet(f"""
            QComboBox {{
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 15px; color: #F0F0F8;
                min-height: 20px;
            }}
            QComboBox:focus {{ border-color: {accent}66; }}
            QComboBox::drop-down {{ border:none; width:28px; }}
            QComboBox QAbstractItemView {{
                background: #1A1A26;
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 8px; color: #F0F0F8;
                selection-background-color: {accent}33;
            }}
        """)
        layout.addWidget(self.source_combo)

        layout.addSpacing(8)

        # ── Buttons ───────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(14)

        btn_cancel = QPushButton(L("btn_cancel"))
        btn_cancel.setFixedHeight(52)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.04);
                color: #606074;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 15px;
                font-size:15px; font-weight:600;
            }
            QPushButton:hover { background:rgba(255,255,255,0.09); color:#A0A0B8; }
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton(L("btn_confirm"))
        btn_save.setFixedHeight(52)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {accent}, stop:1 {accent}BB);
                color: #000; border: none;
                border-radius: 15px;
                font-size: 15px; font-weight: 800;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {accent}EE, stop:1 {accent});
            }}
        """)
        btn_save.clicked.connect(self._on_save)

        btn_row.addWidget(btn_cancel, 1)
        btn_row.addWidget(btn_save, 2)
        layout.addLayout(btn_row)

        # Enter key shortcuts
        self.amount_input.returnPressed.connect(self._on_save)
        if self.source_combo.lineEdit():
            self.source_combo.lineEdit().returnPressed.connect(self._on_save)

        # Auto-focus amount after showing
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(50, self.amount_input.setFocus)

    def _on_save(self):
        txt = self.amount_input.text().replace(",", "").strip()
        try:
            if not txt or float(txt) <= 0:
                raise ValueError
            self.accept()
        except ValueError:
            shake_widget(self.amount_input)
            self.amount_input.setFocus()

    def get_result(self):
        amount = float(self.amount_input.text().replace(",", "") or 0)
        source = self.source_combo.currentText().strip()
        return amount, source
