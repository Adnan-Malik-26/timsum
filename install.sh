#!/usr/bin/env bash
# Timsum Installation Script with Virtual Environment
# This script will install timsum with options for local or system-wide installation
set -e

SCRIPT_NAME="timsum"
PYTHON_SCRIPT="timsum.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
  echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
  echo -e "${RED}❌ $1${NC}"
}

# Function to check if running as root
is_root() {
  [ "$(id -u)" -eq 0 ]
}

# Function to get installation type from user
get_install_type() {
  echo -e "${BLUE}🚀 Timsum Installation Script${NC}"
  echo ""
  echo "Choose installation type:"
  echo "1) Local installation (user-only, recommended)"
  echo "2) System-wide installation (requires sudo)"
  echo ""

  while true; do
    read -p "Enter your choice [1-2]: " choice
    case $choice in
    1)
      INSTALL_TYPE="local"
      break
      ;;
    2)
      INSTALL_TYPE="system"
      break
      ;;
    *)
      print_error "Invalid choice. Please enter 1 or 2."
      ;;
    esac
  done
}

# Function to set installation directories based on type
set_install_dirs() {
  if [ "$INSTALL_TYPE" = "local" ]; then
    INSTALL_DIR="$HOME/.local/share/timsum"
    BIN_DIR="$HOME/.local/bin"
    CONFIG_BASE="$HOME/.config"
    print_status "Installing locally for current user..."
  else
    INSTALL_DIR="/opt/timsum"
    BIN_DIR="/usr/local/bin"
    CONFIG_BASE="/etc"
    print_status "Installing system-wide (requires sudo)..."

    if ! is_root && ! command -v sudo &>/dev/null; then
      print_error "System-wide installation requires sudo, but sudo is not available."
      exit 1
    fi
  fi

  VENV_DIR="$INSTALL_DIR/venv"
  WRAPPER="$BIN_DIR/$SCRIPT_NAME"
}

# Function to create directories
create_directories() {
  if [ "$INSTALL_TYPE" = "system" ] && ! is_root; then
    sudo mkdir -p "$INSTALL_DIR" "$BIN_DIR"
    sudo mkdir -p "$CONFIG_BASE/timsum/themes"
  else
    mkdir -p "$INSTALL_DIR" "$BIN_DIR"
    mkdir -p "$CONFIG_BASE/timsum/themes"
  fi
}

# Function to create virtual environment and install packages
setup_venv() {
  print_status "Creating Python virtual environment..."

  if [ "$INSTALL_TYPE" = "system" ] && ! is_root; then
    sudo python3 -m venv "$VENV_DIR"
    sudo "$VENV_DIR/bin/pip" install --upgrade pip
    sudo "$VENV_DIR/bin/pip" install rich
  else
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install rich
  fi

  print_success "Virtual environment created and packages installed."
}

# Function to install the script
install_script() {
  print_status "Installing timsum script..."

  # Check if the Python script exists
  if [ ! -f "$PYTHON_SCRIPT" ]; then
    print_error "timsum.py not found in current directory. Please run this script from the timsum source directory."
    exit 1
  fi

  # Copy the Python script to the installation directory
  if [ "$INSTALL_TYPE" = "system" ] && ! is_root; then
    sudo cp "$PYTHON_SCRIPT" "$INSTALL_DIR/"
    sudo chmod +x "$INSTALL_DIR/$PYTHON_SCRIPT"
  else
    cp "$PYTHON_SCRIPT" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$PYTHON_SCRIPT"
  fi

  # Create wrapper script
  create_wrapper_script
}

# Function to create wrapper script
create_wrapper_script() {
  local wrapper_content
  wrapper_content=$(
    cat <<EOL
#!/usr/bin/env bash
# Timsum wrapper script - automatically activates virtual environment
source "$VENV_DIR/bin/activate"
exec python3 "$INSTALL_DIR/$PYTHON_SCRIPT" "\$@"
EOL
  )

  if [ "$INSTALL_TYPE" = "system" ] && ! is_root; then
    echo "$wrapper_content" | sudo tee "$WRAPPER" >/dev/null
    sudo chmod +x "$WRAPPER"
  else
    echo "$wrapper_content" >"$WRAPPER"
    chmod +x "$WRAPPER"
  fi

  print_success "Wrapper script created at $WRAPPER"
}

