"""Minimal Chat widget harness that streams responses from the backend."""

import os
import sys
from typing import Any, Optional

from dhxpyt.layout import LayoutConfig, CellConfig, MainWindow
from dhxpyt.chat import (
    Chat,
    ChatConfig,
    ChatAgentConfig,
    ChatMessageConfig,
)

try:
    from openaiproxy import openaiproxy as OpenAIProxy
except Exception:  # pragma: no cover - stub may not exist during tests
    OpenAIProxy = None


SYSTEM_PROMPT = (
    "you can generate an html page. the way to create a viewable one is to wrap the html "
    "with this :::Artifact Dashboard Snapshot | renderer=iframe | language=html\n"
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
            "modelSelect": {"show": False},
        }

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
                "models": [self._default_model],
                "ui": ui_config,
                "user": {"name": self._user_name, "avatar": user_avatar},
                "layout": {
                    "mode": layout_mode,
                    "avatars": {
                        "user": user_avatar,
                        "assistant": assistant_avatar,
                    },
                },
            },
        )

        self._chat_widget = self.add_chat("chat", chat_config)
        self._chat_widget.on_send(self._handle_send)

        if OpenAIProxy is not None:
            try:
                self._openai_proxy = OpenAIProxy()
            except Exception as exc:  # pragma: no cover - diagnostic only
                print(f"[chat_app] Failed to initialise OpenAIProxy: {exc}")
                self._openai_proxy = None

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

        if not self._openai_proxy:
            warning = (
                "Backend connection is not available. Configure OPENAI_API_KEY and restart the service."
            )
            self._chat_widget.append_stream(response_id, warning)
            self._chat_widget.finish_stream(response_id)
            return True

        self._call_bff_backend(prompt, response_id)
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

        stream = self._openai_proxy.chat_stream(context, model=self._default_model)
        self._chat_widget.consume_stream(response_id, stream)



if __name__ == "__main__" and sys.platform != "emscripten":
    from pytincture import launch_service
    launch_service(modules_folder=".")
