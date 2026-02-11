-- Editor plugins: Treesitter, Telescope, gitsigns, fugitive

return {
	-- Treesitter: syntax highlighting + text objects
	{
		"nvim-treesitter/nvim-treesitter",
		build = ":TSUpdate",
		event = { "BufReadPost", "BufNewFile" },
		main = "nvim-treesitter",
		opts = {
			ensure_installed = {
				"bash", "c", "css", "html", "javascript", "json",
				"lua", "markdown", "python", "rust", "toml",
				"tsx", "typescript", "vim", "vimdoc", "yaml",
			},
		},
	},

	-- Telescope: fuzzy finder
	{
		"nvim-telescope/telescope.nvim",
		branch = "0.1.x",
		dependencies = {
			"nvim-lua/plenary.nvim",
			{
				"nvim-telescope/telescope-fzf-native.nvim",
				build = "make",
			},
		},
		config = function()
			local telescope = require("telescope")
			telescope.setup({
				defaults = {
					file_ignore_patterns = { "node_modules", ".git/" },
				},
			})
			telescope.load_extension("fzf")
		end,
	},

	-- Gitsigns: git diff signs in the gutter
	{
		"lewis6991/gitsigns.nvim",
		event = { "BufReadPre", "BufNewFile" },
		opts = {},
	},

	-- Fugitive: Git commands (kept from old config — still the best)
	{
		"tpope/vim-fugitive",
		cmd = "Git",
	},
}
