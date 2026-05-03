import os
import subprocess
import urllib.parse
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("things")

_auth_token: Optional[str] = os.environ.get("THINGS_AUTH_TOKEN")


def _open_things_url(command: str, params: dict) -> str:
    filtered = {k: v for k, v in params.items() if v is not None}
    if filtered:
        query = urllib.parse.urlencode(filtered)
        url = f"things:///{command}?{query}"
    else:
        url = f"things:///{command}"
    subprocess.run(["open", url], check=True)
    return url


def _require_auth() -> str:
    if not _auth_token:
        raise ValueError(
            "THINGS_AUTH_TOKEN environment variable is not set. "
            "Get your token from Things → Settings → General → Enable Things URLs → Manage."
        )
    return _auth_token


@mcp.tool()
def add_todo(
    title: str,
    notes: Optional[str] = None,
    when: Optional[str] = None,
    deadline: Optional[str] = None,
    tags: Optional[str] = None,
    list: Optional[str] = None,
    heading: Optional[str] = None,
    checklist_items: Optional[str] = None,
    completed: Optional[bool] = None,
    canceled: Optional[bool] = None,
) -> str:
    """Create a new to-do in Things.

    Args:
        title: Title of the to-do.
        notes: Notes text (max 10,000 chars).
        when: Scheduling — today, tomorrow, evening, anytime, someday, or a date (yyyy-mm-dd).
        deadline: Due date (yyyy-mm-dd).
        tags: Comma-separated tag names.
        list: Project or area name to add the to-do into.
        heading: Heading within the project.
        checklist_items: Newline-separated checklist item titles (max 100).
        completed: Mark as completed.
        canceled: Mark as canceled.
    """
    url = _open_things_url("add", {
        "title": title,
        "notes": notes,
        "when": when,
        "deadline": deadline,
        "tags": tags,
        "list": list,
        "heading": heading,
        "checklist-items": checklist_items,
        "completed": str(completed).lower() if completed is not None else None,
        "canceled": str(canceled).lower() if canceled is not None else None,
    })
    return f"To-do '{title}' created via {url}"


@mcp.tool()
def add_project(
    title: str,
    notes: Optional[str] = None,
    when: Optional[str] = None,
    deadline: Optional[str] = None,
    tags: Optional[str] = None,
    area: Optional[str] = None,
    todos: Optional[str] = None,
    completed: Optional[bool] = None,
    canceled: Optional[bool] = None,
) -> str:
    """Create a new project in Things.

    Args:
        title: Title of the project.
        notes: Notes text (max 10,000 chars).
        when: Scheduling — today, tomorrow, evening, anytime, someday, or a date (yyyy-mm-dd).
        deadline: Due date (yyyy-mm-dd).
        tags: Comma-separated tag names.
        area: Area name to place the project in.
        todos: Newline-separated to-do titles to add inside the project.
        completed: Mark as completed.
        canceled: Mark as canceled.
    """
    url = _open_things_url("add-project", {
        "title": title,
        "notes": notes,
        "when": when,
        "deadline": deadline,
        "tags": tags,
        "area": area,
        "to-dos": todos,
        "completed": str(completed).lower() if completed is not None else None,
        "canceled": str(canceled).lower() if canceled is not None else None,
    })
    return f"Project '{title}' created via {url}"


@mcp.tool()
def update_todo(
    id: str,
    title: Optional[str] = None,
    notes: Optional[str] = None,
    prepend_notes: Optional[str] = None,
    append_notes: Optional[str] = None,
    when: Optional[str] = None,
    deadline: Optional[str] = None,
    tags: Optional[str] = None,
    add_tags: Optional[str] = None,
    list: Optional[str] = None,
    heading: Optional[str] = None,
    checklist_items: Optional[str] = None,
    prepend_checklist_items: Optional[str] = None,
    append_checklist_items: Optional[str] = None,
    completed: Optional[bool] = None,
    canceled: Optional[bool] = None,
) -> str:
    """Update an existing to-do in Things. Requires THINGS_AUTH_TOKEN.

    Args:
        id: The Things ID of the to-do to update.
        title: New title.
        notes: Replace notes entirely.
        prepend_notes: Text to prepend to existing notes.
        append_notes: Text to append to existing notes.
        when: New schedule — today, tomorrow, evening, anytime, someday, or yyyy-mm-dd.
        deadline: New due date (yyyy-mm-dd).
        tags: Replace all tags (comma-separated).
        add_tags: Add tags without removing existing ones (comma-separated).
        list: Move to this project or area name.
        heading: Move to this heading within the project.
        checklist_items: Replace checklist items (newline-separated).
        prepend_checklist_items: Prepend checklist items (newline-separated).
        append_checklist_items: Append checklist items (newline-separated).
        completed: Mark as completed.
        canceled: Mark as canceled.
    """
    token = _require_auth()
    url = _open_things_url("update", {
        "id": id,
        "auth-token": token,
        "title": title,
        "notes": notes,
        "prepend-notes": prepend_notes,
        "append-notes": append_notes,
        "when": when,
        "deadline": deadline,
        "tags": tags,
        "add-tags": add_tags,
        "list": list,
        "heading": heading,
        "checklist-items": checklist_items,
        "prepend-checklist-items": prepend_checklist_items,
        "append-checklist-items": append_checklist_items,
        "completed": str(completed).lower() if completed is not None else None,
        "canceled": str(canceled).lower() if canceled is not None else None,
    })
    return f"To-do '{id}' updated via {url}"


