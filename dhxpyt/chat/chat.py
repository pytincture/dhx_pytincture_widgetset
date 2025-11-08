import json
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import js
from pyodide.ffi import create_proxy

from .chat_config import ChatConfig, ChatAgentConfig, ChatMessageConfig


logger = logging.getLogger(__name__)
WRAPPER_REVISION = "chat-wrapper/2024-03-01"
logger.info("Chat widget wrapper loaded (%s)", WRAPPER_REVISION)
print(f"[ChatWidget] Wrapper ready ({WRAPPER_REVISION})")


class Chat:
    """
    Python wrapper around the custom Chat widget.
    """

    def __init__(
        self,
        config: Optional[ChatConfig] = None,
        *,
        container: Any = None,
        root: Optional[Union[str, Any]] = None,
    ) -> None:
        if container is None and root is None:
            raise ValueError("Chat widget requires a container or a root element.")

        self.config = config or ChatConfig()
        self._container = container
        self._event_proxies: Dict[str, List[Any]] = {}

        root_element = self._resolve_root(container=container, root=root)
        if root_element is None:
            raise RuntimeError("Unable to resolve root element for Chat widget.")

        config_payload = self.config.to_dict()
        config_json = json.dumps(config_payload)
        config_options = js.JSON.parse(config_json)
        self.chat = js.customdhx.ChatWidget.new(root_element, config_options)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _js_class() -> Any:
        try:
            return js.customdhx.ChatWidget
        except AttributeError as exc:
            raise RuntimeError(
                "customdhx.ChatWidget is not available. Ensure the chat JavaScript bundle has been loaded."
            ) from exc

    def _resolve_root(self, *, container: Any, root: Optional[Union[str, Any]]) -> Any:
        if container is not None:
            return container
        if isinstance(root, str):
            return js.document.querySelector(root)
        return root

    def _bind_event(self, event_name: str, handler: Callable) -> None:
        def wrapped(*args, **kwargs):
            converted = [
                arg.to_py() if hasattr(arg, "to_py") else arg
                for arg in args
            ]
            return handler(*converted, **kwargs)

        proxy = create_proxy(wrapped)
        bucket = self._event_proxies.setdefault(event_name, [])
        bucket.append(proxy)
        self.chat.on(event_name, proxy)

    # ------------------------------------------------------------------
    # Event binding API
    # ------------------------------------------------------------------

    def on_send(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        """
        Fired when the user submits a prompt from the composer.
        Handler receives a payload with message text and identifiers.
        """
        self._bind_event("send", handler)

    def on_artifact_save(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        """
        Fired when the user requests to save/download an artifact.
        """
        self._bind_event("artifact:save", handler)

    def on_artifact_load(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        """
        Fired after a user picks a file to load into the artifact preview pane.
        """
        self._bind_event("artifact:load", handler)

    def on_copy(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        """
        Fired when the user clicks the per-message copy button.
        """
        self._bind_event("copy", handler)

    # ------------------------------------------------------------------
    # Data operations
    # ------------------------------------------------------------------

    @staticmethod
    def _message_to_dict(
        message: Union[ChatMessageConfig, Dict[str, Any]]
    ) -> Dict[str, Any]:
        if hasattr(message, "to_dict"):
            return message.to_dict()
        if isinstance(message, dict):
            return message
        raise TypeError(f"Unsupported chat message type: {type(message)!r}")

    def set_messages(
        self, messages: Iterable[Union[ChatMessageConfig, Dict[str, Any]]]
    ) -> None:
        payload = [self._message_to_dict(message) for message in messages]
        self.chat.setMessages(js.JSON.parse(json.dumps(payload)))

    def add_message(
        self, message: Union[ChatMessageConfig, Dict[str, Any]]
    ) -> str:
        payload = self._message_to_dict(message)
        result = self.chat.addMessage(js.JSON.parse(json.dumps(payload)))
        return result.to_py() if hasattr(result, "to_py") else result

    def update_message(self, message_id: str, **updates: Any) -> None:
        self.chat.updateMessage(
            message_id,
            js.JSON.parse(json.dumps(updates))
        )

    def remove_message(self, message_id: str) -> None:
        if hasattr(self.chat, "removeMessage"):
            self.chat.removeMessage(message_id)

    def clear_messages(self) -> None:
        self.chat.clearMessages()

    # ------------------------------------------------------------------
    # Streaming helpers
    # ------------------------------------------------------------------

    def start_stream(
        self,
        message: Union[ChatMessageConfig, Dict[str, Any]],
    ) -> str:
        payload = self._message_to_dict(message)
        result = self.chat.startStream(js.JSON.parse(json.dumps(payload)))
        return result.to_py() if hasattr(result, "to_py") else result

    def append_stream(self, message_id: str, chunk: str) -> None:
        self.chat.appendStream(message_id, chunk)

    def finish_stream(self, message_id: str, final_chunk: Optional[str] = None) -> None:
        if final_chunk is None:
            self.chat.finishStream(message_id)
        else:
            self.chat.finishStream(message_id, final_chunk)

    # ------------------------------------------------------------------
    # Appearance / metadata
    # ------------------------------------------------------------------

    def set_agent(self, agent: Union[ChatAgentConfig, Dict[str, Any]]) -> None:
        if hasattr(agent, "to_dict"):
            agent_payload = agent.to_dict()
        elif isinstance(agent, dict):
            agent_payload = agent
        else:
            raise TypeError(f"Unsupported agent representation: {type(agent)!r}")
        self.chat.setAgent(js.JSON.parse(json.dumps(agent_payload)))

    def set_theme(self, theme: str) -> None:
        self.chat.setTheme(theme)

    def focus_composer(self) -> None:
        if hasattr(self.chat, "focusComposer"):
            self.chat.focusComposer()

    def set_chat_badge(self, chat_id: str, badge: Optional[int]) -> None:
        if not chat_id:
            raise ValueError("chat_id is required to set a badge")
        self.chat.setChatBadge(chat_id, badge)

    def get_chats(self) -> List[Dict[str, Any]]:
        result = self.chat.getChats()
        if hasattr(result, "to_py"):
            return result.to_py()
        return result

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def destroy(self) -> None:
        try:
            if hasattr(self.chat, "destroy"):
                self.chat.destroy()
        finally:
            self._event_proxies.clear()
