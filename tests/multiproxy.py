"""Backend-for-frontend proxy for multi-provider AI chat APIs.

This module integrates LiteLLM to support OpenAI, Anthropic, AWS Bedrock, xAI
Grok, and Google Gemini through a unified streaming interface while maintaining
PyTincture compatibility.
"""

import json
import os
import sys
import types
import time
import hashlib
from datetime import datetime

import litellm

# Ensure the module is registered for inspect.getfile when loaded via SourceFileLoader.
if __name__ not in sys.modules:
    module_stub = types.ModuleType(__name__)
    module_stub.__file__ = __file__
    sys.modules[__name__] = module_stub
elif not getattr(sys.modules[__name__], "__file__", None):
    sys.modules[__name__].__file__ = __file__

from pytincture.dataclass import backend_for_frontend, bff_stream

# ---------------------------------------------------------------------------
# Defaults (can be overridden when instantiating the proxy)
# ---------------------------------------------------------------------------

DEFAULT_PROVIDER_CONFIG = {
    "providers": {
        "aws_bedrock": {
            "anthropic": [
                "us.anthropic.claude-sonnet-4-20250514-v1:0",
                "us.anthropic.claude-opus-4-20250514-v1:0",
                "us.anthropic.claude-opus-4-1-20250805-v1:0",
                "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            ],
            "meta": [
                "us.meta.llama3-3-70b-instruct-v1:0",
                "us.meta.llama4-maverick-17b-instruct-v1:0",
                "us.meta.llama4-scout-17b-instruct-v1:0",
            ],
            "amazon": [
                "us.amazon.nova-pro-v1:0",
                "us.amazon.nova-premier-v1:0",
                "us.amazon.nova-micro-v1:0",
                "us.amazon.nova-lite-v1:0",
            ],
        },
        "anthropic": [
            "claude-sonnet-4-20250514",
            "claude-opus-4-20250514",
            "claude-opus-4-1-20250805",
            "claude-3-7-sonnet-latest",
            "claude-3-5-sonnet-latest",
        ],
        "openai": [
            "gpt-5",
            "gpt-5-mini",
            "o4-mini",
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1",
            "gpt-4.1-mini",
            "o3",
            "o3-mini",
            "o1",
            "o1-mini",
            "chatgpt-4o-latest",
            "gpt-3.5-turbo",
        ],
        "xai": [
            "xai/grok-3-mini-beta",
            "xai/grok-3-beta",
            "xai/grok-2",
            "xai/grok-2-mini",
        ],
        "google": [
            "gemini-pro",
            "gemini-pro-vision",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
        ],
    }
}

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "60"))
DEBUG_STREAM = os.getenv("MULTIPROXY_DEBUG_STREAM", "").lower() in {"1", "true", "yes"}
DEBUG_TOOLS = os.getenv("MULTIPROXY_DEBUG_TOOLS", "").lower() in {"1", "true", "yes"}
ENABLE_MCP = os.getenv("MULTIPROXY_ENABLE_MCP", "true").lower() in {"1", "true", "yes"}

try:
    import httpx
except Exception:  # pragma: no cover
    httpx = None

MCP_SERVERS = {
    "browser-api": {
        "url": "https://browser-api.fly.dev/mcp",
        "timeout": 30.0,
        "headers": {},
    },
    "accountesi-mcp": {
        "url": "https://accountesi-mcp.fly.dev/mcp",
        "timeout": 30.0,
        "headers": {"x-user-id": "{{USER_ID}}"},
    },
}

# ---------------------------------------------------------------------------
# LiteLLM provider helpers
# ---------------------------------------------------------------------------


