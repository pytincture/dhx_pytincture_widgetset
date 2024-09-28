"""
Sidebar widget implementation
"""

from typing import Any, Callable, Dict, List, Optional, Union
import json
from pyodide.ffi import create_proxy
import js

from .sidebar_config import SidebarConfig


class Sidebar:
    def __init__(self, config: SidebarConfig = None, widget_parent: str = None):
        """
        Initializes the Sidebar widget.

        :param config: (Optional) The SidebarConfig object containing the sidebar configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the sidebar will be attached.
        """
        if config is None:
            config = SidebarConfig()
        config_dict = config.to_dict()
        # Create the Sidebar instance
        self.sidebar = js.dhx.Sidebar.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Sidebar API Functions """

    def collapse(self) -> None:
        """Collapses the sidebar."""
        self.sidebar.collapse()

    def destructor(self) -> None:
        """Destroys the Sidebar instance and releases resources."""
        self.sidebar.destructor()

    def disable(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Disables and dims items of Sidebar."""
        self.sidebar.disable(ids)

    def enable(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Enables disabled items of Sidebar."""
        self.sidebar.enable(ids)

    def expand(self) -> None:
        """Expands the sidebar."""
        self.sidebar.expand()

    def get_selected(self) -> List[Union[str, int]]:
        """Returns an array of IDs of selected items."""
        selected = self.sidebar.getSelected()
        return [item for item in selected.to_py()]

    def hide(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Hides items of Sidebar."""
        self.sidebar.hide(ids)

    def is_collapsed(self) -> bool:
        """Checks whether Sidebar is collapsed."""
        return self.sidebar.isCollapsed()

    def is_disabled(self, id: Union[str, int]) -> bool:
        """Checks whether an item of Sidebar is disabled."""
        return self.sidebar.isDisabled(id)

    def is_selected(self, id: Union[str, int]) -> bool:
        """Checks whether a specified Sidebar item is selected."""
        return self.sidebar.isSelected(id)

    def paint(self) -> None:
        """Repaints Sidebar on a page."""
        self.sidebar.paint()

    def select(self, id: Union[str, int], unselect: bool = True) -> None:
        """Selects a specified Sidebar item."""
        self.sidebar.select(id, unselect)

    def show(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Shows items of Sidebar."""
        self.sidebar.show(ids)

    def toggle(self) -> None:
        """Expands/collapses Sidebar."""
        self.sidebar.toggle()

    def unselect(self, id: Union[str, int] = None) -> None:
        """Unselects a selected Sidebar item."""
        self.sidebar.unselect(id)

    """ Sidebar Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Adds an event handler for the specified event.

        :param event_name: The name of the event.
        :param handler: The handler function to attach.
        """
        event_proxy = create_proxy(handler)
        self.sidebar.events.on(event_name, event_proxy)

    def on_after_collapse(self, handler: Callable[[], None]) -> None:
        """Fires after collapsing a sidebar."""
        self.add_event_handler('afterCollapse', handler)

    def on_after_expand(self, handler: Callable[[], None]) -> None:
        """Fires after expanding a sidebar."""
        self.add_event_handler('afterExpand', handler)

    def on_after_hide(self, handler: Callable[[Any], None]) -> None:
        """
        Fires after hiding a sub-item of Sidebar.

        :param handler: The handler function with parameter events (Event).
        """
        self.add_event_handler('afterHide', handler)

    def on_before_collapse(self, handler: Callable[[], Union[bool, None]]) -> None:
        """
        Fires before collapsing a sidebar.

        :param handler: The handler function that returns False to prevent collapsing.
        """
        def event_handler():
            result = handler()
            if result is False:
                return js.Boolean(False)
        self.sidebar.events.on('beforeCollapse', create_proxy(event_handler))

    def on_before_expand(self, handler: Callable[[], Union[bool, None]]) -> None:
        """
        Fires before expanding a sidebar.

        :param handler: The handler function that returns False to prevent expanding.
        """
        def event_handler():
            result = handler()
            if result is False:
                return js.Boolean(False)
        self.sidebar.events.on('beforeExpand', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, int], Any], Union[bool, None]]) -> None:
        """
        Fires before hiding a sub-item of Sidebar.

        :param handler: The handler function with parameters id (str or int), events (Event).
        """
        def event_handler(id, events):
            result = handler(id, events)
            if result is False:
                return js.Boolean(False)
        self.sidebar.events.on('beforeHide', create_proxy(event_handler))

    def on_click(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """
        Fires after a click on a control.

        :param handler: The handler function with parameters id (str or int), events (Event).
        """
        def event_handler(id, events):
            handler(id, events)
        self.sidebar.events.on('click', create_proxy(event_handler))

    def on_input_blur(self, handler: Callable[[Union[str, int]], None]) -> None:
        """
        Fires when a control is blurred.

        :param handler: The handler function with parameter id (str or int).
        """
        self.add_event_handler('inputBlur', handler)

    def on_input_created(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """
        Fires when a new input is added.

        :param handler: The handler function with parameters id (str or int), input (HTMLInputElement).
        """
        def event_handler(id, input):
            handler(id, input)
        self.sidebar.events.on('inputCreated', create_proxy(event_handler))

    def on_input_focus(self, handler: Callable[[Union[str, int]], None]) -> None:
        """
        Fires when a control is focused.

        :param handler: The handler function with parameter id (str or int).
        """
        self.add_event_handler('inputFocus', handler)

    def on_keydown(self, handler: Callable[[Any, Optional[str]], None]) -> None:
        """
        Fires when any key is pressed and a Sidebar option is in focus.

        :param handler: The handler function with parameters event (KeyboardEvent), id (str or None).
        """
        def event_handler(event, id=None):
            handler(event, id)
        self.sidebar.events.on('keydown', create_proxy(event_handler))

    def on_open_menu(self, handler: Callable[[Union[str, int]], None]) -> None:
        """
        Fires on expanding a menu control.

        :param handler: The handler function with parameter id (str or int).
        """
        self.add_event_handler('openMenu', handler)
