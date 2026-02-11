-- Editor options (migrated from vimrc)

vim.g.mapleader = " "
vim.g.maplocalleader = " "

local opt = vim.opt

-- Line numbers
opt.number = true
opt.relativenumber = true

-- Indentation
opt.smartindent = true
opt.tabstop = 4
opt.softtabstop = 4
opt.shiftwidth = 4
opt.expandtab = true

-- Visual guides
opt.colorcolumn = "100"
opt.signcolumn = "yes"
opt.cursorline = true

-- Encoding & display
opt.encoding = "utf-8"
opt.termguicolors = true

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = true
opt.incsearch = true

-- System clipboard
opt.clipboard = "unnamedplus"

-- Splits
opt.splitbelow = true
opt.splitright = true

-- Undo persistence
opt.undofile = true

-- Reduce update time for snappier gitsigns / LSP
opt.updatetime = 250

-- Scroll context
opt.scrolloff = 8