class UnifiedAIProvider:
    """Unified AI provider using LiteLLM for multi-provider support."""

    def __init__(self, provider_config):
        self.provider_config = provider_config or {"providers": {}}
        self.setup_environment()
        self._build_model_mapping()

    @staticmethod
    def setup_environment() -> None:
        """Populate LiteLLM environment variables from existing env vars."""

        env_mappings = {
            "OPENAI_API_KEY": "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY": "ANTHROPIC_API_KEY",
            "GOOGLE_KEY": "GEMINI_API_KEY",
            "XAI_API_KEY": "XAI_API_KEY",
            "AWS_ACCESS_KEY_ID": "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY": "AWS_SECRET_ACCESS_KEY",
            "AWS_DEFAULT_REGION": "AWS_DEFAULT_REGION",
        }

        for source_var, target_var in env_mappings.items():
            value = os.getenv(source_var)
            if value and not os.getenv(target_var):
                os.environ[target_var] = value

    def _build_model_mapping(self):
        providers = self.provider_config.get("providers", {})
        self.model_mapping = {}

        bedrock = providers.get("aws_bedrock", {})
        for provider_type, models in bedrock.items():
            for model in models:
                litellm_name = self._map_bedrock_model(provider_type, model)
                self.model_mapping[model] = litellm_name

        for provider, models in providers.items():
            if provider == "aws_bedrock":
                continue
            for model in models:
                self.model_mapping[model] = self._map_direct_model(provider, model)

    @staticmethod
    def _map_bedrock_model(provider_type, model):
        prefix_map = {
            "anthropic": "anthropic.",
            "meta": "meta.",
            "amazon": "amazon.",
        }
        prefix = prefix_map.get(provider_type)
        if prefix:
            clean = model.replace(f"us.{provider_type}.", prefix)
            return f"bedrock/{clean}"
        return f"bedrock/{model}"

    @staticmethod
    def _map_direct_model(provider, model):
        if provider == "openai" or provider == "xai":
            return model
        if provider == "google":
            return f"gemini/{model}"
        return f"{provider}/{model}"

    def get_litellm_model(self, model):
        return self.model_mapping.get(model, model)

    def is_xai_model(self, model):
        providers = self.provider_config.get("providers", {})
        if model.startswith("xai/"):
            return True
        return model in providers.get("xai", []) or model.startswith("grok")

    def stream_completion(self, model, messages, **kwargs):
        litellm_model = self.get_litellm_model(model)

        if self.is_xai_model(model):
            original_base_url = os.getenv("OPENAI_BASE_URL")
            os.environ["OPENAI_BASE_URL"] = "https://api.x.ai/v1"
            try:
                response = litellm.completion(
                    model=litellm_model,
                    messages=list(messages),
                    stream=True,
                    api_key=os.getenv("XAI_API_KEY"),
                    **kwargs,
                )
                for chunk in response:
                    yield chunk
            finally:
                if original_base_url is not None:
                    os.environ["OPENAI_BASE_URL"] = original_base_url
                elif "OPENAI_BASE_URL" in os.environ:
                    del os.environ["OPENAI_BASE_URL"]
        else:
            response = litellm.completion(
                model=litellm_model,
                messages=list(messages),
                stream=True,
                **kwargs,
            )
            for chunk in response:
                yield chunk

    def complete(self, model, messages, **kwargs):
        litellm_model = self.get_litellm_model(model)

        if self.is_xai_model(model):
            original_base_url = os.getenv("OPENAI_BASE_URL")
            os.environ["OPENAI_BASE_URL"] = "https://api.x.ai/v1"
            try:
                return litellm.completion(
                    model=litellm_model,
                    messages=list(messages),
                    stream=False,
                    api_key=os.getenv("XAI_API_KEY"),
                    **kwargs,
                )
            finally:
                if original_base_url is not None:
                    os.environ["OPENAI_BASE_URL"] = original_base_url
                elif "OPENAI_BASE_URL" in os.environ:
                    del os.environ["OPENAI_BASE_URL"]

        return litellm.completion(
            model=litellm_model,
            messages=list(messages),
            stream=False,
            **kwargs,
        )


# ---------------------------------------------------------------------------
# Backend-for-frontend proxy
# ---------------------------------------------------------------------------


