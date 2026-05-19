#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Variables – adjust if your paths differ
# ------------------------------------------------------------------
SCRIPT_PATH="/home/electric-otter/Downloads/kali-code-main/kali-code-main/interactive.py"
LINK_NAME="kali-code"
LINK_DIR="/usr/local/bin"

# ------------------------------------------------------------------
# Step 1 – Ensure the Python script is executable
# ------------------------------------------------------------------
if [[ ! -x "$SCRIPT_PATH" ]]; then
    echo "Making interactive.py executable..."
    chmod +x "$SCRIPT_PATH"
else
    echo "interactive.py is already executable."
fi

# ------------------------------------------------------------------
# Step 2 – Create (or update) the symlink in /usr/local/bin
# ------------------------------------------------------------------
TARGET_LINK="${LINK_DIR}/${LINK_NAME}"

if [[ -L "$TARGET_LINK" ]] && [[ "$(readlink -f "$TARGET_LINK")" == "$SCRIPT_PATH" ]]; then
    echo "Symlink already exists and points to the correct script."
else
    echo "Creating symlink: $TARGET_LINK -> $SCRIPT_PATH"
    sudo ln -sf "$SCRIPT_PATH" "$TARGET_LINK"
fi

# ------------------------------------------------------------------
# Optional Step 3 – Add the whole project directory to $PATH
# ------------------------------------------------------------------
# Uncomment the following lines if you’d rather have the entire folder on your PATH
# PROJECT_DIR="$(dirname "$SCRIPT_PATH")"
# SHELL_RC="${HOME}/.bashrc"   # change to .zshrc if you use Zsh
# if ! grep -q "export PATH=.*${PROJECT_DIR}" "$SHELL_RC"; then
#     echo "Adding project directory to PATH in $SHELL_RC"
#     echo "export PATH=\"\$PATH:${PROJECT_DIR}\"" >> "$SHELL_RC"
#     echo "Run 'source $SHELL_RC' or start a new terminal to apply."
# else
#     echo "Project directory already in PATH."
# fi

# ------------------------------------------------------------------
# Done!
# ------------------------------------------------------------------
echo "Installation complete. You can now run:"
echo "    kali-code"
echo "If you added the optional PATH entry, remember to reload your shell:"
echo "    source \${HOME}/.bashrc   # or .zshrc"
