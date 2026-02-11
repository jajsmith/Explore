#!/usr/bin/env bash
# Modernized macOS dev environment setup
# Neovim + lazy.nvim + Starship + Nerd Font
#
# Replaces the 2015 setup.sh. Run with: bash setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── 1. Homebrew ──────────────────────────────────────────────
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add brew to PATH for the rest of this script (Apple Silicon path)
    if [[ -f /opt/homebrew/bin/brew ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "Homebrew already installed."
fi

# ── 2. Core tools ───────────────────────────────────────────
echo "Installing core tools..."
brew install neovim starship ripgrep fd

# ── 3. Nerd Font ─────────────────────────────────────────────
echo "Installing MesloLGS Nerd Font..."
brew install --cask font-meslo-lg-nerd-font

# ── 4. iTerm2 ────────────────────────────────────────────────
if brew list --cask iterm2 &>/dev/null || [[ -d "/Applications/iTerm.app" ]]; then
    echo "iTerm2 already installed."
else
    echo "Installing iTerm2..."
    brew install --cask iterm2
fi

# ── 5. Starship prompt ──────────────────────────────────────
# Add Starship init and vim alias to .zshrc if not already present
if ! grep -q 'starship init zsh' ~/.zshrc 2>/dev/null; then
    echo '' >> ~/.zshrc
    echo '# Starship prompt' >> ~/.zshrc
    echo 'eval "$(starship init zsh)"' >> ~/.zshrc
    echo "Added Starship init to ~/.zshrc"
else
    echo "Starship init already in ~/.zshrc"
fi

if ! grep -q 'alias vim=nvim' ~/.zshrc 2>/dev/null; then
    echo '' >> ~/.zshrc
    echo '# Use Neovim as vim' >> ~/.zshrc
    echo 'alias vim=nvim' >> ~/.zshrc
    echo "Added vim→nvim alias to ~/.zshrc"
else
    echo "vim→nvim alias already in ~/.zshrc"
fi

# Copy Starship config
mkdir -p ~/.config
cp "${SCRIPT_DIR}/starship.toml" ~/.config/starship.toml
echo "Copied starship.toml → ~/.config/starship.toml"

# ── 6. Neovim config ────────────────────────────────────────
NVIM_CONFIG_DIR="${HOME}/.config/nvim"

if [[ -e "${NVIM_CONFIG_DIR}" ]]; then
    if [[ -L "${NVIM_CONFIG_DIR}" ]]; then
        echo "Removing existing nvim config symlink..."
        rm "${NVIM_CONFIG_DIR}"
    else
        BACKUP="${NVIM_CONFIG_DIR}.backup.$(date +%Y%m%d%H%M%S)"
        echo "Backing up existing nvim config → ${BACKUP}"
        mv "${NVIM_CONFIG_DIR}" "${BACKUP}"
    fi
fi

ln -s "${SCRIPT_DIR}/nvim" "${NVIM_CONFIG_DIR}"
echo "Symlinked nvim config → ${NVIM_CONFIG_DIR}"

# ── Done ─────────────────────────────────────────────────────
echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Open a new terminal tab — Starship prompt should render with icons"
echo "  2. Set iTerm2 font to \"MesloLGS Nerd Font\" (Preferences → Profiles → Text)"
echo "  3. Run 'nvim' — lazy.nvim will auto-install all plugins on first launch"
echo "  4. Open a .py, .ts, or .rs file — Mason will auto-install the LSP server"