@backend_for_frontend
class multiaiproxy:
    """Multi-provider AI proxy supporting OpenAI, Anthropic, Bedrock, xAI, and Google."""

    def __init__(self, *, provider_config=None, default_model=None, timeout=None):
        config = provider_config or self._load_config_from_env() or DEFAULT_PROVIDER_CONFIG
        self._provider = UnifiedAIProvider(config)
        self._provider_config = config
        self._default_model = default_model or os.getenv("DEFAULT_MODEL", DEFAULT_MODEL)
        self._timeout = timeout or REQUEST_TIMEOUT
        self._tool_handlers = {}
        self._register_builtin_tools()
        self._mcp_tools_loaded = False
        self._mcp_tools = []
        self._mcp_sessions = {}
        self._current_tool_names = []
        self._mcp_tool_name_map = {}

    @staticmethod
    def _normalize_stream_chunk(chunk):
        if chunk is None:
            return None

        payload = chunk
        if hasattr(payload, "model_dump"):
            payload = payload.model_dump(exclude_none=True)
        elif hasattr(payload, "dict"):
            payload = payload.dict(exclude_none=True)

        if isinstance(payload, (bytes, bytearray)):
            payload = payload.decode("utf-8", errors="replace")

        if isinstance(payload, str):
            text = payload.strip()
            if not text or text == "[DONE]":
                return None
            if text.startswith("data:"):
                text = text[5:].strip()
                if text == "[DONE]":
                    return None
                try:
                    payload = json.loads(text)
                except json.JSONDecodeError:
                    return {"choices": [{"delta": {"content": text}}]}
            else:
                return {"choices": [{"delta": {"content": text}}]}

        if not isinstance(payload, dict):
            return None

        if payload.get("type") == "content.delta":
            delta = payload.get("delta")
            if isinstance(delta, dict):
                text = delta.get("content") or delta.get("text") or ""
            else:
                text = delta or ""
            if text:
                return {"choices": [{"delta": {"content": text}}]}
            return None

        if "choices" not in payload:
            if "delta" in payload:
                delta = payload.get("delta")
                if isinstance(delta, dict):
                    text = delta.get("content") or delta.get("text") or ""
                else:
                    text = delta or ""
                if text:
                    return {"choices": [{"delta": {"content": text}}]}
            elif "content" in payload:
                text = payload.get("content")
                if isinstance(text, str) and text:
                    return {"choices": [{"delta": {"content": text}}]}

        return payload

    @staticmethod
    def _load_config_from_env():
        raw = os.getenv("MULTIPROXY_PROVIDER_CONFIG")
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("Warning: MULTIPROXY_PROVIDER_CONFIG is not valid JSON; falling back to defaults.")
            return None

    def get_available_models(self):
        return self._provider_config.get("providers", {})

    def get_model_info(self, model):
        litellm_name = self._provider.get_litellm_model(model)
        provider = "unknown"
        providers = self._provider_config.get("providers", {})

        if model in providers.get("openai", []):
            provider = "openai"
        elif model in providers.get("anthropic", []):
            provider = "anthropic"
        elif model in providers.get("xai", []):
            provider = "xai"
        elif model in providers.get("google", []):
            provider = "google"
        elif any(model in group for group in providers.get("aws_bedrock", {}).values()):
            provider = "aws_bedrock"

        return {
            "original_name": model,
            "litellm_name": litellm_name,
            "provider": provider,
            "supported": model in self._provider.model_mapping,
        }

    def register_tools(self, *, tool_handlers=None):
        if isinstance(tool_handlers, dict):
            self._tool_handlers.update(tool_handlers)

    def _register_builtin_tools(self):
        def _now():
            return datetime.now().astimezone()

        self._tool_handlers.setdefault(
            "get_current_datetime",
            lambda _args: {
                "iso": _now().isoformat(),
                "date": _now().strftime("%Y-%m-%d"),
                "time": _now().strftime("%H:%M:%S"),
                "timezone": str(_now().tzinfo),
            },
        )
        self._tool_handlers.setdefault(
            "get_current_date",
            lambda _args: {"date": _now().strftime("%Y-%m-%d")},
        )
        self._tool_handlers.setdefault(
            "get_current_time",
            lambda _args: {"time": _now().strftime("%H:%M:%S")},
        )
        self._tool_handlers.setdefault(
            "get_unix_timestamp",
            lambda _args: {"timestamp": int(_now().timestamp())},
        )
        self._tool_handlers.setdefault(
            "get_timezone",
            lambda _args: {"timezone": str(_now().tzinfo)},
        )
        self._tool_handlers.setdefault(
            "echo",
            lambda args: {"message": (args or {}).get("message", "")},
        )
        self._tool_handlers.setdefault(
            "list_available_tools",
            lambda _args: {"tools": list(self._current_tool_names)},
        )

    def _mcp_user_id(self):
        return (
            os.getenv("MCP_USER_ID")
            or os.getenv("XERO_USER_ID")
            or os.getenv("MULTIPROXY_MCP_USER_ID")
            or "demo-user"
        )

    def _mcp_headers(self, template, session_id=None):
        user_id = self._mcp_user_id()
        headers = {
            "accept": "application/json, application/*+json, text/event-stream, */*",
            "content-type": "application/json; charset=utf-8",
            "user-agent": "dhxpyt-mcp-bridge/1.0",
        }
        if session_id:
            headers["mcp-session-id"] = session_id
        for key, value in (template or {}).items():
            headers[key] = value.replace("{{USER_ID}}", user_id)
        return headers

    def _mcp_request(self, url, headers, method, params=None, timeout=None, server_key=None):
        if httpx is None:
            raise RuntimeError("httpx is not available for MCP calls.")
        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),
            "method": method,
        }
        if params:
            payload["params"] = params
        urls = [url, url.rstrip("/") + "/"] if not url.endswith("/") else [url, url.rstrip("/")]
        last_exc = None
        for attempt, target in enumerate(urls, start=1):
            try:
                with httpx.Client(timeout=timeout or 30.0) as client:
                    resp = client.post(target, json=payload, headers=headers)
                    if resp.status_code in {400, 406}:
                        raise httpx.HTTPStatusError(
                            f"{resp.status_code} {resp.text[:200]}",
                            request=resp.request,
                            response=resp,
                        )
                    resp.raise_for_status()
                    content_type = resp.headers.get("content-type", "")
                    if "json" in content_type:
                        data = resp.json()
                    elif "text/event-stream" in content_type:
                        data = self._parse_sse_json(resp.text)
                    else:
                        raise RuntimeError(f"Non-JSON response: {content_type} {resp.text[:200]}")
                    session_header = resp.headers.get("mcp-session-id") or resp.headers.get("x-mcp-session-id")
                    if session_header and server_key:
                        self._mcp_sessions[server_key] = session_header
                if isinstance(data, dict) and "error" in data:
                    raise RuntimeError(data["error"])
                return data.get("result") if isinstance(data, dict) else data
            except httpx.HTTPStatusError as exc:
                last_exc = exc
                if attempt == len(urls):
                    raise
            except Exception as exc:
                last_exc = exc
                if attempt == len(urls):
                    raise
        if last_exc:
            raise last_exc

    @staticmethod
    def _parse_sse_json(text: str):
        for line in text.splitlines():
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload:
                continue
            try:
                return json.loads(payload)
            except Exception:
                continue
        raise RuntimeError(f"Non-JSON response: text/event-stream {text[:200]}")

    def _ensure_mcp_session(self, server_key, server):
        if self._mcp_sessions.get(server_key):
            return
        headers = self._mcp_headers(server.get("headers") or {})
        versions = [
            server.get("protocolVersion"),
            os.getenv("MCP_PROTOCOL_VERSION"),
            "2024-11-05",
            "2024-05-14",
            "2024-03-26",
        ]
        versions = [version for version in versions if version]
        last_exc = None
        for version in versions:
            params = {
                "protocolVersion": version,
                "clientInfo": {"name": "dhxpyt-mcp-bridge", "version": "0.1"},
                "capabilities": {},
            }
            try:
                result = self._mcp_request(
                    server["url"],
                    headers,
                    "initialize",
                    params=params,
                    timeout=server.get("timeout") or 30.0,
                    server_key=server_key,
                )
                if isinstance(result, dict):
                    session_id = result.get("sessionId") or result.get("session_id")
                    if session_id:
                        self._mcp_sessions[server_key] = session_id
                        return
            except Exception as exc:
                last_exc = exc
        if DEBUG_TOOLS:
            print(f"[multiproxy] MCP init failed {server_key}: {last_exc}")

    def _mcp_list_tools(self, server):
        server_key = server.get("name") or "server"
        self._ensure_mcp_session(server_key, server)
        session_id = self._mcp_sessions.get(server_key)
        headers = self._mcp_headers(server.get("headers") or {}, session_id=session_id)
        result = self._mcp_request(
            server["url"],
            headers,
            "tools/list",
            params={},
            timeout=server.get("timeout") or 30.0,
            server_key=server_key,
        ) or []
        if isinstance(result, dict) and "tools" in result:
            return result.get("tools") or []
        if isinstance(result, list):
            return result
        return []

    def _mcp_call_tool(self, server, tool_name, arguments):
        server_key = server.get("name") or "server"
        self._ensure_mcp_session(server_key, server)
        session_id = self._mcp_sessions.get(server_key)
        headers = self._mcp_headers(server.get("headers") or {}, session_id=session_id)
        params = {"name": tool_name, "arguments": arguments or {}}
        return self._mcp_request(
            server["url"],
            headers,
            "tools/call",
            params,
            timeout=server.get("timeout") or 30.0,
            server_key=server_key,
        )

    def _ensure_mcp_tools(self):
        if self._mcp_tools_loaded or not ENABLE_MCP:
            return
        self._mcp_tools_loaded = True
        loaded_any = False
        for server_name, server in MCP_SERVERS.items():
            server = dict(server)
            server["name"] = server_name
            try:
                tool_list = self._mcp_list_tools(server)
            except Exception as exc:
                print(f"[multiproxy] MCP list failed {server_name}: {exc}")
                continue
            loaded_any = loaded_any or bool(tool_list)
            print(f"[multiproxy] MCP tools {server_name}: {len(tool_list)}")
            for tool in tool_list:
                raw_name = tool.get("name")
                if not raw_name:
                    continue
                tool_name = self._mcp_tool_name(server_name, raw_name)
                input_schema = tool.get("inputSchema") or {"type": "object", "properties": {}}
                self._mcp_tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "description": tool.get("description")
                            or f"MCP tool {raw_name} ({server_name})",
                            "parameters": input_schema,
                        },
                    }
                )

                def _make_handler(server_cfg, mcp_tool_name):
                    def _handler(args):
                        return self._mcp_call_tool(server_cfg, mcp_tool_name, args or {})

                    return _handler

                self._tool_handlers[tool_name] = _make_handler(server, raw_name)
        if not loaded_any:
            print("[multiproxy] MCP enabled but no tools loaded from any server.")

    def _mcp_tool_name(self, server_name, raw_name):
        base = f"mcp_{server_name.replace('-', '_')}__{raw_name}"
        if len(base) <= 64:
            return base
        digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]
        prefix = f"mcp_{server_name.replace('-', '_')}__"
        short = f"{prefix}{digest}"
        self._mcp_tool_name_map[short] = base
        return short

    @bff_stream()
    def chat_stream(self, messages, model=None, **extra):
        options = extra.copy()
        timeout_override = options.pop("timeout", None)
        options.pop("stream", None)
        tool_handler = options.pop("tool_handler", None)
        tool_choice_override = options.pop("tool_choice", None)
        timeout = timeout_override or self._timeout

        selected_model = model or self._default_model

        if selected_model not in self._provider.model_mapping:
            raise ValueError(
                f"Model '{selected_model}' is not supported. Available models: {list(self._provider.model_mapping.keys())}"
            )

        tools = options.pop("tools", None)
        enable_tools = options.pop("enable_tools", True)
        if not enable_tools:
            tools = None

        try:
            tool_used = False
            if ENABLE_MCP:
                if not self._mcp_tools_loaded or not self._mcp_tools:
                    self._ensure_mcp_tools()
                if self._mcp_tools:
                    tools = (tools or []) + list(self._mcp_tools)
                elif DEBUG_TOOLS:
                    print("[multiproxy] MCP enabled but no tools loaded.")
            list_tool_def = {
                "type": "function",
                "function": {
                    "name": "list_available_tools",
                    "description": "Return the names of all available tools.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False,
                    },
                },
            }
            if tools is None:
                tools = []
            if not any(t.get("function", {}).get("name") == "list_available_tools" for t in tools):
                tools = list(tools) + [list_tool_def]
            self._current_tool_names = [
                t.get("function", {}).get("name") for t in tools if t.get("function", {}).get("name")
            ]
            if tools:
                tool_choice = tool_choice_override or self._infer_tool_choice(messages, tools) or "auto"
                tool_result, tool_used = self._maybe_run_tools(
                    messages=messages,
                    model=selected_model,
                    timeout=timeout,
                    tools=tools,
                    tool_choice=tool_choice,
                    options=options,
                    tool_handler=tool_handler,
                )
                if tool_result is not None:
                    messages = tool_result
            tools_for_stream = None if tool_used else tools
            tool_choice_for_stream = None if tools_for_stream is None else (tool_choice_override or "auto")

            yielded_any = False
            for chunk in self._provider.stream_completion(
                model=selected_model,
                messages=messages,
                timeout=timeout,
                tools=tools_for_stream,
                tool_choice=tool_choice_for_stream,
                **options,
            ):
                if DEBUG_STREAM:
                    print(f"[multiproxy] raw chunk: {type(chunk)!r} {chunk!r}")
                normalized = self._normalize_stream_chunk(chunk)
                if DEBUG_STREAM:
                    print(f"[multiproxy] normalized: {normalized!r}")
                if normalized is not None:
                    yielded_any = True
                    yield normalized
            if not yielded_any:
                response = self._provider.complete(
                    model=selected_model,
                    messages=messages,
                    timeout=timeout,
                    tools=tools_for_stream,
                    tool_choice=tool_choice_for_stream,
                    **options,
                )
                payload = response
                if hasattr(payload, "model_dump"):
                    payload = payload.model_dump(exclude_none=True)
                elif hasattr(payload, "dict"):
                    payload = payload.dict(exclude_none=True)
                text = ""
                if isinstance(payload, dict):
                    for choice in payload.get("choices") or []:
                        message = (choice or {}).get("message") or {}
                        if isinstance(message, dict):
                            text = message.get("content") or ""
                        if text:
                            break
                if text:
                    yield {"choices": [{"delta": {"content": text}}]}
        except Exception as exc:  # pragma: no cover - provider errors
            yield {
                "error": {
                    "message": str(exc),
                    "type": "provider_error",
                    "code": "stream_error",
                }
            }

    @staticmethod
    def _infer_tool_choice(messages, tools):
        if not messages:
            return None
        last_user = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user = (msg.get("content") or "").lower()
                break
        if not last_user:
            return None
        names = {tool.get("function", {}).get("name") for tool in tools}
        def _use(name):
            if name in names:
                return {"type": "function", "function": {"name": name}}
            return None
        if "timezone" in last_user or "time zone" in last_user:
            return _use("get_timezone")
        if "timestamp" in last_user or "unix" in last_user:
            return _use("get_unix_timestamp")
        if "date" in last_user or "today" in last_user:
            if "time" in last_user:
                return _use("get_current_datetime") or _use("get_current_time")
            return _use("get_current_date")
        if "time" in last_user:
            return _use("get_current_time")
        if any(token in last_user for token in ("what tools", "list tools", "show tools", "tools do you")):
            return _use("list_available_tools")
        return None

    @bff_stream()
    def chat_stream_with_provider_info(self, messages, model=None, **extra):
        model_info = self.get_model_info(model or self._default_model)
        yield {"type": "model_info", "model_info": model_info}
        for chunk in self.chat_stream(messages, model, **extra):
            if isinstance(chunk, dict) and "error" not in chunk:
                chunk["provider"] = model_info["provider"]
            yield chunk

    # ------------------------------------------------------------------
    # Tools
    # ------------------------------------------------------------------

    def _run_tool(self, name, arguments, tool_handler=None):
        handler = None
        raw_name = name or ""
        if isinstance(tool_handler, dict):
            handler = tool_handler.get(raw_name)
        elif tool_handler is None:
            handler = self._tool_handlers.get(raw_name)
        if callable(tool_handler) and handler is None:
            try:
                handler = tool_handler(raw_name)
            except Exception:
                handler = None
        if handler is None:
            candidate = raw_name
            if candidate.startswith("functions."):
                candidate = candidate.split(".", 1)[1]
            if candidate.startswith("function."):
                candidate = candidate.split(".", 1)[1]
            normalized = "".join(ch for ch in candidate.lower() if ch.isalnum())
            if normalized:
                combined = {}
                if isinstance(tool_handler, dict):
                    combined.update(tool_handler)
                combined.update(self._tool_handlers)
                for tool_name, tool_func in combined.items():
                    key = "".join(ch for ch in str(tool_name).lower() if ch.isalnum())
                    if key == normalized:
                        handler = tool_func
                        break
        if callable(handler):
            try:
                return json.dumps(handler(arguments or {}))
            except Exception as exc:
                return json.dumps({"error": str(exc)})
        return json.dumps({"error": f"Unknown tool: {name}"})

    def _maybe_run_tools(self, *, messages, model, timeout, tools, tool_choice, options, tool_handler):
        if DEBUG_TOOLS:
            try:
                tool_names = [tool.get("function", {}).get("name") for tool in tools]
                print(f"[multiproxy] tools preflight: {tool_names} tool_choice={tool_choice!r}")
            except Exception:
                print("[multiproxy] tools preflight: unable to list tools")
        response = self._provider.complete(
            model=model,
            messages=list(messages),
            timeout=timeout,
            tools=tools,
            tool_choice=tool_choice,
            **options,
        )
        payload = response
        if hasattr(payload, "model_dump"):
            payload = payload.model_dump(exclude_none=True)
        elif hasattr(payload, "dict"):
            payload = payload.dict(exclude_none=True)
        if not isinstance(payload, dict):
            return None, False
        choices = payload.get("choices") or []
        if not choices:
            return None, False
        message = (choices[0] or {}).get("message") or {}
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            function_call = message.get("function_call") or {}
            if isinstance(function_call, dict) and function_call.get("name"):
                tool_calls = [
                    {
                        "id": None,
                        "function": {
                            "name": function_call.get("name"),
                            "arguments": function_call.get("arguments") or "{}",
                        },
                    }
                ]
        if not tool_calls:
            return None, False
        if DEBUG_TOOLS:
            try:
                called = [call.get("function", {}).get("name") for call in tool_calls]
                print(f"[multiproxy] tool_calls: {called}")
            except Exception:
                print("[multiproxy] tool_calls: unable to read")
        tool_messages = []
        for call in tool_calls:
            if not isinstance(call, dict):
                continue
            call_id = call.get("id")
            function = call.get("function") or {}
            name = function.get("name")
            arguments = function.get("arguments") or "{}"
            if not name:
                continue
            try:
                parsed_args = json.loads(arguments) if isinstance(arguments, str) else arguments
            except json.JSONDecodeError:
                parsed_args = {}
            if DEBUG_TOOLS:
                print(f"[multiproxy] running tool: {name} args={parsed_args}")
            result = self._run_tool(name, parsed_args, tool_handler=tool_handler)
            tool_messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": result,
                }
            )
        if not tool_messages:
            return None, False
        combined = list(messages)
        combined.append(message)
        combined.extend(tool_messages)
        return combined, True


# Backwards compatibility alias expected by existing demos
openaiproxy = multiaiproxy
