#!/usr/bin/env bash

# Timsum Installation Script with Virtual Environment
# This script will install timsum in a local Python virtual environment

set -e

INSTALL_DIR="$HOME/.timsum"
VENV_DIR="$INSTALL_DIR/venv"
SCRIPT_NAME="timsum"
PYTHON_SCRIPT="timsum.py"
BIN_DIR="$INSTALL_DIR/bin"

echo "🚀 Installing timsum in a virtual environment..."

# Ensure Python 3 is installed
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 is not installed. Please install Python 3 first."
  exit 1
fi

# Create installation directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
  echo "🔧 Creating Python virtual environment..."
  python3 -m venv "$VENV_DIR"
else
  echo "ℹ️  Virtual environment already exists."
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip and install required packages
echo "📦 Installing required Python packages..."
pip install --upgrade pip
pip install rich

# Copy timsum.py to bin directory
mkdir -p "$BIN_DIR"
cp "$PYTHON_SCRIPT" "$BIN_DIR/$SCRIPT_NAME"
chmod +x "$BIN_DIR/$SCRIPT_NAME"

# Create a wrapper script to activate venv automatically
WRAPPER="$INSTALL_DIR/$SCRIPT_NAME"
cat >"$WRAPPER" <<EOL
#!/usr/bin/env bash
source "$VENV_DIR/bin/activate"
exec "$BIN_DIR/$SCRIPT_NAME" "\$@"
EOL
chmod +x "$WRAPPER"

echo "✅ timsum installed to $WRAPPER"

echo ""
echo "Make sure $INSTALL_DIR is in your PATH. You can add this line to ~/.bashrc or ~/.zshrc:"
echo "  export PATH=\"$INSTALL_DIR:\$PATH\""

echo ""
echo "Usage examples:"
echo "  $SCRIPT_NAME --theme mocha --range :week"
echo "  $SCRIPT_NAME --theme latte --range :month"
echo "  $SCRIPT_NAME --theme frappe --range :all"
