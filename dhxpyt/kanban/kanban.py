import json
from typing import Any, Callable, Dict, List, Union
from pyodide.ffi import create_proxy
import js

from .kanban_config import KanbanConfig

class Kanban:
    """
    Wrapper class for the DHTMLX Kanban widget.
    """
    def __init__(self, config: KanbanConfig, container: str = None):
        """
        Initializes the Kanban widget.

        :param config: KanbanConfig object containing the configuration.
        :param container: ID of the HTML element to attach the Kanban to.
        """
        config_dict = config.to_dict()
        self.kanban = js.kanban.Kanban.new(container, js.JSON.parse(json.dumps(config_dict)))

    """ Kanban API Methods """

    def add_card(self, card: Dict[str, Any]) -> None:
        """Adds a new card to the Kanban."""
        self.kanban.addCard(js.JSON.parse(json.dumps(card)))

    def remove_card(self, card_id: Union[str, int]) -> None:
        """Removes a card by its ID."""
        self.kanban.removeCard(card_id)

    def update_card(self, card_id: Union[str, int], updates: Dict[str, Any]) -> None:
        """Updates a card's properties."""
        self.kanban.updateCard(card_id, js.JSON.parse(json.dumps(updates)))

    def add_column(self, column: Dict[str, Any]) -> None:
        """Adds a new column to the Kanban."""
        self.kanban.addColumn(js.JSON.parse(json.dumps(column)))

    def set_theme(self, theme: str) -> None:
        self.kanban.setTheme(js.JSON.parse(json.dumps({"name": theme, "fonts": True})))

    def remove_column(self, column_id: Union[str, int]) -> None:
        """Removes a column by its ID."""
        self.kanban.removeColumn(column_id)

    def get_cards(self) -> List[Dict[str, Any]]:
        """Returns all cards in the Kanban."""
        return [card.to_py() for card in self.kanban.getCards()]

    def get_columns(self) -> List[Dict[str, Any]]:
        """Returns all columns in the Kanban."""
        return [column.to_py() for column in self.kanban.getColumns()]

    def select_card(self, card_id: Union[str, int]) -> None:
        """Selects a card by its ID."""
        self.kanban.selectCard(card_id)

    def unselect_card(self, card_id: Union[str, int]) -> None:
        """Unselects a card by its ID."""
        self.kanban.unselectCard(card_id)

    def export_to_json(self) -> str:
        """Exports Kanban data to JSON format."""
        return self.kanban.data.serialize()

    """ Kanban Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Adds an event handler for the specified event."""
        event_proxy = create_proxy(handler)
        self.kanban.events.on(event_name, event_proxy)

    def on_card_click(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires when a card is clicked."""
        def event_handler(card):
            handler(card.to_py())
        self.kanban.events.on("cardClick", create_proxy(event_handler))

    def on_column_click(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires when a column header is clicked."""
        def event_handler(column):
            handler(column.to_py())
        self.kanban.events.on("columnClick", create_proxy(event_handler))

    def on_card_drag(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires during a card drag event."""
        def event_handler(card):
            handler(card.to_py())
        self.kanban.events.on("cardDrag", create_proxy(event_handler))

    def on_card_drop(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires when a card is dropped."""
        def event_handler(card):
            handler(card.to_py())
        self.kanban.events.on("cardDrop", create_proxy(event_handler))

    def on_editor_change(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires when editor data is changed."""
        def event_handler(data):
            handler(data.to_py())
        self.kanban.events.on("editorChange", create_proxy(event_handler))