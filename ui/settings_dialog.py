"""
Money Tracker — Settings Dialog
Clean dark-themed settings: password management + shortcut key configuration.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QLineEdit, QKeySequenceEdit, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QSettings, QTimer
from PyQt6.QtGui import QKeySequence

from .styles import THEME
from common.locale import L, get_lang, set_lang


class SettingsDialog(QDialog):
    """
    Settings dialog.
    Accepts (security_manager, parent) for compatibility with _open_settings call.
    """

    def __init__(self, security=None, parent=None):
        super().__init__(parent)
        from common.security import SecurityManager
        self.security = security if security is not None else SecurityManager()
        self.settings = QSettings("MoneyTracker", "Shortcuts")
        self._setup_ui()

    def _setup_ui(self):
        t = THEME
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedWidth(480)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("settingsCard")
        card.setStyleSheet(f"""
            QFrame#settingsCard {{
                background: {t['bg_layer1']};
                border: 1px solid {t['border_bright']};
                border-radius: 24px;
            }}
        """)
        outer.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # ── Title ──────────────────────────────────────────────
        title_row = QHBoxLayout()
        title = QLabel(L("settings_title"))
        title.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {t['text_p']}; background: transparent;")
        title_row.addWidget(title)
        title_row.addStretch()
        layout.addLayout(title_row)

        # ── Divider ────────────────────────────────────────────
        layout.addWidget(self._divider())

        # ── Shortcut Section ───────────────────────────────────
        sc_label = QLabel(L("shortcut_section"))
        sc_label.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {t['accent']}; letter-spacing: 1px; background: transparent;")
        layout.addWidget(sc_label)

        sc_hint = QLabel(L("shortcut_hint"))
        sc_hint.setStyleSheet(f"font-size: 12px; color: {t['text_t']}; background: transparent;")
        layout.addWidget(sc_hint)

        # Shortcut rows
        sc_grid = QVBoxLayout()
        sc_grid.setSpacing(10)

        self.key_income_edit, income_row = self._shortcut_row(
            L("shortcut_income"), "key_income", "Z", t
        )
        self.key_expense_edit, expense_row = self._shortcut_row(
            L("shortcut_expense"), "key_expense", "X", t
        )
        sc_grid.addLayout(income_row)
        sc_grid.addLayout(expense_row)
        layout.addLayout(sc_grid)

        # ── Divider ────────────────────────────────────────────
        layout.addWidget(self._divider())

        # ── Password Section ───────────────────────────────────
        pwd_label = QLabel("🔐  密码保护")
        pwd_label.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {t['accent']}; letter-spacing: 1px; background: transparent;")
        layout.addWidget(pwd_label)

        has_pwd = self.security.has_password()

        if has_pwd:
            status = QLabel(L("pwd_set"))
        else:
            status = QLabel(L("pwd_not_set"))
        status.setStyleSheet(f"font-size: 13px; color: {t['text_s']}; background: transparent;")
        layout.addWidget(status)

        pwd_btn_row = QHBoxLayout()
        pwd_btn_row.setSpacing(10)

        if has_pwd:
            btn_change = self._action_btn(L("btn_change_pwd"), t['accent'])
            btn_change.clicked.connect(self._change_password)
            pwd_btn_row.addWidget(btn_change)

            btn_remove = self._action_btn(L("btn_remove_pwd"), t['danger'])
            btn_remove.clicked.connect(self._remove_password)
            pwd_btn_row.addWidget(btn_remove)
        else:
            btn_set = self._action_btn(L("btn_set_pwd"), t['accent'])
            btn_set.clicked.connect(self._set_password)
            pwd_btn_row.addWidget(btn_set)

        layout.addLayout(pwd_btn_row)

        # ── Language Section ─────────────────────────────
        layout.addWidget(self._divider())
        lang_label = QLabel(L("language_section"))
        lang_label.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {t['accent']}; letter-spacing: 1px; background: transparent;")
        layout.addWidget(lang_label)

        lang_row = QHBoxLayout()
        lang_row.setSpacing(12)
        lang_group = QButtonGroup(self)

        def _lang_radio(text, code):
            rb = QRadioButton(text)
            rb.setChecked(get_lang() == code)
            rb.setStyleSheet(f"""
                QRadioButton {{
                    color: {t['text_s']}; font-size: 13px; background: transparent;
                }}
                QRadioButton::indicator {{
                    width: 16px; height: 16px;
                    border-radius: 8px;
                    border: 2px solid {t['border_bright']};
                    background: transparent;
                }}
                QRadioButton::indicator:checked {{
                    background: {t['accent']};
                    border-color: {t['accent']};
                }}
            """)
            rb.toggled.connect(lambda checked, c=code: set_lang(c) if checked else None)
            lang_group.addButton(rb)
            lang_row.addWidget(rb)

        _lang_radio("中文", "zh")
        _lang_radio("English", "en")
        lang_row.addStretch()
        layout.addLayout(lang_row)

        lang_hint = QLabel(L("lang_restart_hint"))
        lang_hint.setStyleSheet(f"font-size: 11px; color: {t['text_t']}; background: transparent;")
        layout.addWidget(lang_hint)

        # ── About / Developer Section ─────────────────────
        layout.addWidget(self._divider())
        about_label = QLabel(L("about_section"))
        about_label.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {t['accent']}; letter-spacing: 1px; background: transparent;")
        layout.addWidget(about_label)

        about_grid = QVBoxLayout()
        about_grid.setSpacing(4)

        def _about_row(key_txt, val_txt):
            row = QHBoxLayout()
            k = QLabel(key_txt)
            k.setStyleSheet(f"font-size: 12px; color: {t['text_t']}; background: transparent; min-width: 90px;")
            v = QLabel(val_txt)
            v.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {t['text_s']}; background: transparent;")
            row.addWidget(k)
            row.addWidget(v)
            row.addStretch()
            return row

        about_grid.addLayout(_about_row(L("developer_label") + " :", L("developer_name")))
        about_grid.addLayout(_about_row(L("version_label") + " :", L("version_value")))
        layout.addLayout(about_grid)

        # ── Save + Done buttons ───────────────────────────────
        layout.addWidget(self._divider())
        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_cancel = QPushButton(L("btn_cancel"))
        btn_cancel.setFixedHeight(50)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background: {t['bg_layer2']}; color: {t['text_s']};
                border: 1px solid {t['border']}; border-radius: 14px;
                font-size: 14px; font-weight: 600;
            }}
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton(L("btn_save_close"))
        btn_save.setFixedHeight(50)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {t['accent']}, stop:1 {t['accent_deep']});
                color: #000; border: none; border-radius: 14px;
                font-size: 15px; font-weight: 800;
            }}
        """)
        btn_save.clicked.connect(self._save_and_close)

        btn_row.addWidget(btn_cancel, 1)
        btn_row.addWidget(btn_save, 2)
        layout.addLayout(btn_row)

    def _shortcut_row(self, label_txt: str, settings_key: str, default_key: str, t: dict):
        """Create a labeled shortcut key input row. Returns (QKeySequenceEdit, QHBoxLayout)."""
        row = QHBoxLayout()
        row.setSpacing(12)

        lbl = QLabel(label_txt)
        lbl.setStyleSheet(f"font-size: 14px; color: {t['text_s']}; background: transparent;")
        lbl.setFixedWidth(160)
        row.addWidget(lbl)

        saved_key = self.settings.value(settings_key, default_key)
        edit = QKeySequenceEdit(QKeySequence(saved_key))
        edit.setFixedHeight(44)
        edit.setStyleSheet(f"""
            QKeySequenceEdit {{
                background: {t['bg_input']};
                border: 1.5px solid {t['border']};
                border-radius: 12px;
                padding: 0 14px;
                font-size: 16px; font-weight: 700;
                color: {t['accent']};
            }}
            QKeySequenceEdit:focus {{ border-color: {t['accent']}; }}
        """)

        row.addWidget(edit, 1)

        # Reset button
        btn_reset = QPushButton(f"默认 [{default_key}]")
        btn_reset.setFixedHeight(44)
        btn_reset.setFixedWidth(100)
        btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reset.setStyleSheet(f"""
            QPushButton {{
                background: {t['bg_layer2']}; color: {t['text_s']};
                border: 1px solid {t['border']}; border-radius: 12px;
                font-size: 12px; font-weight: 600;
            }}
            QPushButton:hover {{ color: {t['text_p']}; }}
        """)
        btn_reset.clicked.connect(lambda: edit.setKeySequence(QKeySequence(default_key)))
        row.addWidget(btn_reset)

        return edit, row

    def _save_and_close(self):
        """Save all settings and accept the dialog."""
        # Save shortcuts
        income_seq = self.key_income_edit.keySequence()
        expense_seq = self.key_expense_edit.keySequence()
        if not income_seq.isEmpty():
            self.settings.setValue("key_income", income_seq.toString())
        if not expense_seq.isEmpty():
            self.settings.setValue("key_expense", expense_seq.toString())
        self.settings.sync()
        self.accept()

    def _divider(self):
        t = THEME
        d = QFrame()
        d.setFixedHeight(1)
        d.setStyleSheet(f"background: {t['border']}; border: none;")
        return d

    def _action_btn(self, text: str, color: str):
        t = THEME
        btn = QPushButton(text)
        btn.setFixedHeight(44)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {color}22;
                color: {color};
                border: 1px solid {color}55;
                border-radius: 12px; font-size: 14px; font-weight: 700;
            }}
            QPushButton:hover {{ background: {color}33; }}
        """)
        return btn

    def _password_input_dialog(self, prompt: str):
        """Show a styled dark password input dialog."""
        t = THEME
        dlg = QDialog(self)
        dlg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        dlg.setModal(True)
        dlg.setFixedWidth(380)

        outer = QVBoxLayout(dlg)
        outer.setContentsMargins(0, 0, 0, 0)
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {t['bg_layer2']};
                border: 1px solid {t['border_bright']};
                border-radius: 20px;
            }}
        """)
        outer.addWidget(card)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(16)

        lbl = QLabel(prompt)
        lbl.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {t['text_p']}; background: transparent;")
        lbl.setWordWrap(True)
        lay.addWidget(lbl)

        inp = QLineEdit()
        inp.setEchoMode(QLineEdit.EchoMode.Password)
        inp.setFixedHeight(48)
        inp.setPlaceholderText("输入密码…")
        inp.setStyleSheet(f"""
            QLineEdit {{
                background: {t['bg_input']};
                border: 1.5px solid {t['border']};
                border-radius: 12px;
                padding: 0 16px;
                font-size: 16px;
                color: {t['text_p']};
            }}
            QLineEdit:focus {{ border-color: {t['accent']}; }}
        """)
        lay.addWidget(inp)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_ok = QPushButton("确 认")
        btn_ok.setFixedHeight(44)
        btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ok.setStyleSheet(f"""
            QPushButton {{
                background: {t['accent']}; color: #000;
                border: none; border-radius: 12px; font-size: 14px; font-weight: 800;
            }}
        """)
        btn_ok.clicked.connect(dlg.accept)
        inp.returnPressed.connect(dlg.accept)

        btn_cancel = QPushButton("取 消")
        btn_cancel.setFixedHeight(44)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background: {t['bg_layer3']}; color: {t['text_s']};
                border: 1px solid {t['border']}; border-radius: 12px; font-size: 14px;
            }}
        """)
        btn_cancel.clicked.connect(dlg.reject)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)
        lay.addLayout(btn_row)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            return inp.text()
        return None

    def _set_password(self):
        t = THEME
        pwd = self._password_input_dialog("请设置新密码（至少4位）：")
        if pwd is None:
            return
        if len(pwd) < 4:
            self._show_dark_info("密码过短", "密码至少需要4位字符。")
            return
        pwd2 = self._password_input_dialog("请再次输入密码确认：")
        if pwd2 is None:
            return
        if pwd != pwd2:
            self._show_dark_info("密码不一致", "两次输入的密码不匹配，请重试。")
            return
        self.security.set_password(pwd)
        self._show_dark_info("设置成功", "密码已设置，下次启动时将要求验证。")
        self.accept()

    def _change_password(self):
        old = self._password_input_dialog("请先输入当前密码验证：")
        if old is None:
            return
        if not self.security.verify_password(old):
            self._show_dark_info("验证失败", "当前密码不正确。")
            return
        self._set_password()

    def _remove_password(self):
        old = self._password_input_dialog("请输入当前密码以确认移除：")
        if old is None:
            return
        if not self.security.verify_password(old):
            self._show_dark_info("验证失败", "当前密码不正确。")
            return
        self.security.remove_password()
        self._show_dark_info("已移除", "密码已取消，下次启动将直接进入。")
        self.accept()

    def _show_dark_info(self, title: str, text: str):
        t = THEME
        dlg = QDialog(self)
        dlg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        dlg.setModal(True)
        dlg.setFixedWidth(360)

        outer = QVBoxLayout(dlg)
        outer.setContentsMargins(0, 0, 0, 0)
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {t['bg_layer2']};
                border: 1px solid {t['border_bright']};
                border-radius: 18px;
            }}
        """)
        outer.addWidget(card)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"font-size: 17px; font-weight: 800; color: {t['text_p']}; background: transparent;")
        lay.addWidget(lbl_title)

        lbl_text = QLabel(text)
        lbl_text.setStyleSheet(f"font-size: 14px; color: {t['text_s']}; background: transparent;")
        lbl_text.setWordWrap(True)
        lay.addWidget(lbl_text)

        btn_ok = QPushButton("知 道 了")
        btn_ok.setFixedHeight(44)
        btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ok.setStyleSheet(f"""
            QPushButton {{
                background: {t['accent']}; color: #000;
                border: none; border-radius: 12px; font-size: 14px; font-weight: 800;
            }}
        """)
        btn_ok.clicked.connect(dlg.accept)
        lay.addWidget(btn_ok)
        dlg.exec()
