# Timsum
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
**TimSum** is a Python script that generates beautiful, colorized summaries of your Timewarrior time tracking data.
It provides rich formatting, customizable themes, and flexible time ranges, all powered by Python and [Rich](https://github.com/Textualize/rich).

---

## Features

- 🚀 Fast, terminal-friendly summary output
- 🎨 Multiple color themes (e.g., `mocha`, `latte`, `frappe`) with custom theme support
- ⏱ Flexible time ranges (`:day`, `:week`, `:month`, `:all`)
- 💻 Isolated Python environment with virtual environment support
- 📦 Easy user-level installation without root
- 🎯 Consistent tag coloring across summaries

---

## Table of Contents

- [Installation](#installation)
  - [System-Wide](#system-wide-installation)
  - [User / Virtual Environment](#user--virtual-environment-installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Custom Themes](#custom-themes)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Installation

### User / Virtual Environment Installation (Recommended)

This method installs `timsum` in a local virtual environment, avoiding conflicts with system Python packages.

```bash
# Clone the repository
git clone https://github.com/yourusername/timsum.git
cd timsum

# Run the installation script
bash install.sh
```

The installation script will ask you to choose between local or system-wide installation. For most users, local installation is recommended.

After installation, ensure the install directory is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

You can add this line to ~/.bashrc or ~/.zshrc to persist it.

### System-Wide Installation (Optional)

Requires root privileges.

```bash
sudo bash install.sh
```

This will install timsum to /usr/local/bin and install required Python packages system-wide.

## Usage

```bash
timsum [OPTIONS]
```

### Examples

```bash
timsum --theme mocha --range :week
timsum --theme latte --range :month
timsum --theme kanagawa --range :all
timsum --theme frappe --range :day
```

### Options

- `--theme <theme>`: Choose a theme for output (mocha, latte, frappe, macchiato, or custom theme name)
- `--range <range>`: Select a time range (`:day`, `:week`, `:month`, `:all`)

## Configuration

TimSum supports configuration files for setting default options:

**Configuration file location:**
- Local installation: `~/.config/timsum/timsum.conf`
- System-wide installation: `/etc/timsum/timsum.conf`

**Example configuration:**
```ini
[timsum]
theme = mocha
range = :week
```

Command-line arguments will override configuration file settings.

## Custom Themes

TimSum supports custom themes in addition to the built-in Catppuccin themes. You can create your own themes by adding JSON files to the themes directory.

**Theme directory location:**
- Local installation: `~/.config/timsum/themes/`
- System-wide installation: `/etc/timsum/themes/`

**Creating a custom theme:**

1. Create a JSON file named `{theme-name}.json` in the themes directory
2. Define the four required color properties:

```json
{
  "base": "#1f1f28",
  "text": "#dcd7ba", 
  "accent": "#7e9cd8",
  "highlight": "#ff9e3b"
}
```

**Example custom theme (Kanagawa):**
```bash
# Create the theme file
echo '{
  "base": "#1f1f28",
  "text": "#dcd7ba",
  "accent": "#7e9cd8", 
  "highlight": "#ff9e3b"
}' > ~/.config/timsum/themes/kanagawa.json

# Use your custom theme
timsum --theme kanagawa --range :week
```

The installer automatically creates a sample Kanagawa theme to get you started.

## Development

### Prerequisites

- Python 3.10+
- `pip` package manager

### Setup for Development

```bash
# Clone the repo
git clone https://github.com/yourusername/timsum.git
cd timsum

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Run Locally

```bash
python timsum.py --theme mocha/frappe/macchiato/latte --range :all/:week/:day/:month
```

### Contributions 

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to your branch: `git push origin feature/my-feature`
5. Open a Pull Request.

Please adhere to [PEP 8](https://peps.python.org/pep-0008/) for Python code style.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- [Catppuccin](https://github.com/catppuccin/catppuccin) color palette for built-in themes
- Inspired by terminal productivity tools like `tldr` and `glances`.

## Roadmap

- [x] ~~Config file support (~/.timsum/timsum.conf)~~
- [x] ~~Additional themes and color schemes~~
- [ ] Export summaries to CSV or JSON
- [ ] Interactive TUI mode
