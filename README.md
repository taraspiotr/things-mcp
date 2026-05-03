# things-mcp

A [Model Context Protocol](https://modelcontextprotocol.io) server for [Things 3](https://culturedcode.com/things/) — lets Claude (or any MCP-compatible LLM) create, update, and navigate your tasks hands-free.

## What it does

Exposes the [Things URL scheme](https://culturedcode.com/things/support/articles/2803573/) as MCP tools so you can say things like:

> *"Add a to-do to buy milk for tomorrow"*  
> *"Create a project called 'Corsica Trip' with packing tasks"*  
> *"Move that task to Someday"*  
> *"Show me today's list"*

## Requirements

- macOS with [Things 3](https://culturedcode.com/things/) installed
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone https://github.com/taraspiotr/things-mcp
cd things-mcp
uv sync
```

## Claude Desktop setup

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "things": {
      "command": "/path/to/things-mcp/.venv/bin/things-mcp",
      "env": {
        "THINGS_AUTH_TOKEN": "your-token-here"
      }
    }
  }
}
```

Replace `/path/to/things-mcp` with the actual clone path (e.g. `/Users/yourname/repositories/things-mcp`).

### Getting your auth token

Things 3 → **Settings → General → Enable Things URLs → Manage**

The token is only required for updating existing tasks. Creating tasks and navigating works without it.

### Using a token file instead

If you'd rather not put the token directly in the config:

```bash
echo "your-token" > ~/.things-token
chmod 600 ~/.things-token
```

```json
"env": { "THINGS_AUTH_TOKEN_FILE": "/Users/yourname/.things-token" }
```

The server will refuse to start if the file permissions are anything other than `600`.

## Available tools

| Tool | Description | Auth required |
|------|-------------|:---:|
| `add_todo` | Create a to-do | |
| `add_project` | Create a project | |
| `update_todo` | Update an existing to-do | ✓ |
| `update_project` | Update an existing project | ✓ |
| `show` | Navigate to a list, project, or item | |
| `search` | Open the search screen | |
| `get_version` | Get the Things app version | |
| `json_command` | Bulk create/update via JSON | ✓ |

### Scheduling values

The `when` parameter accepts: `today`, `tomorrow`, `evening`, `anytime`, `someday`, or a date string (`2026-05-10`).

## License

MIT
