"""
Money Tracker — World-Class Design System
Premium Dark Glassmorphism UI Token Library
Designed to top-tier award-winning standards.
"""

# ═══════════════════════════════════════════════════════════
#  Color Tokens
# ═══════════════════════════════════════════════════════════
THEME = {
    # Backgrounds — layered depth system
    "bg_void":    "#08080E",              # deepest void
    "bg_deep":    "#0D0D14",             # app background
    "bg_layer1":  "#13131C",             # panels
    "bg_layer2":  "#1A1A26",             # cards
    "bg_layer3":  "#21212F",             # elevated cards
    "bg_input":   "#17171F",             # input fields
    "bg_glass":   "rgba(24,24,36,0.92)", # glassmorphism

    # Gold accent system
    "accent":       "#FFB800",
    "accent_deep":  "#E09800",
    "accent_glow":  "rgba(255,184,0,0.22)",
    "accent_ultra": "rgba(255,184,0,0.08)",

    # Semantic colors (Chinese convention: income=red, expense=green)
    "income":       "#FF4C5E",
    "income_glow":  "rgba(255,76,94,0.20)",
    "income_soft":  "rgba(255,76,94,0.10)",
    "expense":      "#00D68F",
    "expense_glow": "rgba(0,214,143,0.20)",
    "expense_soft": "rgba(0,214,143,0.10)",

    # Text hierarchy
    "text_p":  "#F0F0F8",    # primary
    "text_s":  "#A0A0B8",    # secondary
    "text_t":  "#606074",    # tertiary
    "text_d":  "#404050",    # disabled

    # Borders
    "border":        "rgba(255,255,255,0.07)",
    "border_bright": "rgba(255,255,255,0.15)",
    "border_gold":   "rgba(255,184,0,0.40)",

    # State colors
    "info":    "#0A84FF",
    "success": "#30D158",
    "danger":  "#FF453A",
}

DARK_THEME = THEME

# Module accent palette (8 vivid colors, each distinct)
MODULE_COLORS = [
    "#FF6B00",  # Amber Flame
    "#00C2E0",  # Neon Cyan
    "#FF3D71",  # Hot Coral
    "#00D68F",  # Emerald
    "#7B61FF",  # Electric Violet
    "#FF6B9D",  # Bubblegum
    "#FFD60A",  # Cyber Yellow
    "#147EFB",  # Royal Blue
]

DEFAULT_ICON = "💰"
INCOME_SOURCES = ["工资", "奖金", "红包", "理财", "副业", "转账", "退款", "其他"]
EXPENSE_SOURCES = ["餐饮", "交通", "购物", "娱乐", "住房", "医疗", "教育", "通讯", "转账", "其他"]

# ═══════════════════════════════════════════════════════════
#  Typography
# ═══════════════════════════════════════════════════════════
FONT_FAMILY = '"SF Pro Display", "Inter", "Segoe UI", "PingFang SC", "Microsoft YaHei UI", sans-serif'
FONT_MONO   = '"JetBrains Mono", "Cascadia Code", "Consolas", monospace'


