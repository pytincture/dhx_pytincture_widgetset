import json
from typing import Any, Callable, Dict, Iterable, List, Optional, Union
from uuid import uuid4

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
        self._mount_id: Optional[str] = None
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
            mount_id = f"cardpanel_{uuid4().hex}"
            attach_html = getattr(container, "attachHTML", None)
            if callable(attach_html):
                attach_html(f'<div id="{mount_id}" style="width:100%;height:100%;"></div>')
            else:
                attach = getattr(container, "attach", None)
                if callable(attach):
                    attach(f'<div id="{mount_id}" style="width:100%;height:100%;"></div>')
                else:
                    raise ValueError("Provided container does not support attachHTML/attach.")

            self._mount_id = mount_id
            return js.document.getElementById(mount_id)

        if isinstance(root, str):
            return js.document.querySelector(root)

        return root

    def _bind_event(self, event_name: str, handler: Callable) -> None:
        """
        Helper that registers an event handler and keeps a proxy alive.
        """
        proxy = create_proxy(handler)
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
        if self._mount_id:
            element = js.document.getElementById(self._mount_id)
            if element and element.parentElement:
                element.parentElement.removeChild(element)
        self._event_proxies.clear()
