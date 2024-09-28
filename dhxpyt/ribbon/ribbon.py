"""
Ribbon widget implementation
"""

from typing import Any, Callable, Dict, List, Optional, Union
import json
from pyodide.ffi import create_proxy
import js

from .ribbon_config import RibbonConfig


class Ribbon:
    def __init__(self, config: RibbonConfig = None, widget_parent: str = None):
        """
        Initializes the Ribbon widget.

        :param config: (Optional) The RibbonConfig object containing the ribbon configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the ribbon will be attached.
        """
        if config is None:
            config = RibbonConfig()
        config_dict = config.to_dict()
        # Create the Ribbon instance
        self.ribbon = js.dhx.Ribbon.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Ribbon API Functions """

    def destructor(self) -> None:
        """Destroys the Ribbon instance and releases resources."""
        self.ribbon.destructor()

    def disable(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Disables and dims an item(s) of Ribbon."""
        self.ribbon.disable(ids)

    def enable(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Enables a disabled item(s) of Ribbon."""
        self.ribbon.enable(ids)

    def get_selected(self) -> List[Union[str, int]]:
        """Returns an array of IDs of selected items."""
        selected = self.ribbon.getSelected()
        return [item for item in selected.to_py()]

    def get_state(self) -> Dict[str, Any]:
        """Gets current values/states of controls."""
        state = self.ribbon.getState()
        return state.to_py()

    def hide(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Hides an item of Ribbon."""
        self.ribbon.hide(ids)

    def is_disabled(self, id: Union[str, int]) -> bool:
        """Checks whether an item of Ribbon is disabled."""
        return self.ribbon.isDisabled(id)

    def is_selected(self, id: Union[str, int]) -> bool:
        """Checks whether a specified Ribbon item is selected."""
        return self.ribbon.isSelected(id)

    def paint(self) -> None:
        """Repaints Ribbon on a page."""
        self.ribbon.paint()

    def select(self, id: Union[str, int], unselect: bool = True) -> None:
        """Selects a specified item of Ribbon."""
        self.ribbon.select(id, unselect)

    def set_state(self, state: Dict[str, Any]) -> None:
        """Sets values/states of controls."""
        self.ribbon.setState(js.JSON.parse(json.dumps(state)))

    def show(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Shows an item of Ribbon."""
        self.ribbon.show(ids)

    def unselect(self, id: Union[str, int] = None) -> None:
        """Unselects a selected Ribbon item."""
        self.ribbon.unselect(id)

    """ Ribbon Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Adds an event handler for the specified event.

        :param event_name: The name of the event.
        :param handler: The handler function to attach.
        """
        event_proxy = create_proxy(handler)
        self.ribbon.events.on(event_name, event_proxy)

    def on_click(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """
        Fires after a click on a control.

        :param handler: The handler function with parameters id (str or int), events (Event).
        """
        def event_handler(id, events):
            handler(id, events)
        self.ribbon.events.on('click', create_proxy(event_handler))

    def on_input(self, handler: Callable[[str, str], None]) -> None:
        """
        Fires on entering text into the input field.

        :param handler: The handler function with parameters id (str), value (str).
        """
        def event_handler(id, value):
            handler(id, value)
        self.ribbon.events.on('input', create_proxy(event_handler))

    def on_input_blur(self, handler: Callable[[Union[str, int]], None]) -> None:
        """
        Fires when a control is blurred.

        :param handler: The handler function with parameter id (str or int).
        """
        self.add_event_handler('inputBlur', handler)

    def on_input_change(self, handler: Callable[[Union[str, int], str], None]) -> None:
        """
        Fires on changing the value in the Input control of Ribbon.

        :param handler: The handler function with parameters id (str or int), newValue (str).
        """
        def event_handler(id, newValue):
            handler(id, newValue)
        self.ribbon.events.on('inputChange', create_proxy(event_handler))

    def on_input_created(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """
        Fires when a new input is added.

        :param handler: The handler function with parameters id (str or int), input (HTMLInputElement).
        """
        def event_handler(id, input):
            handler(id, input)
        self.ribbon.events.on('inputCreated', create_proxy(event_handler))

    def on_input_focus(self, handler: Callable[[Union[str, int]], None]) -> None:
        """
        Fires when a control is focused.

        :param handler: The handler function with parameter id (str or int).
        """
        self.add_event_handler('inputFocus', handler)

    def on_keydown(self, handler: Callable[[Any, Optional[str]], None]) -> None:
        """
        Fires when any key is pressed and a control of Ribbon is in focus.

        :param handler: The handler function with parameters event (KeyboardEvent), id (str or None).
        """
        def event_handler(event, id=None):
            handler(event, id)
        self.ribbon.events.on('keydown', create_proxy(event_handler))

    def on_open_menu(self, handler: Callable[[Union[str, int]], None]) -> None:
        """
        Fires on expanding a menu control.

        :param handler: The handler function with parameter id (str or int).
        """
        self.add_event_handler('openMenu', handler)