@mcp.tool()
def update_project(
    id: str,
    title: Optional[str] = None,
    notes: Optional[str] = None,
    prepend_notes: Optional[str] = None,
    append_notes: Optional[str] = None,
    when: Optional[str] = None,
    deadline: Optional[str] = None,
    tags: Optional[str] = None,
    add_tags: Optional[str] = None,
    area: Optional[str] = None,
    completed: Optional[bool] = None,
    canceled: Optional[bool] = None,
) -> str:
    """Update an existing project in Things. Requires THINGS_AUTH_TOKEN.

    Args:
        id: The Things ID of the project to update.
        title: New title.
        notes: Replace notes entirely.
        prepend_notes: Text to prepend to existing notes.
        append_notes: Text to append to existing notes.
        when: New schedule — today, tomorrow, evening, anytime, someday, or yyyy-mm-dd.
        deadline: New due date (yyyy-mm-dd).
        tags: Replace all tags (comma-separated).
        add_tags: Add tags without removing existing ones (comma-separated).
        area: Move to this area name.
        completed: Mark as completed.
        canceled: Mark as canceled.
    """
    token = _require_auth()
    url = _open_things_url("update-project", {
        "id": id,
        "auth-token": token,
        "title": title,
        "notes": notes,
        "prepend-notes": prepend_notes,
        "append-notes": append_notes,
        "when": when,
        "deadline": deadline,
        "tags": tags,
        "add-tags": add_tags,
        "area": area,
        "completed": str(completed).lower() if completed is not None else None,
        "canceled": str(canceled).lower() if canceled is not None else None,
    })
    return f"Project '{id}' updated via {url}"


@mcp.tool()
def show(
    id: Optional[str] = None,
    query: Optional[str] = None,
    filter: Optional[str] = None,
) -> str:
    """Navigate to a list, project, area, tag, or to-do in Things.

    Args:
        id: Item ID or built-in list name: inbox, today, anytime, upcoming, someday,
            logbook, tomorrow, deadlines, repeating, all-projects, logged-projects.
        query: Name-based search (used instead of id if id is not set).
        filter: Comma-separated tag names to filter the view.
    """
    url = _open_things_url("show", {"id": id, "query": query, "filter": filter})
    return f"Navigated via {url}"


@mcp.tool()
def search(query: Optional[str] = None) -> str:
    """Open the search screen in Things, optionally pre-filled with a query.

    Args:
        query: Search text to pre-fill.
    """
    url = _open_things_url("search", {"query": query})
    return f"Search opened via {url}"


@mcp.tool()
def get_version() -> str:
    """Get the Things app version and URL scheme version."""
    url = _open_things_url("version", {})
    return f"Version URL opened: {url}"


@mcp.tool()
def json_command(data: str) -> str:
    """Bulk create or update to-dos, projects, and headings via JSON. Requires THINGS_AUTH_TOKEN for updates.

    Args:
        data: JSON array string. Each element is an object with:
              - type: "to-do", "project", or "heading"
              - operation: "create" (default) or "update"
              - id: required for updates
              - attributes: object with title, notes, when, deadline, tags, checklist-items,
                            list, list-id, heading, heading-id, area, area-id, items,
                            completed, canceled, creation-date, completion-date

    Example:
        [{"type": "to-do", "attributes": {"title": "Buy milk", "when": "today"}}]
    """
    token = _require_auth()
    url = _open_things_url("json", {"data": data, "auth-token": token})
    return f"JSON command executed via {url}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
