import json
from typing import Any, Callable, Dict, List, Union
from pyodide.ffi import create_proxy
import js

from .reconciliation_config import ReconciliationConfig

class Reconciliation:
    """
    Wrapper class for the Reconciliation widget.
    """
    def __init__(self, config: ReconciliationConfig, container: str = None):
        """
        Initializes the Reconciliation widget.

        :param config: ReconciliationConfig object containing the configuration.
        :param container: ID of the HTML element to attach the Reconciliation to.
        """
        config_dict = config.to_dict()
        self.reconciliation = js.customdhx.Reconciliation.new(container, js.JSON.parse(json.dumps(config_dict)))

    def update_header(self):
        self.reconciliation.updateHeader()

    """ Reconciliation API Methods """

    def set_theme(self, theme: str) -> None:
        self.reconciliation.setTheme(js.JSON.parse(json.dumps({"name": theme, "fonts": True})))

    def export_to_json(self) -> str:
        """Exports Reconciliation data to JSON format."""
        return self.reconciliation.data.serialize()

    """ Reconciliation Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Adds an event handler for the specified event."""
        event_proxy = create_proxy(handler)
        self.reconciliation.events.on(event_name, event_proxy)

    def on_net_div_click(self, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.reconciliation.onNetDivClick = event_proxy

    # def on_card_click(self, handler: Callable[[Dict[str, Any]], None]) -> None:
    #     """Fires when a card is clicked."""
    #     def event_handler(card):
    #         handler(card.to_py())
    #     self.reconciliation.events.on("cardClick", create_proxy(event_handler))

    # TODO:
    # add transaction
    #
