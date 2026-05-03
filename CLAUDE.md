# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                          # install / sync dependencies
uv run things-mcp                # run the MCP server (stdio mode)
uv run mcp dev src/things_mcp/server.py  # open MCP inspector for interactive testing
```

## Architecture

All logic lives in a single file: `src/things_mcp/server.py`.

- **`_load_auth_token()`** — reads the token from `THINGS_AUTH_TOKEN` env var, or from a file path in `THINGS_AUTH_TOKEN_FILE` (enforces `chmod 600`). Called once at import time; result stored in module-level `_auth_token`.
- **`_open_things_url(command, params)`** — strips `None` values, URL-encodes with `quote_via=urllib.parse.quote` (spaces → `%20`, not `+`), builds `things:///{command}?...`, and calls `subprocess.run(["open", url])`. Fire-and-forget; no return values from Things.
- **`_require_auth()`** — raises `ValueError` with a helpful message if `_auth_token` is `None`.
- **MCP tools** — eight `@mcp.tool()` functions mapping 1:1 to Things URL scheme commands: `add_todo`, `add_project`, `update_todo`, `update_project`, `show`, `search`, `get_version`, `json_command`. Update tools call `_require_auth()` before building the URL.

The entry point `main()` calls `mcp.run()` (FastMCP stdio transport), invoked via the `things-mcp` script defined in `pyproject.toml`.
