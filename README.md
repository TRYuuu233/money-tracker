# ✦ Lumis — Smart Finance Tracker Pro
### 💰 The most beautiful open-source personal finance app for Windows

> *Dark glassmorphism UI · Animated real-time analytics · 100% offline · Bilingual ZH/EN*  
> *深色玻璃拟态 UI · 实时动态数据分析 · 完全本地离线 · 中英双语*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![PyQt6](https://img.shields.io/badge/UI-PyQt6-41CD52?logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)](https://github.com/TRYuuu233/money-tracker/releases)
[![Stars](https://img.shields.io/github/stars/TRYuuu233/money-tracker?style=social)](https://github.com/TRYuuu233/money-tracker)

<div align="center">
  <h3>🌍 Official Websites / 官方主页</h3>
  <a href="https://TRYuuu233.github.io/money-tracker/"><b>English Website (GitHub Pages)</b></a> &nbsp;|&nbsp;
  <a href="https://rainbow-cajeta-646fb8.netlify.app/"><b>中文引流官网 (Netlify)</b></a>
</div>

---

## 🏆 Why This App Crushes Every Other Finance Tracker / 为什么选它

Most open-source money trackers look like Excel spreadsheets from 2003.  
大多数开源记账软件看起来像2003年的Excel表格。

**Lumis is different.**  
**Lumis 不一样。**

| Others / 其他应用 | Lumis ✦ |
|---|---|
| 💀 Plain white / gray UI | ✨ Animated dark glassmorphism |
| 📊 Static numbers | 🔢 Smooth animated number transitions |
| 🌐 Browser-based (slow, needs internet) | 🖥️ Native desktop, 100% offline |
| 🔒 Your data goes to the cloud | 🔐 All data stays on your machine |
| 💸 Subscription / ads | 🆓 Free, open-source, MIT license |
| 🇨🇳 Only one language | 🌐 Chinese + English, built-in |
| 🐢 Slow to load | ⚡ Instant start, no web overhead |

---

## ✨ Features / 核心功能

- **📚 Multi-Ledger System** — Create unlimited named ledger books, each with its own icon, color, and balance  
  多账本体系 — 无限创建账本，各自独立余额、图标和颜色

- **↗↙ Income & Expense Tracking** — Record transactions with categories and custom notes  
  收支记账 — 分类标签与自定义备注，秒速记录

- **🔍 Sort & Filter** — Filter by All / Income / Expense; sort by Date or Amount, Asc / Desc   
  排序筛选 — 按全部/收入/支出筛选，按日期或金额升降序排列

- **📊 Real-time Analytics Dashboard** — Animated net worth hero card with per-ledger breakdown  
  实时数据分析 — 动画净资产卡片，每本账精细拆分，添加交易即刻更新

- **🔍 Global Search** — Instantly search across all ledger books simultaneously  
  全局搜索 — 跨所有账本实时搜索交易记录

- **🌐 Bilingual UI** — Switch between Chinese and English in Settings  
  双语界面 — 系统设置中一键切换中/英文

- **🔐 Password Protection** — Optional startup password lock  
  密码保护 — 可选启动密码，保护财务隐私

- **📤 Excel Export** — Export any ledger to a beautifully formatted `.xlsx` file  
  导出Excel — 一键将账本导出为格式精美的xlsx文件

- **🎨 Glassmorphism Dark UI** — Animated numbers, smooth transitions, glow effects  
  玻璃拟态深色 UI — 动态数字、平滑过渡、发光特效

---

## 🆕 v1.0.0 Release Notes / 发行说明

**New in this release / 本版本新功能:**

- Sort & type-filter bar inside every ledger (Date/Amount · Asc/Desc · All/Income/Expense)    
  账本内置排序+筛选栏（日期/金额 · 升序/降序 · 全部/收入/支出）  
- Precise amount tooltips — hover "1.2万" → see exact "12,345.67"  
  精确金额提示 — 悬停简写金额即显示完整精确数值
- Analytics real-time update on every transaction change  
  每次记账/删除后数据分析面板即时刷新
- Red background white ✕ close buttons in all dialogs  
  所有弹窗红底白字 ✕ 关闭按钮，清晰显眼
- Bilingual ZH / EN support with language selector in Settings  
  系统设置支持中英双语切换
- Developer info & version shown in Settings → About  
  设置页显示开发者信息和版本号

---

## 🚀 Quick Start / 快速开始

### Requirements / 环境要求

| Package | Version |
|---|---|
| Python | 3.11+ |
| PyQt6 | 6.4+ |
| openpyxl | 3.1+ |

```bash
# Install / 安装依赖
pip install PyQt6 openpyxl

# Run / 运行
python main.py
```

**Or download the pre-built `.exe` from [Releases](https://github.com/TRYuuu233/money-tracker/releases).**  
**或直接从 [Releases](https://github.com/TRYuuu233/money-tracker/releases) 下载编译好的 `.exe` 文件。**

---

## 🌐 Internationalization / 多语言支持

Want to add Japanese, Korean, or another language? It's one file!  
想加日语、韩语等新语言？只需修改一个文件！

See [CONTRIBUTING.md](CONTRIBUTING.md) for the detailed guide.  
详细指南见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📁 Project Structure / 项目结构

```
money-tracker/
├── main.py                    # Entry point / 入口
├── common/
│   ├── database.py            # SQLite data layer / 数据层
│   ├── locale.py              # i18n string system / 多语言系统
│   └── security.py            # Password manager / 密码管理
└── ui/
    ├── main_window.py         # Main window + ledger panel / 主窗口+账本面板
    ├── summary_panel.py       # Analytics dashboard / 分析看板
    ├── transaction_dialog.py  # Add transaction dialog / 添加交易弹窗
    ├── module_dialog.py       # Ledger create/edit dialog / 账本弹窗
    ├── settings_dialog.py     # Settings (language, password, shortcuts) / 设置
    ├── animated_number.py     # Animated number labels / 动态数字
    ├── effects.py             # Visual effects / 视觉特效
    └── styles.py              # Design tokens / 设计变量
```

---

## 🤝 Contributing / 参与贡献

All improvements welcome via **Pull Request** — requires review before merge.  
欢迎通过 **Pull Request** 贡献改进，需审核后合并。

Great contribution ideas / 欢迎的贡献类型:
- 🌐 New language packs (Japanese, Korean, Spanish…) / 新语言包
- 🐛 Bug fixes / 问题修复
- ✨ New features / 新功能
- 🎨 UI polish / 界面优化

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License / 许可证

[MIT](LICENSE) — Free to use, modify, distribute. Attribution appreciated.  
MIT 协议 — 可自由使用、修改、分发，欢迎署名致谢。

---

<div align="center">

**Made with ❤️ by [TRYuuu233](https://github.com/TRYuuu233)**

*If this project helped you, please consider giving it a ⭐ — it helps others discover it!*  
*如果这个项目对你有帮助，请点个 ⭐ — 让更多人发现它！*

</div>
