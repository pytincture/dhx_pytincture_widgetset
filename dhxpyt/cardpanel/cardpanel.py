import json
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import js
from pyodide.ffi import create_proxy

from .cardpanel_config import CardPanelConfig, CardPanelCardConfig


class CardPanel:
    """
    Python wrapper for the custom CardPanel widget.
    """

    def __init__(
        self,
        config: Optional[CardPanelConfig] = None,
        *,
        container: Any = None,
        root: Optional[Union[str, Any]] = None,
    ) -> None:
        """
        :param config: Optional CardPanelConfig object describing initial options.
        :param container: Optional DHTMLX layout cell (or similar) used to mount the widget.
        :param root: Optional CSS selector string or DOM element where the widget should render.
        """
        if container is None and root is None:
            raise ValueError("CardPanel requires either a container or a root element.")

        self.config = config or CardPanelConfig()
        self._event_proxies: Dict[str, List[Any]] = {}
        self._container = container

        root_element = self._resolve_root(container=container, root=root)
        if root_element is None:
            raise RuntimeError("Unable to resolve root element for CardPanel.")

        config_payload = self.config.to_dict()
        self.cardpanel = js.customdhx.CardPanel.new(
            root_element,
            js.JSON.parse(json.dumps(config_payload))
        )

    def _resolve_root(self, *, container: Any, root: Optional[Union[str, Any]]) -> Any:
        """
        Resolve the DOM element that will host the CardPanel.
        """
        if container is not None:
            return container

        if isinstance(root, str):
            return js.document.querySelector(root)

        return root

    def _bind_event(self, event_name: str, handler: Callable) -> None:
        """
        Helper that registers an event handler and keeps a proxy alive.
        """
        def wrapped(*args, **kwargs):
            if args:
                converted = [
                    arg.to_py() if hasattr(arg, "to_py") else arg
                    for arg in args
                ]
            else:
                converted = []
            return handler(*converted, **kwargs)

        proxy = create_proxy(wrapped)
        bucket = self._event_proxies.setdefault(event_name, [])
        bucket.append(proxy)
        self.cardpanel.on(event_name, proxy)

    # Event bindings -------------------------------------------------------

    def on_search(self, handler: Callable[[str], Any]) -> None:
        self._bind_event("search", handler)

    def on_add(self, handler: Callable[[], Any]) -> None:
        self._bind_event("add", handler)

    def on_view(self, handler: Callable[[Any], Any]) -> None:
        self._bind_event("view", handler)

    def on_card_click(self, handler: Callable[[Any], Any]) -> None:
        self._bind_event("cardClick", handler)

    # Data API -------------------------------------------------------------

    def load(self, cards: Iterable[Union[CardPanelCardConfig, Dict[str, Any]]]) -> None:
        payload = [card.to_dict() if hasattr(card, "to_dict") else card for card in cards]
        self.cardpanel.load(js.JSON.parse(json.dumps(payload)))

    def add_card(self, card: Union[CardPanelCardConfig, Dict[str, Any]]) -> None:
        card_payload = card.to_dict() if hasattr(card, "to_dict") else card
        self.cardpanel.add(js.JSON.parse(json.dumps(card_payload)))

    def filter(self, query: str) -> None:
        """
        Access the underlying filter logic (mirrors the JS helper).
        """
        if hasattr(self.cardpanel, "_filter"):
            self.cardpanel._filter(query)

    def destroy(self) -> None:
        """
        Tears down DOM content created for the widget (best-effort).
        """
        try:
            if hasattr(self.cardpanel, "destroy"):
                self.cardpanel.destroy()
            elif hasattr(self.cardpanel, "destructor"):
                self.cardpanel.destructor()
        finally:
            self._event_proxies.clear()
