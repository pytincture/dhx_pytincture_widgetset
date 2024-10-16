"""
Toolbar widget implementation
"""

from typing import Any, Callable, List, Union, Optional
import json
from pyodide.ffi import create_proxy
import js

from .toolbar_config import ToolbarConfig


class Toolbar:
    def __init__(self, config: ToolbarConfig = None, widget_parent: str = None):
        """
        Initializes the Toolbar widget.

        :param config: (Optional) The ToolbarConfig object containing the toolbar configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the toolbar will be attached.
        """
        if config is None:
            config = ToolbarConfig()
        config_dict = config.to_dict()
        # Create the Toolbar instance
        self.toolbar = js.dhx.Toolbar.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Toolbar API Functions """

    def destructor(self) -> None:
        """Destroys the Toolbar instance and releases resources."""
        self.toolbar.destructor()

    def disable(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Disables and dims items of Toolbar."""
        self.toolbar.disable(ids)

    def enable(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Enables disabled items of Toolbar."""
        self.toolbar.enable(ids)

    def get_selected(self) -> List[Union[str, int]]:
        """Returns an array of IDs of selected items."""
        selected = self.toolbar.getSelected()
        return [item for item in selected.to_py()]

    def get_state(self, id: Union[str, int] = None) -> Union[str, bool, dict]:
        """Gets current values/states of controls."""
        return self.toolbar.getState(id)

    def hide(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Hides items of Toolbar."""
        self.toolbar.hide(ids)

    def is_disabled(self, id: Union[str, int]) -> bool:
        """Checks whether an item of Toolbar is disabled."""
        return self.toolbar.isDisabled(id)

    def is_selected(self, id: Union[str, int]) -> bool:
        """Checks whether a specified Toolbar item is selected."""
        return self.toolbar.isSelected(id)

    def paint(self) -> None:
        """Repaints Toolbar on a page."""
        self.toolbar.paint()

    def select(self, id: Union[str, int], unselect: bool = True) -> None:
        """Selects a specified Toolbar item."""
        self.toolbar.select(id, unselect)

    def set_focus(self, id: Union[str, int]) -> None:
        """Sets focus on an Input control by its ID."""
        self.toolbar.setFocus(id)

    def set_state(self, state: dict) -> None:
        """Sets values/states of controls."""
        self.toolbar.setState(js.JSON.parse(json.dumps(state)))

    def update_item(self, id, item_dict: str) -> None:
        """Updates a toolbar item that is already on the toolbar"""
        self.toolbar.data.update(id, js.JSON.parse(json.dumps(item_dict)))

    def show(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Shows items of Toolbar."""
        self.toolbar.show(ids)

    def unselect(self, id: Union[str, int] = None) -> None:
        """Unselects a selected Toolbar item."""
        self.toolbar.unselect(id)

    """ Toolbar Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Adds an event handler for the specified event.
        
        :param event_name: The name of the event.
        :param handler: The handler function to attach.
        """
        event_proxy = create_proxy(handler)
        self.toolbar.events.on(event_name, event_proxy)

    def on_after_hide(self, handler: Callable[[Any], None]) -> None:
        """Fires after hiding a toolbar item."""
        self.add_event_handler('afterHide', handler)

    def on_before_hide(self, handler: Callable[[Union[str, int], Any], Union[bool, None]]) -> None:
        """Fires before hiding a toolbar item."""
        def event_handler(id, events):
            result = handler(id, events)
            if result is False:
                return js.Boolean(False)
        self.toolbar.events.on('beforeHide', create_proxy(event_handler))

    def on_click(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """Fires after a click on a control."""
        def event_handler(id, events):
            handler(id, events)
        self.toolbar.events.on('click', create_proxy(event_handler))

    def on_input(self, handler: Callable[[str, str], None]) -> None:
        """Fires on entering text into an input field."""
        self.add_event_handler('input', handler)

    def on_input_blur(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires when a control is blurred."""
        self.add_event_handler('inputBlur', handler)

    def on_input_change(self, handler: Callable[[Union[str, int], str], Any]) -> None:
        """Fires on changing the value of an Input control."""
        self.add_event_handler('inputChange', handler)

    def on_input_created(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """Fires when a new input is created."""
        self.add_event_handler('inputCreated', handler)

    def on_input_focus(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires when a control is focused."""
        self.add_event_handler('inputFocus', handler)

    def on_keydown(self, handler: Callable[[Any, Optional[str]], None]) -> None:
        """Fires when any key is pressed while a Toolbar control is in focus."""
        def event_handler(event, id=None):
            handler(event, id)
        self.toolbar.events.on('keydown', create_proxy(event_handler))

    def on_open_menu(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires when expanding a menu control."""
        self.add_event_handler('openMenu', handler)
