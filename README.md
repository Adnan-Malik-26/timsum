<div align="center">

# ⏰ TimSum

*Beautiful Timewarrior summaries in your terminal*

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Rich](https://img.shields.io/badge/powered%20by-Rich-ff69b4?style=for-the-badge)](https://github.com/Textualize/rich)

**Transform your time tracking data into stunning, colorful terminal displays**

[Installation](#-installation) • [Usage](#-usage) • [Themes](#-custom-themes) • [Contributing](#-contributing)

---

</div>

## ✨ Features

<table>
<tr>
<td>

🚀 **Lightning Fast**  
Terminal-native performance with instant summaries

🎨 **Beautiful Themes**  
Catppuccin palettes + unlimited custom themes

⏱ **Flexible Ranges**  
From daily snapshots to complete history

</td>
<td>

💻 **Clean Installation**  
Isolated virtual environment, zero conflicts

🎯 **Consistent Colors**  
Tags maintain colors across all views

📊 **Rich Formatting**  
Elegant tables powered by Rich library

</td>
</tr>
</table>

---

## 🚀 Installation

### 🏠 Local Installation *(Recommended)*

Perfect for personal use - installs in your home directory without touching system files.

```bash
git clone https://github.com/yourusername/timsum.git
cd timsum
bash install.sh
```

> 💡 **Pro tip**: The installer will guide you through local vs system-wide options

### 🌐 System-Wide Installation

For system administrators or multi-user setups.

```bash
git clone https://github.com/yourusername/timsum.git
cd timsum
sudo bash install.sh
```

### 📝 PATH Setup

Add to your shell configuration (`~/.bashrc` or `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## 🎮 Usage

### Quick Start

```bash
# Weekly summary with Mocha theme
timsum --theme mocha --range :week

# Monthly overview with custom theme
timsum --theme kanagawa --range :month

# Complete history with Latte theme
timsum --theme latte --range :all
```

### 🎛 Command Options

| Option | Description | Examples |
|--------|-------------|----------|
| `--theme` | Color theme | `mocha`, `latte`, `frappe`, `macchiato`, `kanagawa` |
| `--range` | Time period | `:day`, `:week`, `:month`, `:all` |

---

## ⚙️ Configuration

### 📄 Config File

TimSum reads configuration from:

| Installation | Config Path |
|--------------|-------------|
| **Local** | `~/.config/timsum/timsum.conf` |
| **System** | `/etc/timsum/timsum.conf` |

**Example configuration:**
```ini
[timsum]
theme = mocha
range = :week
```

> 🔄 **Override**: Command-line arguments always take precedence

---

## 🎨 Custom Themes

### 🎪 Built-in Themes
> There are 22 Built-in themes but you can add your own. (See Below)

### 🎭 Create Your Own

**1. Choose your theme directory:**

| Installation | Theme Directory |
|--------------|-----------------|
| **Local** | `~/.config/timsum/themes/` |
| **System** | `/etc/timsum/themes/` |

**2. Create a JSON theme file:**

```json
{
  "base": "#1f1f28",      // Background color
  "text": "#dcd7ba",      // Primary text
  "accent": "#7e9cd8",    // Headers & totals  
  "highlight": "#ff9e3b"  // Emphasis & highlights
}
```

**3. Save and use:**

```bash
# Save as ~/.config/timsum/themes/mytheme.json
timsum --theme mytheme --range :week
```

### 🌸 Example: Kanagawa Theme

```bash
# Create the theme
cat > ~/.config/timsum/themes/kanagawa.json << 'EOF'
{
  "base": "#1f1f28",
  "text": "#dcd7ba",
  "accent": "#7e9cd8",
  "highlight": "#ff9e3b"
}
EOF

# Use it immediately
timsum --theme kanagawa --range :month
```

---

## 🛠 Development

### 🏗 Setup

```bash
git clone https://github.com/yourusername/timsum.git
cd timsum

# Create development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
python timsum.py --theme mocha --range :week
```

### 🧪 Testing

```bash
# Test with different themes
python timsum.py --theme latte --range :day
python timsum.py --theme frappe --range :month
python timsum.py --theme macchiato --range :all
```

---

## 🤝 Contributing

We love contributions! Here's how to get started:

### 🐛 Found a Bug?
[Open an issue](https://github.com/yourusername/timsum/issues) with details and steps to reproduce.

### 💡 Have an Idea?
[Start a discussion](https://github.com/yourusername/timsum/discussions) about new features.

### 🔧 Ready to Code?

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to your branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

> 📋 **Style Guide**: We follow [PEP 8](https://peps.python.org/pep-0008/) for Python code

---

## 📚 Roadmap

### ✅ Completed
- [x] Config file support
- [x] Custom theme system  
- [x] Consistent tag coloring
- [x] Virtual environment installation

### 🚧 In Progress
- [ ] 📊 Export to CSV/JSON
- [ ] 🖥 Interactive TUI mode

---

## 📜 License

Released under the **MIT License** - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

<div align="center">

**Built with amazing open-source projects**

[![Rich](https://img.shields.io/badge/Rich-Terminal%20Formatting-ff69b4?style=flat-square)](https://github.com/Textualize/rich)
[![Catppuccin](https://img.shields.io/badge/Catppuccin-Color%20Palettes-fab387?style=flat-square)](https://github.com/catppuccin/catppuccin)
[![Timewarrior](https://img.shields.io/badge/Timewarrior-Time%20Tracking-89b4fa?style=flat-square)](https://timewarrior.net/)

*Inspired by terminal productivity tools like `tldr`, `glances`, and `bat`*

</div>

---

<div align="center">

**Made with ❤️ for the terminal**

[⬆ Back to top](#-timsum)

</div>
