-- LSP: mason (auto-install servers) + native vim.lsp.config (Neovim 0.11+)

return {
	-- Mason: portable LSP/DAP/linter/formatter installer
	{
		"williamboman/mason.nvim",
		build = ":MasonUpdate",
		opts = {},
	},

	-- Bridge mason ↔ lspconfig (handles auto-install)
	{
		"williamboman/mason-lspconfig.nvim",
		dependencies = { "williamboman/mason.nvim" },
		opts = {
			ensure_installed = {
				"pyright",
				"ruff",
				"ts_ls",
				"rust_analyzer",
			},
			automatic_installation = true,
		},
	},

	-- cmp-nvim-lsp (needed to advertise completion capabilities)
	{
		"hrsh7th/cmp-nvim-lsp",
		lazy = true,
	},

	-- LSP keymaps via LspAttach autocmd + native vim.lsp.config
	{
		"williamboman/mason-lspconfig.nvim",
		event = { "BufReadPre", "BufNewFile" },
		config = function()
			local capabilities = require("cmp_nvim_lsp").default_capabilities()

			-- Keymaps applied per-buffer when any LSP attaches
			vim.api.nvim_create_autocmd("LspAttach", {
				callback = function(ev)
					local map = function(keys, func, desc)
						vim.keymap.set("n", keys, func, { buffer = ev.buf, desc = desc })
					end

					map("gd", vim.lsp.buf.definition, "Go to definition")
					map("gr", vim.lsp.buf.references, "Go to references")
					map("gI", vim.lsp.buf.implementation, "Go to implementation")
					map("K", vim.lsp.buf.hover, "Hover documentation")
					map("<leader>rn", vim.lsp.buf.rename, "Rename symbol")
					map("<leader>ca", vim.lsp.buf.code_action, "Code action")
					map("<leader>f", function()
						vim.lsp.buf.format({ async = true })
					end, "Format buffer")
				end,
			})

			-- Configure servers using native vim.lsp.config
			local servers = { "pyright", "ruff", "ts_ls", "rust_analyzer" }

			for _, server in ipairs(servers) do
				vim.lsp.config(server, {
					capabilities = capabilities,
				})
			end

			vim.lsp.enable(servers)
		end,
	},
}
