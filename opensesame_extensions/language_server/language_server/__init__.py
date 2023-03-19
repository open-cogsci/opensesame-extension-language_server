"""Support for language server protocol (LSP)"""

settings = {
    "lsp_enable_r": True,
    "lsp_enable_css": True,
    "lsp_enable_python": False,
    "lsp_enable_typescript": True,
    "lsp_enable_json": True,
    "lsp_enable_yaml": True,
    "lsp_diagnostics": True,
    "lsp_diagnostics_ignore": {
        "ide": "",
        "default": "Cannot find name 'vars'"
    },
    "lsp_calltips": True,
    "lsp_code_completion": True,
    "lsp_symbols": True,
    "lsp_symbols_kind": "Class;Function;Method"}
modes = ["ide", "default"]
