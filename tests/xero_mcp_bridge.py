"""Xero OAuth + read-only API bridge for the chat demo."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import sys
import time
from typing import Any, Tuple, List, Dict, Callable

from pytincture.dataclass import backend_for_frontend

_PYODIDE = sys.platform == "emscripten"

ACCOUNTESI_MCP_PATH = os.getenv("ACCOUNTESI_MCP_PATH", "/Users/schapman1974/repos/accountesi-mcp")
if not _PYODIDE and os.path.isdir(ACCOUNTESI_MCP_PATH) and ACCOUNTESI_MCP_PATH not in sys.path:
    sys.path.insert(0, ACCOUNTESI_MCP_PATH)

if not _PYODIDE:
    import httpx
    try:
        from app.xero_client import XeroClient  # type: ignore
        from app.models import TokenPayload, TokenState  # type: ignore
        from app.token_store import TokenStore  # type: ignore
    except Exception:  # pragma: no cover - fallback
        XeroClient = None  # type: ignore
        TokenPayload = None  # type: ignore
        TokenState = None  # type: ignore
        TokenStore = None  # type: ignore
else:  # pragma: no cover - pyodide stub
    XeroClient = None  # type: ignore
    TokenPayload = None  # type: ignore
    TokenState = None  # type: ignore
    TokenStore = None  # type: ignore


DEFAULT_SCOPES = (
    "offline_access "
    "accounting.transactions.read "
    "accounting.reports.read "
    "accounting.contacts.read "
    "accounting.settings "
    "openid profile email"
)


def _tool_def(name: str, description: str, parameters: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters,
        },
    }


def _attach_tool(cls, name: str, func, description: str, parameters: dict[str, Any]) -> None:
    func._chat_tool_def = _tool_def(name, description, parameters)
    setattr(cls, name, func)


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def _expires_at(expires_in: int) -> float:
    return time.time() + max(0, expires_in - 60)


def _require_xero_client() -> XeroClient:
    client_id = _env("XERO_CLIENT_ID")
    client_secret = _env("XERO_CLIENT_SECRET")
    redirect_uri = _env("XERO_REDIRECT_URI")
    if not client_id or not client_secret or not redirect_uri:
        raise ValueError(
            "Missing Xero OAuth env vars. Set XERO_CLIENT_ID, XERO_CLIENT_SECRET, XERO_REDIRECT_URI."
        )
    if XeroClient is None:
        raise ValueError("accountesi-mcp XeroClient is unavailable.")
    return XeroClient(client_id, client_secret, redirect_uri)


def _token_store_path(user_id: str) -> str:
    root = _env("XERO_TOKEN_STORE_PATH", "./data/xero_token_store.json")
    if "{user_id}" in root:
        return root.format(user_id=user_id)
    if root.endswith(".json"):
        return root.replace(".json", f".{user_id}.json")
    return f"{root}.{user_id}.json"


class _SimpleTokenState:
    def __init__(
        self,
        *,
        access_token: str,
        refresh_token: str,
        expires_at: float,
        scope: str | None,
        tenant_id: str,
        tenant_name: str | None,
        tenant_type: str | None,
    ) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.scope = scope
        self.tenant_id = tenant_id
        self.tenant_name = tenant_name
        self.tenant_type = tenant_type


class _SimpleTokenStore:
    def __init__(self, path: str) -> None:
        self._path = path

    def load(self) -> _SimpleTokenState | None:
        if not os.path.exists(self._path):
            return None
        try:
            with open(self._path, "r", encoding="utf-8") as handle:
                raw = handle.read().strip()
            if not raw:
                return None
            data = json.loads(raw)
            return _SimpleTokenState(**data)
        except Exception:
            return None

    def save(self, state: _SimpleTokenState) -> None:
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as handle:
            json.dump(state.__dict__, handle, indent=2, sort_keys=True)

    def clear(self) -> None:
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as handle:
            handle.write("")


def _get_store(user_id: str):
    path = _token_store_path(user_id)
    if TokenStore is not None:
        return TokenStore(path)
    return _SimpleTokenStore(path)


def _sign_state(user_id: str) -> str:
    secret = _env("XERO_STATE_SECRET")
    payload = {"uid": user_id, "ts": int(time.time())}
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    b64 = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    if not secret:
        return b64
    sig = hmac.new(secret.encode("utf-8"), b64.encode("utf-8"), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")
    return f"{b64}.{sig_b64}"


def _verify_state(state: str) -> str:
    secret = _env("XERO_STATE_SECRET")
    try:
        if "." in state and secret:
            b64, sig_b64 = state.split(".", 1)
            expected = hmac.new(secret.encode("utf-8"), b64.encode("utf-8"), hashlib.sha256).digest()
            expected_b64 = base64.urlsafe_b64encode(expected).decode("ascii").rstrip("=")
            if not hmac.compare_digest(expected_b64, sig_b64):
                raise ValueError("bad signature")
        else:
            b64 = state
        raw = base64.urlsafe_b64decode(b64 + "==")
        payload = json.loads(raw.decode("utf-8"))
        return str(payload.get("uid") or "")
    except Exception:
        return ""


@backend_for_frontend
class xero_mcp_bridge:
    """Minimal Xero OAuth + read-only API bridge for chat."""

    def get_login_link(self, user_id: str, state: str | None = None) -> dict[str, Any]:
        client = _require_xero_client()
        scope = _env("XERO_SCOPES", DEFAULT_SCOPES) or DEFAULT_SCOPES
        if not state:
            state = _sign_state(user_id)
        return {
            "login_url": client.build_auth_url(state=state, scope=scope),
            "state": state,
            "provider": "xero",
        }

    def auth_callback(self, user_id: str, code: str, tenant_id: str | None = None, state: str | None = None) -> dict[str, Any]:
        client = _require_xero_client()
        if state:
            inferred = _verify_state(state)
            if inferred and inferred != user_id:
                raise ValueError("State mismatch for user.")
        store = _get_store(user_id)
        with httpx.Client(timeout=30) as http:
            token_data = http.post(
                "https://identity.xero.com/connect/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": _env("XERO_REDIRECT_URI"),
                },
                headers={"Authorization": client._basic_auth_header()},  # type: ignore[attr-defined]
            )
            token_data.raise_for_status()
            payload = token_data.json()
            if TokenPayload is not None:
                payload_obj = TokenPayload.model_validate(payload)
                access_token = payload_obj.access_token
                refresh_token = payload_obj.refresh_token
                expires_in = payload_obj.expires_in
                scope = payload_obj.scope
            else:
                access_token = payload["access_token"]
                refresh_token = payload["refresh_token"]
                expires_in = int(payload.get("expires_in", 3600))
                scope = payload.get("scope")
            conns = http.get(
                "https://api.xero.com/connections",
                headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
            )
            conns.raise_for_status()
            connections = conns.json()
            if not connections:
                raise ValueError("No Xero connections found.")
            selected = connections[0]
            if tenant_id:
                for conn in connections:
                    if conn.get("tenantId") == tenant_id:
                        selected = conn
                        break
            if TokenState is not None:
                state_obj = TokenState(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    expires_at=_expires_at(expires_in),
                    scope=scope,
                    tenant_id=selected.get("tenantId"),
                    tenant_name=selected.get("tenantName"),
                    tenant_type=selected.get("tenantType"),
                    provider="xero",
                )
                import asyncio

                asyncio.run(store.save(state_obj))  # type: ignore[arg-type]
            else:
                store.save(
                    _SimpleTokenState(
                        access_token=access_token,
                        refresh_token=refresh_token,
                        expires_at=_expires_at(expires_in),
                        scope=scope,
                        tenant_id=selected.get("tenantId"),
                        tenant_name=selected.get("tenantName"),
                        tenant_type=selected.get("tenantType"),
                    )
                )
            return {
                "tenant_id": selected.get("tenantId"),
                "tenant_name": selected.get("tenantName"),
                "tenant_type": selected.get("tenantType"),
            }

    def auth_status(self, user_id: str) -> dict[str, Any]:
        store = _get_store(user_id)
        state = None
        if TokenStore is not None:
            import asyncio

            state = asyncio.run(store.load())
        else:
            state = store.load()
        if not state:
            return {"authenticated": False}
        expires_at = float(state.expires_at)
        return {
            "authenticated": expires_at > time.time(),
            "expires_at": expires_at,
            "tenant_id": state.tenant_id,
            "tenant_name": state.tenant_name,
            "tenant_type": state.tenant_type,
        }

    def refresh(self, user_id: str) -> dict[str, Any]:
        client = _require_xero_client()
        store = _get_store(user_id)
        if TokenStore is not None:
            import asyncio

            state = asyncio.run(store.load())
        else:
            state = store.load()
        if not state:
            raise ValueError("Not authenticated.")
        refresh_token = state.refresh_token
        with httpx.Client(timeout=30) as http:
            token_data = http.post(
                "https://identity.xero.com/connect/token",
                data={"grant_type": "refresh_token", "refresh_token": refresh_token},
                headers={"Authorization": client._basic_auth_header()},  # type: ignore[attr-defined]
            )
            token_data.raise_for_status()
            payload = token_data.json()
            access_token = payload["access_token"]
            new_refresh = payload.get("refresh_token", refresh_token)
            expires_in = int(payload.get("expires_in", 3600))
            scope = payload.get("scope")
            if TokenState is not None:
                refreshed = TokenState(
                    access_token=access_token,
                    refresh_token=new_refresh,
                    expires_at=_expires_at(expires_in),
                    scope=scope,
                    tenant_id=state.tenant_id,
                    tenant_name=state.tenant_name,
                    tenant_type=state.tenant_type,
                    provider="xero",
                )
                import asyncio

                asyncio.run(store.save(refreshed))  # type: ignore[arg-type]
            else:
                store.save(
                    _SimpleTokenState(
                        access_token=access_token,
                        refresh_token=new_refresh,
                        expires_at=_expires_at(expires_in),
                        scope=scope,
                        tenant_id=state.tenant_id,
                        tenant_name=state.tenant_name,
                        tenant_type=state.tenant_type,
                    )
                )
            return {"authenticated": True, "expires_at": _expires_at(expires_in)}

    def get_connections(self, user_id: str) -> list[dict[str, Any]]:
        client = _require_xero_client()
        store = _get_store(user_id)
        if TokenStore is not None:
            import asyncio

            state = asyncio.run(store.load())
        else:
            state = store.load()
        if not state:
            raise ValueError("Not authenticated.")
        with httpx.Client(timeout=30) as http:
            return client.get_connections(http, state.access_token)  # type: ignore[arg-type]

    def get_organization(self, user_id: str) -> dict[str, Any]:
        client = _require_xero_client()
        store = _get_store(user_id)
        if TokenStore is not None:
            import asyncio

            state = asyncio.run(store.load())
        else:
            state = store.load()
        if not state:
            raise ValueError("Not authenticated.")
        with httpx.Client(timeout=30) as http:
            return client.api_get(  # type: ignore[arg-type]
                http,
                state.access_token,
                state.tenant_id,
                "/api.xro/2.0/Organisation",
            )


def build_xero_tools(
    user_name: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Callable[[dict[str, Any]], Any]]]:
    def _user_id(args):
        return (args or {}).get("user_id") or os.getenv("XERO_USER_ID") or (user_name or "user")

    def xero_get_login_link(args):
        if _PYODIDE:
            return {"error": "Xero login requires server mode."}
        bridge = xero_mcp_bridge()
        return bridge.get_login_link(user_id=_user_id(args))

    def xero_auth_status(args):
        if _PYODIDE:
            return {"error": "Xero auth requires server mode."}
        bridge = xero_mcp_bridge()
        return bridge.auth_status(user_id=_user_id(args))

    def xero_refresh(args):
        if _PYODIDE:
            return {"error": "Xero auth requires server mode."}
        bridge = xero_mcp_bridge()
        return bridge.refresh(user_id=_user_id(args))

    def xero_get_connections(args):
        if _PYODIDE:
            return {"error": "Xero auth requires server mode."}
        bridge = xero_mcp_bridge()
        return bridge.get_connections(user_id=_user_id(args))

    def xero_get_organization(args):
        if _PYODIDE:
            return {"error": "Xero auth requires server mode."}
        bridge = xero_mcp_bridge()
        return bridge.get_organization(user_id=_user_id(args))

    tools = [
        _tool_def(
            "xero_get_login_link",
            "Return a Xero OAuth login URL for the user.",
            {"type": "object", "properties": {"user_id": {"type": "string"}}, "additionalProperties": False},
        ),
        _tool_def(
            "xero_auth_status",
            "Return authentication status for the current Xero user.",
            {"type": "object", "properties": {"user_id": {"type": "string"}}, "additionalProperties": False},
        ),
        _tool_def(
            "xero_refresh",
            "Refresh the stored Xero token for the user.",
            {"type": "object", "properties": {"user_id": {"type": "string"}}, "additionalProperties": False},
        ),
        _tool_def(
            "xero_get_connections",
            "List Xero connections (tenants) for the user.",
            {"type": "object", "properties": {"user_id": {"type": "string"}}, "additionalProperties": False},
        ),
        _tool_def(
            "xero_get_organization",
            "Fetch Xero organization details for the user.",
            {"type": "object", "properties": {"user_id": {"type": "string"}}, "additionalProperties": False},
        ),
    ]
    handlers = {
        "xero_get_login_link": xero_get_login_link,
        "xero_auth_status": xero_auth_status,
        "xero_refresh": xero_refresh,
        "xero_get_connections": xero_get_connections,
        "xero_get_organization": xero_get_organization,
    }
    return tools, handlers


def register_chat_tools(
    tools: list[dict[str, Any]],
    handlers: dict[str, Callable[[dict[str, Any]], Any]],
    *,
    user_name: str | None = None,
) -> None:
    extra_tools, extra_handlers = build_xero_tools(user_name=user_name)
    tools.extend(extra_tools)
    handlers.update(extra_handlers)


def attach_tools(chat_cls) -> None:
    if chat_cls is None:
        return

    def _user_id(self, args):
        return (args or {}).get("user_id") or os.getenv("XERO_USER_ID") or getattr(self, "_user_name", "user")

    def _wrap(func):
        def _handler(self, args):
            return func(args, self)
        return _handler

    def _login(args, self):
        if _PYODIDE:
            return {"error": "Xero login requires server mode."}
        return xero_mcp_bridge().get_login_link(user_id=_user_id(self, args))

    def _status(args, self):
        if _PYODIDE:
            return {"error": "Xero auth requires server mode."}
        return xero_mcp_bridge().auth_status(user_id=_user_id(self, args))

    def _refresh(args, self):
        if _PYODIDE:
            return {"error": "Xero auth requires server mode."}
        return xero_mcp_bridge().refresh(user_id=_user_id(self, args))

    def _connections(args, self):
        if _PYODIDE:
            return {"error": "Xero auth requires server mode."}
        return xero_mcp_bridge().get_connections(user_id=_user_id(self, args))

    def _organization(args, self):
        if _PYODIDE:
            return {"error": "Xero auth requires server mode."}
        return xero_mcp_bridge().get_organization(user_id=_user_id(self, args))

    def _add(name, func, description):
        handler = _wrap(func)
        _attach_tool(
            chat_cls,
            name,
            handler,
            description,
            {"type": "object", "properties": {"user_id": {"type": "string"}}, "additionalProperties": False},
        )

    _add("xero_get_login_link", _login, "Return a Xero OAuth login URL for the user.")
    _add("xero_auth_status", _status, "Return authentication status for the current Xero user.")
    _add("xero_refresh", _refresh, "Refresh the stored Xero token for the user.")
    _add("xero_get_connections", _connections, "List Xero connections (tenants) for the user.")
    _add("xero_get_organization", _organization, "Fetch Xero organization details for the user.")
