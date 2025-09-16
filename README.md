TimSum is a python script that allows users to see their timewarrior's summary more beautifully

# Timsum

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**TimSum** is a Python script that generates beautiful, colorized summaries of your Timewarrior time tracking data.
It provides rich formatting, customizable themes, and flexible time ranges, all powered by Python and [Rich](https://github.com/Textualize/rich).

---

## Features

- 🚀 Fast, terminal-friendly summary output
- 🎨 Multiple color themes (e.g., `mocha`, `latte`, `frappe`)
- ⏱ Flexible time ranges (`:day`, `:week`, `:month`, `:all`)
- 💻 Isolated Python environment with virtual environment support
- 📦 Easy user-level installation without root

---

## Table of Contents

- [Installation](#installation)
  - [System-Wide](#system-wide-installation)
  - [User / Virtual Environment](#user--virtual-environment-installation)
- [Usage](#usage)
- [Configuration](#configuration)
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
After installation, ensure the install directory is in your PATH:
```bash
export PATH="$HOME/.timsum:$PATH"
```

You can add this line to ~/.bashrc or ~/.zshrc to persist it.

System-Wide Installation (Optional)

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
timsum --theme frappe --range :all
```

### Options
- --theme <theme>: Choose a theme for output (mocha, latte, frappe)

- --range <range>: Select a time range (:day, :week, :month, :all)

## Configuration

Currently, configuration is minimal and handled via CLI arguments.
Future versions may support a config file in ~/.timsum/config.toml with defaults for:
- Default theme
- Default time range
- Output format

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
python timew.py --theme mocha/frappe/machiatto/latte --range :all/:week/:day/:month
```

### Contributions 
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: git checkout -b feature/my-feature
3. Commit your changes: git commit -m "Add my feature"
4. Push to your branch: git push origin feature/my-feature
5. Open a Pull Request.

Please adhere to [PEP 8](https://peps.python.org/pep-0008/) for Python code style.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Inspired by terminal productivity tools like `tldr` and `glances`.

## Roadmap
- [ ] Config file support (~/.timsum/config.toml)
- [ ] Additional themes and color schemes
- [ ] Export summaries to CSV or JSON
- [ ] Interactive TUI mode
