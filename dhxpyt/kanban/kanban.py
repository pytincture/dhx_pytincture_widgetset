from __future__ import annotations

import json
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import js
from pyodide.ffi import create_proxy

from .kanban_config import (
    KanbanCardConfig,
    KanbanColumnConfig,
    KanbanConfig,
    KanbanLaneConfig,
)


logger = logging.getLogger(__name__)
WRAPPER_REVISION = "kanban-wrapper/2024-06-02"
logger.info("Kanban widget wrapper loaded (%s)", WRAPPER_REVISION)
print(f"[KanbanWidget] Wrapper ready ({WRAPPER_REVISION})")


class Kanban:
    """
    Python wrapper around the custom Kanban widget (mirrors the structure used
    by the CardPanel and Chat wrappers in this package).
    """

    _template_proxies: Dict[str, List[Any]] = {}

    def __init__(
        self,
        config: Optional[KanbanConfig] = None,
        *,
        container: Any = None,
        root: Optional[Union[str, Any]] = None,
    ) -> None:
        if container is None and root is None:
            raise ValueError("Kanban widget requires a container or a root element.")

        self.config = config or KanbanConfig()
        self._container = container
        self._event_proxies: Dict[str, List[Any]] = {}

        root_element = self._resolve_root(container=container, root=root)
        if root_element is None:
            raise RuntimeError("Unable to resolve root element for Kanban widget.")

        config_dict = self.config.to_dict()
        config_json = json.dumps(config_dict)
        config_options = js.JSON.parse(config_json)

        widget_cls = self._js_class()
        self.kanban = widget_cls.new(root_element, config_options)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _js_class() -> Any:
        try:
            return js.customdhx.KanbanBoard
        except AttributeError as exc:
            raise RuntimeError(
                "customdhx.KanbanBoard is not available. Ensure the custom Kanban "
                "JavaScript bundle has been loaded."
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
        self.kanban.on(event_name, proxy)

    # ------------------------------------------------------------------
    # Template registration
    # ------------------------------------------------------------------

    @classmethod
    def register_card_template(cls, name: str, factory: Any) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Template name must be a non-empty string.")

        widget_cls = cls._js_class()
        register = getattr(widget_cls, "registerCardTemplate", None)
        if register is None:
            raise RuntimeError("KanbanBoard.registerCardTemplate is not available.")

        template_key = f"card::{name}"
        factory_ref = factory

        if isinstance(factory, str):
            factory_ref = js.eval(factory)
        elif callable(factory) and not hasattr(factory, "to_py"):
            proxied = create_proxy(factory)
            cls._template_proxies.setdefault(template_key, []).append(proxied)
            factory_ref = proxied
        register(name, factory_ref)
        logger.info("Kanban.register_card_template -> '%s' (%s)", name, WRAPPER_REVISION)
        print(f"[KanbanWidget] register_card_template -> '{name}' ({WRAPPER_REVISION})")

    @classmethod
    def register_column_template(cls, name: str, factory: Any) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Template name must be a non-empty string.")

        widget_cls = cls._js_class()
        register = getattr(widget_cls, "registerColumnTemplate", None)
        if register is None:
            raise RuntimeError("KanbanBoard.registerColumnTemplate is not available.")

        template_key = f"column::{name}"
        factory_ref = factory

        if isinstance(factory, str):
            factory_ref = js.eval(factory)
        elif callable(factory) and not hasattr(factory, "to_py"):
            proxied = create_proxy(factory)
            cls._template_proxies.setdefault(template_key, []).append(proxied)
            factory_ref = proxied
        register(name, factory_ref)
        logger.info("Kanban.register_column_template -> '%s' (%s)", name, WRAPPER_REVISION)
        print(f"[KanbanWidget] register_column_template -> '{name}' ({WRAPPER_REVISION})")

    # ------------------------------------------------------------------
    # Event bindings
    # ------------------------------------------------------------------

    def on_card_click(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._bind_event("cardClick", handler)

    def on_card_move(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._bind_event("cardMove", handler)

    def on_card_create(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._bind_event("cardCreate", handler)

    def on_column_create(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._bind_event("columnCreate", handler)

    def on_column_toggle(self, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._bind_event("columnToggle", handler)

    # ------------------------------------------------------------------
    # Data operations
    # ------------------------------------------------------------------

    @staticmethod
    def _column_to_dict(
        column: Union[KanbanColumnConfig, Dict[str, Any]]
    ) -> Dict[str, Any]:
        if hasattr(column, "to_dict"):
            return column.to_dict()
        if isinstance(column, dict):
            return column
        raise TypeError(f"Unsupported column representation: {type(column)!r}")

    @staticmethod
    def _card_to_dict(
        card: Union[KanbanCardConfig, Dict[str, Any]]
    ) -> Dict[str, Any]:
        if hasattr(card, "to_dict"):
            return card.to_dict()
        if isinstance(card, dict):
            return card
        raise TypeError(f"Unsupported card representation: {type(card)!r}")

    @staticmethod
    def _lane_to_dict(
        lane: Union[KanbanLaneConfig, Dict[str, Any]]
    ) -> Dict[str, Any]:
        if hasattr(lane, "to_dict"):
            return lane.to_dict()
        if isinstance(lane, dict):
            return lane
        raise TypeError(f"Unsupported lane representation: {type(lane)!r}")

    def load(self, config: KanbanConfig) -> None:
        """
        Replace the board with a new configuration payload.
        """
        self.reload(config)

    def reload(self, config: KanbanConfig) -> None:
        """
        Low-level hook: forward an entire configuration payload to the JS widget.
        """
        payload = config.to_dict()
        self.kanban.load(js.JSON.parse(json.dumps(payload)))

    def set_columns(
        self,
        columns: Iterable[Union[KanbanColumnConfig, Dict[str, Any]]],
    ) -> None:
        payload = [self._column_to_dict(column) for column in columns]
        self.kanban.setColumns(js.JSON.parse(json.dumps(payload)))

    def set_cards(
        self,
        cards: Iterable[Union[KanbanCardConfig, Dict[str, Any]]],
    ) -> None:
        payload = [self._card_to_dict(card) for card in cards]
        self.kanban.setCards(js.JSON.parse(json.dumps(payload)))

    def set_lanes(
        self,
        lanes: Iterable[Union[KanbanLaneConfig, Dict[str, Any]]],
    ) -> None:
        payload = [self._lane_to_dict(lane) for lane in lanes]
        self.kanban.setLanes(js.JSON.parse(json.dumps(payload)))

    def add_card(
        self,
        card: Union[KanbanCardConfig, Dict[str, Any]],
        *,
        index: Optional[int] = None,
    ) -> str:
        payload = self._card_to_dict(card)
        result = self.kanban.addCard(
            js.JSON.parse(json.dumps(payload)),
            index if index is None else int(index),
        )
        return result.to_py() if hasattr(result, "to_py") else result

    def update_card(self, card_id: str, **updates: Any) -> None:
        self.kanban.updateCard(card_id, js.JSON.parse(json.dumps(updates)))

    def remove_card(self, card_id: str) -> None:
        self.kanban.removeCard(card_id)

    def move_card(
        self,
        card_id: str,
        *,
        to_column: str,
        lane: Optional[str] = None,
        index: Optional[int] = None,
    ) -> None:
        options = {
            "column": to_column,
            "lane": lane,
            "index": index,
        }
        options = {k: v for k, v in options.items() if v is not None}
        if options:
            self.kanban.moveCard(card_id, js.JSON.parse(json.dumps(options)))
        else:
            self.kanban.moveCard(card_id)

    def add_column(
        self,
        column: Union[KanbanColumnConfig, Dict[str, Any]],
        *,
        index: Optional[int] = None,
    ) -> str:
        payload = self._column_to_dict(column)
        result = self.kanban.addColumn(
            js.JSON.parse(json.dumps(payload)),
            index if index is None else int(index),
        )
        return result.to_py() if hasattr(result, "to_py") else result

    def update_column(self, column_id: str, **updates: Any) -> None:
        self.kanban.updateColumn(column_id, js.JSON.parse(json.dumps(updates)))

    def remove_column(self, column_id: str) -> None:
        self.kanban.removeColumn(column_id)

    def set_theme(self, theme: str) -> None:
        self.kanban.setTheme(theme)

    def get_state(self) -> Dict[str, Any]:
        result = self.kanban.getState()
        return result.to_py() if hasattr(result, "to_py") else result

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def destroy(self) -> None:
        try:
            if hasattr(self.kanban, "destroy"):
                self.kanban.destroy()
        finally:
            self._event_proxies.clear()