# Function to create sample config and theme
create_sample_config() {
  print_status "Creating sample configuration and theme..."

  local config_dir="$CONFIG_BASE/timsum"
  local sample_config="$config_dir/timsum.conf"
  local sample_theme="$config_dir/themes/kanagawa.json"

  # Create sample config
  local config_content=$(
    cat <<EOL
[timsum]
theme = mocha
range = :week
EOL
  )

  # Create sample Kanagawa theme
  local kanagawa_theme=$(
    cat <<EOL
{
  "base": "#1f1f28",
  "text": "#dcd7ba",
  "accent": "#7e9cd8",
  "highlight": "#ff9e3b"
}
EOL
  )

  if [ "$INSTALL_TYPE" = "system" ] && ! is_root; then
    if [ ! -f "$sample_config" ]; then
      echo "$config_content" | sudo tee "$sample_config" >/dev/null
      print_success "Sample config created at $sample_config"
    fi
    if [ ! -f "$sample_theme" ]; then
      echo "$kanagawa_theme" | sudo tee "$sample_theme" >/dev/null
      print_success "Sample Kanagawa theme created at $sample_theme"
    fi
  else
    if [ ! -f "$sample_config" ]; then
      echo "$config_content" >"$sample_config"
      print_success "Sample config created at $sample_config"
    fi
    if [ ! -f "$sample_theme" ]; then
      echo "$kanagawa_theme" >"$sample_theme"
      print_success "Sample Kanagawa theme created at $sample_theme"
    fi
  fi
}

# Function to check PATH and provide guidance
check_path() {
  if [ "$INSTALL_TYPE" = "local" ]; then
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
      print_warning "$BIN_DIR is not in your PATH."
      echo ""
      echo "To add it to your PATH, add this line to your shell configuration file:"
      echo "  ~/.bashrc (for Bash) or ~/.zshrc (for Zsh):"
      echo ""
      echo "  export PATH=\"$BIN_DIR:\$PATH\""
      echo ""
      echo "Then restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
    else
      print_success "$BIN_DIR is already in your PATH."
    fi
  else
    print_success "System-wide installation completed. $BIN_DIR should be in your PATH."
  fi
}

# Function to display usage examples
show_usage() {
  echo ""
  echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
  echo ""
  echo "Usage examples:"
  echo "  $SCRIPT_NAME --theme mocha --range :week"
  echo "  $SCRIPT_NAME --theme kanagawa --range :month"
  echo "  $SCRIPT_NAME --theme latte --range :all"
  echo ""
  echo "Configuration locations:"
  if [ "$INSTALL_TYPE" = "local" ]; then
    echo "  Config file: ~/.config/timsum/timsum.conf"
    echo "  Themes directory: ~/.config/timsum/themes/"
  else
    echo "  Config file: /etc/timsum/timsum.conf"
    echo "  Themes directory: /etc/timsum/themes/"
  fi
}

# Main installation function
main() {
  # Check if Python 3 is installed
  if ! command -v python3 &>/dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
  fi

  # Check if timewarrior is installed
  if ! command -v timew &>/dev/null; then
    print_warning "Timewarrior (timew) not found. Please install timewarrior for timsum to work properly."
  fi

  # Get installation preference from user
  get_install_type

  # Set installation directories
  set_install_dirs

  # Create necessary directories
  create_directories

  # Setup virtual environment and install packages
  setup_venv

  # Install the main script
  install_script

  # Create sample configuration and theme
  create_sample_config

  # Check PATH and provide guidance
  check_path

  # Show usage information
  show_usage
}

# Run main function
main "$@"
