"""MCP bridge for exposing MCP tools to the chat app."""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

_PYODIDE = sys.platform == "emscripten"

if not _PYODIDE:
    import httpx


MCP_SERVERS = {
    "browser-api": {
        "type": "streamable-http",
        "url": "https://browser-api.fly.dev/mcp",
        "timeout": 30.0,
        "serverInstructions": True,
        "headers": {},
    },
    "accountesi-mcp": {
        "type": "streamable-http",
        "url": "https://accountesi-mcp.fly.dev/mcp",
        "timeout": 30.0,
        "serverInstructions": True,
        "headers": {"X-User-ID": "{{USER_ID}}"},
    },
}


def _user_id(default_user: str | None = None) -> str:
    return os.getenv("MCP_USER_ID") or os.getenv("XERO_USER_ID") or (default_user or "user")


def _render_headers(template: dict[str, str], user_id: str) -> dict[str, str]:
    headers = {}
    for key, value in (template or {}).items():
        headers[key] = value.replace("{{USER_ID}}", user_id)
    return headers


def _mcp_request(url: str, headers: dict[str, str], method: str, params: dict[str, Any] | None = None) -> Any:
    payload = {
        "jsonrpc": "2.0",
        "id": f"mcp-{int(time.time() * 1000)}",
        "method": method,
        "params": params or {},
    }
    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(data["error"])
    return data.get("result") if isinstance(data, dict) else data


def _list_tools(server: dict[str, Any], user_id: str) -> list[dict[str, Any]]:
    headers = _render_headers(server.get("headers") or {}, user_id)
    result = _mcp_request(server["url"], headers, "tools/list") or []
    if isinstance(result, dict) and "tools" in result:
        return result.get("tools") or []
    if isinstance(result, list):
        return result
    return []


def _call_tool(server: dict[str, Any], user_id: str, tool_name: str, arguments: dict[str, Any]) -> Any:
    headers = _render_headers(server.get("headers") or {}, user_id)
    params = {"name": tool_name, "arguments": arguments or {}}
    return _mcp_request(server["url"], headers, "tools/call", params)


def register_mcp_tools(
    tools: list[dict[str, Any]],
    handlers: dict[str, Any],
    *,
    default_user: str | None = None,
) -> None:
    if _PYODIDE:
        return
    user_id = _user_id(default_user)
    for server_name, server in MCP_SERVERS.items():
        try:
            tool_list = _list_tools(server, user_id)
        except Exception as exc:
            print(f"[mcp_bridge] Failed to list tools for {server_name}: {exc}")
            continue
        for tool in tool_list:
            mcp_name = tool.get("name")
            if not mcp_name:
                continue
            tool_name = f"mcp_{server_name.replace('-', '_')}__{mcp_name}"
            input_schema = tool.get("inputSchema") or {"type": "object", "properties": {}}
            tool_def = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool.get("description") or f"MCP tool {mcp_name} ({server_name})",
                    "parameters": input_schema,
                },
            }
            tools.append(tool_def)

            def _make_handler(server_cfg, raw_name):
                def _handler(args):
                    return _call_tool(server_cfg, user_id, raw_name, args or {})

                return _handler

            handlers[tool_name] = _make_handler(server, mcp_name)
