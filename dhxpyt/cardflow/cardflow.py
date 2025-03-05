import json
from typing import Any, Callable, TypeVar
from pyodide.ffi import create_proxy
import js

from .cardflow_config import CardFlowConfig

class CardFlow:
    """
    Wrapper class for the CardFlow widget.
    """
    def __init__(self, config: CardFlowConfig, container: str = None):
        # Convert the config to a dictionary and initialize CardFlow widget
        config_dict = config.to_dict()
        self.cardflow = js.customdhx.CardFlow.new(container, js.JSON.parse(json.dumps(config_dict)))
        
        # Dictionary to store event handlers
        self.event_handlers = {}

    def update_header(self):
        self.cardflow.updateHeader()

    def set_theme(self, theme: str) -> None:
        self.cardflow.setTheme(js.JSON.parse(json.dumps({"name": theme, "fonts": True})))

    def export_to_json(self) -> str:
        return self.cardflow.data.serialize()

    def on_sort(self, handler: Callable) -> None:
        event_proxy = create_proxy(handler)
        self.cardflow.events.on("sort", event_proxy)

    def on_card_options(self, handler: Callable) -> None:
        """
        Handles when card options are triggered (e.g., toolbar options button clicked).
        """
        event_proxy = create_proxy(handler)
        self.cardflow.onOptions = event_proxy

    def on_card_expand(self, handler: Callable) -> None:
        """
        Handles when a card is expanded.
        """
        event_proxy = create_proxy(handler)
        self.cardflow.onExpand = event_proxy

    def on_card_collapse(self, handler: Callable) -> None:
        """
        Handles when a card is collapsed.
        """
        event_proxy = create_proxy(handler)
        self.cardflow.onCollapse = event_proxy

    def on_options(self, handler: Callable) -> None:
        """
        Handles when a card is collapsed.
        """
        event_proxy = create_proxy(handler)
        self.cardflow.onOptions = event_proxy

    def add_layout(self, id: str = "mainwindow", layout_config = None):
        """ Adds a Layout into a Layout cell """
        from ..layout import Layout
        layout_widget = Layout(config=layout_config)
        self.attach_to_card_content(id, layout_widget.layout)
        return layout_widget

    def attach_to_card_content(self, cardid: str, widget: str) -> None:
        """
        Attach a widget to the card content area when expanded.
        You can customize this function to attach real widgets.
        """
        # Example: Attaching a widget to card content
        self.cardflow.attachToCardContent(cardid, widget)

    def detach_from_card_content(self, cardid: str) -> None:
        """
        Example function to remove widget from the card's content area.
        Customize this function as needed.
        """
        self.cardflow.detachCardFromContent(cardid)
