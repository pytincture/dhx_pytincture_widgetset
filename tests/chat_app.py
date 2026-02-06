"""Minimal Chat widget harness that streams responses from the backend."""

import copy
import os
import sys
from typing import Any, Optional, Set

from dhxpyt.layout import LayoutConfig, CellConfig, MainWindow
from dhxpyt.chat import (
    Chat,
    ChatConfig,
    ChatAgentConfig,
    ChatMessageConfig,
)

OpenAIProxy = None
try:
    from multiproxy import multiaiproxy as OpenAIProxy  # type: ignore
except Exception:  # pragma: no cover - fallback to legacy proxy
    try:
        from openaiproxy import openaiproxy as OpenAIProxy  # type: ignore
    except Exception:
        OpenAIProxy = None


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


SYSTEM_PROMPT = (
    "you can generate an html page. the way to create a viewable one is to wrap the html "
    "with this ::::Artifact Dashboard Snapshot | renderer=iframe | language=html\n"
    ". then after ::::Artifact to close it. Only generate when I ask for you to generate a page or similar remark"
)


class chatdemo(MainWindow):
    layout_config = LayoutConfig(
        type="line",
        rows=[CellConfig(id="chat", height="100%")],
    )

    def __init__(self):
        super().__init__()
        self.set_theme("dark")
        self._chat_widget: Optional[Chat] = None
        self._openai_proxy: Optional[Any] = None
        self._system_prompt = SYSTEM_PROMPT
        self._default_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self._user_name = os.getenv("CHATDEMO_USER", "You")
        self._cancelled_response_ids: Set[str] = set()
        self.load_ui()

    # ------------------------------------------------------------------
    # UI assembly
    # ------------------------------------------------------------------

    def load_ui(self) -> None:
        assistant = ChatAgentConfig(
            name="Atlas",
            subtitle="",
            tagline="",
            accent_color="#1e3a8a",
            avatar=os.getenv("CHATDEMO_ASSISTANT_AVATAR", "https://avatars.githubusercontent.com/u/6344670?v=4"),
        )

        user_avatar = os.getenv("CHATDEMO_USER_AVATAR", "https://avatars.githubusercontent.com/u/139426?v=4")
        assistant_avatar = assistant.avatar
        layout_mode = os.getenv("CHATDEMO_LAYOUT_MODE", "advanced")
        layout_density = os.getenv("CHATDEMO_LAYOUT_DENSITY", "comfortable")

        if OpenAIProxy is not None:
            try:
                self._openai_proxy = OpenAIProxy()
            except Exception as exc:  # pragma: no cover - diagnostic only
                print(f"[chat_app] Failed to initialise MultiAIProxy: {exc}")
                self._openai_proxy = None


        # UI controls can be toggled or styled from Python.
        ui_config = {
            "sidebar": {
                "newChat": {"icon": "forum", "tooltip": "Start a new chat"},
                "clearChats": {"icon": "delete_sweep", "tooltip": "Clear chats"},
                "toggleTheme": {"icon": "dark_mode", "tooltip": "Toggle dark mode", "show": True},
                "toggleSidebar": {
                    "icons": {"expanded": "chevron_left", "collapsed": "chevron_right"},
                    "tooltips": {"expanded": "Collapse sidebar", "collapsed": "Expand sidebar"},
                },
            },
            "header": {
                "demoButton": {"show": False},
                "toggleTheme": {"show": False},
            },
            "modelSelect": {"show": True},
        }

        available_models = [self._default_model]
        if self._openai_proxy:
            try:
                providers = self._openai_proxy.get_available_models()
                flat = []
                if isinstance(providers, dict):
                    for values in providers.values():
                        if isinstance(values, dict):
                            for nested in values.values():
                                if isinstance(nested, (list, tuple)):
                                    flat.extend(nested)
                        elif isinstance(values, (list, tuple)):
                            flat.extend(values)
                flat.append(self._default_model)
                available_models = sorted({model for model in flat if isinstance(model, str) and model})
            except Exception as exc:  # pragma: no cover - diagnostics only
                print(f"[chat_app] Unable to load model catalog: {exc}")

        models_config = copy.deepcopy(DEFAULT_PROVIDER_CONFIG)
        models_config.setdefault("providers", {})
        session_models = [model for model in available_models if isinstance(model, str) and model]
        if session_models:
            models_config["providers"]["session"] = session_models
        chat_config = ChatConfig(
            agent=assistant,
            messages=[],
            enable_artifacts=True,
            artifact_panel_width=420,
            streaming_debounce_ms=80,
            input_placeholder="Describe what you need…",
            send_button_text="Send",
            composer_max_height=240,
            storage_key="chatdemo_state_v1",
            extra={
                "models": available_models,
                "providerConfig": models_config,
                "ui": ui_config,
                "user": {"name": self._user_name, "avatar": user_avatar},
                "layout": {
                    "mode": layout_mode,
                    "density": layout_density,
                    "avatars": {
                        "user": user_avatar,
                        "assistant": assistant_avatar,
                    },
                },
            },
        )

        self._chat_widget = self.add_chat("chat", chat_config)
        self._chat_widget.on_send(self._handle_send)
        self._chat_widget.on_cancel(self._handle_cancel)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _handle_send(self, payload) -> None:
        """Stream responses from the backend for each submitted prompt."""
        if not self._chat_widget:
            return

        prompt = (payload or {}).get("text", "").strip()
        if not prompt:
            return

        print(f"[chat_app] on_send received prompt: {prompt}")

        assistant_message = ChatMessageConfig(
            role="assistant",
            name="Atlas",
            content="",
            streaming=True,
        )

        response_id = self._chat_widget.start_stream(assistant_message)
        self._cancelled_response_ids.discard(response_id)

        if not self._openai_proxy:
            warning = (
                "Backend connection is not available. Configure OPENAI_API_KEY and restart the service."
            )
            self._chat_widget.append_stream(response_id, warning)
            self._chat_widget.finish_stream(response_id)
            return True

        self._call_bff_backend(prompt, response_id)
        return True

    def _handle_cancel(self, payload) -> None:
        if not payload:
            return True
        message_id = payload.get("messageId")
        if message_id:
            self._cancelled_response_ids.add(message_id)
        return True

    def _call_bff_backend(self, prompt: str, response_id: str) -> None:
        if not self._chat_widget or not self._openai_proxy:
            return

        context = self._chat_widget.build_history(
            system_prompt=self._system_prompt,
            exclude_ids={response_id},
        )
        if not any(msg.get("role") == "user" and msg.get("content") == prompt for msg in context):
            context.append({"role": "user", "content": prompt})

        selected_model = None
        if self._chat_widget and hasattr(self._chat_widget, "get_chats"):
            try:
                chats = self._chat_widget.get_chats()
                active = next((chat for chat in chats if chat.get("isActive")), None)
                if active:
                    selected_model = active.get("model")
            except Exception as exc:  # pragma: no cover - diagnostics only
                print(f"[chat_app] Unable to determine active model: {exc}")

        def _extract_text(chunk):
            if chunk is None:
                return ""
            if isinstance(chunk, str):
                return chunk
            payload = chunk
            if hasattr(payload, "model_dump"):
                payload = payload.model_dump(exclude_none=True)
            elif hasattr(payload, "to_dict"):
                payload = payload.to_dict()
            if isinstance(payload, str):
                return payload
            if not isinstance(payload, dict):
                return ""
            if "error" in payload:
                error = payload.get("error") or {}
                return error.get("message") or ""
            choices = payload.get("choices") or []
            for choice in choices:
                delta = (choice or {}).get("delta")
                if isinstance(delta, dict):
                    content = delta.get("content")
                    if isinstance(content, str):
                        return content
                    if isinstance(content, list):
                        parts = []
                        for item in content:
                            if isinstance(item, str):
                                parts.append(item)
                            elif isinstance(item, dict):
                                text = item.get("text") or item.get("content")
                                if isinstance(text, str):
                                    parts.append(text)
                        return "".join(parts)
                    text = delta.get("text")
                    if isinstance(text, str):
                        return text
                message = (choice or {}).get("message")
                if isinstance(message, dict):
                    content = message.get("content")
                    if isinstance(content, str):
                        return content
            content = payload.get("content")
            if isinstance(content, str):
                return content
            return ""

        stream = self._openai_proxy.chat_stream(
            context,
            model=selected_model or self._default_model,
        )
        try:
            self._chat_widget.consume_stream(
                response_id,
                stream,
                parser=_extract_text,
                cancel_check=lambda: response_id in self._cancelled_response_ids,
            )
        except TypeError:
            self._chat_widget.consume_stream(
                response_id,
                stream,
                parser=_extract_text,
            )



if __name__ == "__main__" and sys.platform != "emscripten":
    from pytincture import launch_service
    launch_service(modules_folder=".")
