import json
from typing import Any, Callable, Dict, Optional, TypeVar, Union
from pyodide.ffi import create_proxy
import js

from .cardflow_config import CardFlowConfig

class CardFlow:
    """
    Wrapper class for the CardFlow widget.
    """
    def __init__(self, config: CardFlowConfig, container: str = None):
        """
        :param config: An instance of CardFlowConfig describing columns, data, etc.
        :param container: An optional reference to a layout cell or container ID where the JS CardFlow is attached.
        """
        # Convert the config to a dictionary and initialize the CardFlow widget
        config_dict = config.to_dict()
        self.cardflow = js.customdhx.CardFlow.new(
            container,
            js.JSON.parse(json.dumps(config_dict))
        )
        
        # Dictionary to store event handlers (if you want to store them for potential removal)
        self.event_handlers = {}

    def on_sort(self, handler: Callable) -> None:
        """
        Placeholder for a sort event if the JS side triggers a "sort" event.
        Currently, the main code does not raise a custom "sort" event, so you may 
        want to capture the sorting user action differently or modify the JS code 
        to fire an event.
        """
        event_proxy = create_proxy(handler)
        self.cardflow.events.on("sort", event_proxy)

    def on_card_options(self, handler: Callable) -> None:
        """
        Called when card's options (e.g., dots menu) are used.
        """
        event_proxy = create_proxy(handler)
        self.cardflow.onOptions = event_proxy


    def on_card_expand(self, handler: Callable) -> None:
        """
        Called when a card is expanded.
        """
        event_proxy = create_proxy(handler)
        self.cardflow.onExpand = event_proxy

    def on_card_collapse(self, handler: Callable) -> None:
        """
        Called when a card is collapsed.
        """
        event_proxy = create_proxy(handler)
        self.cardflow.onCollapse = event_proxy

    def on_options(self, handler: Callable) -> None:
        """
        Same as above for on_card_options, if you prefer a shorter name.
        """
        event_proxy = create_proxy(handler)
        self.cardflow.onOptions = event_proxy

    def update_header(self):
        """
        If your JS code has a method named updateHeader, call it here.
        Otherwise, remove or adjust as needed.
        """
        if hasattr(self.cardflow, "updateHeader"):
            self.cardflow.updateHeader()

    def set_row_color(self, row_id, color):
        self.cardflow.setRowColor(row_id, color)

    def set_row_font_size(self, row_id, font_size):
        self.cardflow.setRowFontSize(row_id, font_size)

    def set_row_data_value(self, row_id, column_id, value):
        self.cardflow.setRowDataValue(row_id, column_id, value)

    def toggle_header(self, show=None):
        self.cardflow.toggleHeader(show)

    def toggle_sort(self, show=None):
        self.cardflow.toggleSort(show)

    def toggle_data_headers(self, show=None):
        self.cardflow.toggleDataHeaders(show)

    def set_card_expanded_height(self, card_id: str, height: str) -> None:
        """
        Sets the expanded height for a specific card.
        
        :param card_id: The ID of the card to modify
        :param height: The height value (e.g., "400px", "50vh", "auto")
        """
        self.cardflow.setCardExpandedHeight(card_id, height)

    def set_theme(self, theme: Union[str, Dict[str, Any]], css_vars: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        """Apply a theme to the underlying cardflow widget and optional CSS variable overrides."""
        try:
            from .. import theme as _theme_helper
            _theme_helper.apply_theme(theme, css_vars)
        except Exception:
            if hasattr(self.cardflow, "setTheme"):
                if isinstance(theme, dict):
                    self.cardflow.setTheme(js.JSON.parse(json.dumps(theme)))
                else:
                    self.cardflow.setTheme(js.JSON.parse(json.dumps({"name": theme, "fonts": True})))

    def export_to_json(self) -> str:
        """
        Exports the current data to JSON. If your JS code actually supports data.serialize(), this will work.
        """
        if hasattr(self.cardflow, "data") and hasattr(self.cardflow.data, "serialize"):
            return self.cardflow.data.serialize()
        return ""

    def collapse_all(self) -> None:
        """
        Collapses all cards (if the underlying JS code includes collapseAll()).
        """
        self.cardflow.collapseAll()

    def expand_all(self) -> None:
        """
        Expands all cards (if the underlying JS code includes expandAll()).
        """
        self.cardflow.expandAll()

    def add_layout(self, id: str = "mainwindow", layout_config=None):
        """
        Example of how you might nest a dhtmlx Layout inside a card's content.
        This calls attach_to_card_content to wire up the new layout widget. 
        Modify as needed for your application.
        """
        from ..layout import Layout
        layout_widget = Layout(config=layout_config)
        self.attach_to_card_content(id, layout_widget.layout)
        return layout_widget

    def attach_to_card_content(self, cardid: str, widget: Any) -> None:
        """
        Attach a (JS) widget to a card's content area when expanded.
        Passing in the cardid and the widget (which might be another dhtmlx object).
        """
        self.cardflow.attachToCardContent(cardid, widget)

    def detach_from_card_content(self, cardid: str) -> None:
        """
        Removes a widget from the card's content area.
        """
        self.cardflow.detachCardFromContent(cardid)