# ═══════════════════════════════════════════════════════════
#  Main Stylesheet
# ═══════════════════════════════════════════════════════════
def get_theme_stylesheet(theme: dict = None) -> str:
    if theme is None:
        theme = THEME
    t = theme

    return f"""
/* ═══ Global Reset ═══ */
* {{
    font-family: {FONT_FAMILY};
    color: {t['text_p']};
    outline: none;
}}

QMainWindow, QWidget#centralWidget {{
    background-color: {t['bg_deep']};
}}

/* ═══ Tooltips ═══ */
QToolTip {{
    background: #21212F;
    color: #F0F0F8;
    border: 1px solid rgba(255,184,0,0.5);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 600;
}}

/* ═══ Scrollbars — ultra-minimal ═══ */
QScrollBar:vertical {{
    border: none;
    background: transparent;
    width: 5px;
    margin: 4px 0;
}}
QScrollBar::handle:vertical {{
    background: rgba(255,255,255,0.12);
    border-radius: 2px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: {t['accent']};
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0px; }}

QScrollBar:horizontal {{
    border: none;
    background: transparent;
    height: 5px;
    margin: 0 4px;
}}
QScrollBar::handle:horizontal {{
    background: rgba(255,255,255,0.12);
    border-radius: 2px;
    min-width: 24px;
}}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{ width: 0px; }}

/* ═══ QListWidget — clean container ═══ */
QListWidget {{
    background: transparent;
    border: none;
    outline: none;
}}
QListWidget::item {{
    background: transparent;
    border: none;
    padding: 2px;
}}
QListWidget::item:selected {{
    background: transparent;
    border: none;
}}
QListWidget::item:hover {{
    background: transparent;
}}

/* ═══ Module List (Sidebar) ═══ */
QListWidget#moduleList {{
    padding: 4px 0;
}}
QListWidget#moduleList::item {{
    background: rgba(255,255,255,0.03);
    border: 1px solid {t['border']};
    border-radius: 12px;
    padding: 11px 14px;
    margin-bottom: 6px;
    color: {t['text_s']};
    font-size: 13px;
    font-weight: 500;
}}
QListWidget#moduleList::item:hover {{
    background: rgba(255,255,255,0.07);
    border-color: {t['border_bright']};
    color: {t['text_p']};
}}
QListWidget#moduleList::item:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {t['accent']}22, stop:1 {t['accent']}11);
    border: 1px solid {t['border_gold']};
    color: {t['accent']};
    font-weight: 700;
}}
QListWidget#moduleList::item:selected:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {t['accent']}33, stop:1 {t['accent']}18);
}}

/* ═══ Global Input Fields ═══ */
QLineEdit {{
    background: {t['bg_input']};
    border: 1px solid {t['border']};
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 14px;
    color: {t['text_p']};
    selection-background-color: {t['accent']}55;
}}
QLineEdit:focus {{
    border: 1px solid {t['border_gold']};
    background: {t['bg_layer2']};
}}
QLineEdit:hover:!focus {{
    border-color: {t['border_bright']};
}}

/* ═══ Global Buttons ═══ */
QPushButton {{
    background: {t['bg_layer2']};
    border: 1px solid {t['border']};
    border-radius: 10px;
    padding: 9px 18px;
    font-size: 13px;
    font-weight: 600;
    color: {t['text_s']};
}}
QPushButton:hover {{
    background: {t['bg_layer3']};
    border-color: {t['border_bright']};
    color: {t['text_p']};
}}
QPushButton:pressed {{
    background: {t['bg_layer1']};
}}
QPushButton#primaryButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {t['accent']}, stop:1 {t['accent_deep']});
    color: #000000;
    border: none;
    font-weight: 700;
}}
QPushButton#primaryButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #FFC533, stop:1 {t['accent']});
}}

/* ═══ Balance Card ═══ */
QFrame#balanceCard {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1C1C28, stop:0.5 #16162000, stop:1 #0F0F18);
    border: 1px solid {t['border_gold']};
    border-radius: 22px;
}}

/* ═══ Summary / Glass Cards ═══ */
QFrame#summaryCard {{
    background: {t['bg_glass']};
    border: 1px solid {t['border_bright']};
    border-radius: 22px;
}}
"""


MAIN_STYLESHEET = get_theme_stylesheet(THEME)

# ═══════════════════════════════════════════════════════════
#  Dialog Stylesheet (for popups)
# ═══════════════════════════════════════════════════════════
DIALOG_STYLESHEET = f"""
QFrame#summaryCard {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #16161E, stop:1 #0D0D14);
    border: 1px solid {THEME['border_gold']};
    border-radius: 24px;
}}
QLabel {{
    color: {THEME['text_p']};
    background: transparent;
}}
QLineEdit {{
    background: {THEME['bg_input']};
    border: 1px solid {THEME['border']};
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 15px;
    color: {THEME['text_p']};
    selection-background-color: {THEME['accent']}55;
}}
QLineEdit:focus {{
    border-color: {THEME['border_gold']};
    background: {THEME['bg_layer2']};
}}
QPushButton {{
    background: {THEME['bg_layer2']};
    border-radius: 14px;
    padding: 12px;
    font-weight: 700;
    color: {THEME['text_s']};
    border: 1px solid {THEME['border']};
}}
QPushButton:hover {{
    background: {THEME['bg_layer3']};
    border-color: {THEME['border_bright']};
    color: {THEME['text_p']};
}}
QComboBox {{
    background: {THEME['bg_input']};
    border: 1px solid {THEME['border']};
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 15px;
    color: {THEME['text_p']};
}}
QComboBox:focus {{
    border-color: {THEME['border_gold']};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background: {THEME['bg_layer2']};
    border: 1px solid {THEME['border_bright']};
    border-radius: 8px;
    color: {THEME['text_p']};
    selection-background-color: {THEME['accent']}33;
}}
"""
