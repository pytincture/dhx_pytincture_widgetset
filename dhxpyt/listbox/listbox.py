"""
ListBox widget implementation
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .listbox_config import ListboxConfig


class Listbox:
    def __init__(self, config: ListboxConfig = None, widget_parent: str = None):
        """
        Initializes the ListBox widget.

        :param config: (Optional) The ListBoxConfig object containing the list configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the list will be attached.
        """
        if config is None:
            config = ListboxConfig()
        config_dict = config.to_dict()
        self.listbox = js.dhx.List.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ ListBox API Functions """

    def destructor(self) -> None:
        """Destroys the ListBox instance and releases resources."""
        self.listbox.destructor()

    def edit_item(self, item_id: Union[str, int]) -> None:
        """Enables editing of an item."""
        self.listbox.editItem(item_id)

    def get_focus(self) -> Union[str, int]:
        """Returns the ID of the item in focus."""
        return self.listbox.getFocus()

    def get_focus_item(self) -> Dict[str, Any]:
        """Returns the object of the item in focus."""
        item = self.listbox.getFocusItem()
        return item.to_py() if item else None

    def paint(self) -> None:
        """Repaints the list on the page."""
        self.listbox.paint()

    def reset_focus(self) -> None:
        """Resets focus and moves the scroll to the beginning of the list."""
        self.listbox.resetFocus()

    def set_focus(self, item_id: Union[str, int]) -> None:
        """Sets focus to an item by its ID and moves the scroll to it."""
        self.listbox.setFocus(item_id)

    """ ListBox Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Adds an event handler for the specified event."""
        event_proxy = create_proxy(handler)
        self.listbox.events.on(event_name, event_proxy)

    def on_after_drag(self, handler: Callable[[Dict[str, Any], Any], None]) -> None:
        """Fires after dragging of an item is finished."""
        def event_handler(data, events):
            handler(data.to_py(), events)
        self.listbox.events.on('afterDrag', create_proxy(event_handler))

    def on_after_drop(self, handler: Callable[[Dict[str, Any], Any], None]) -> None:
        """Fires before the user has finished dragging of an item but after the mouse button is released."""
        def event_handler(data, events):
            handler(data.to_py(), events)
        self.listbox.events.on('afterDrop', create_proxy(event_handler))

    def on_after_edit_end(self, handler: Callable[[str, Union[str, int]], None]) -> None:
        """Fires after editing of an item is ended."""
        self.add_event_handler('afterEditEnd', handler)

    def on_after_edit_start(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires after editing of an item has started."""
        self.add_event_handler('afterEditStart', handler)

    def on_before_drag(self, handler: Callable[[Dict[str, Any], Any], Union[bool, None]]) -> None:
        """Fires before dragging of an item has started."""
        def event_handler(data, events):
            result = handler(data.to_py(), events)
            if result is False:
                return js.Boolean(False)
        self.listbox.events.on('beforeDrag', create_proxy(event_handler))

    def on_before_drop(self, handler: Callable[[Dict[str, Any], Any], Union[bool, None]]) -> None:
        """Fires before the user has finished dragging of an item and released the mouse button."""
        def event_handler(data, events):
            result = handler(data.to_py(), events)
            if result is False:
                return js.Boolean(False)
        self.listbox.events.on('beforeDrop', create_proxy(event_handler))

    def on_before_edit_end(self, handler: Callable[[str, Union[str, int]], Union[bool, None]]) -> None:
        """Fires before editing of an item is ended."""
        def event_handler(value, id):
            result = handler(value, id)
            if result is False:
                return js.Boolean(False)
        self.listbox.events.on('beforeEditEnd', create_proxy(event_handler))

    def on_before_edit_start(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before editing of an item has started."""
        def event_handler(id):
            result = handler(id)
            if result is False:
                return js.Boolean(False)
        self.listbox.events.on('beforeEditStart', create_proxy(event_handler))

    def on_cancel_drop(self, handler: Callable[[Dict[str, Any], Any], None]) -> None:
        """Fires on moving a mouse pointer out of item's borders while dragging the item."""
        def event_handler(data, events):
            handler(data.to_py(), events)
        self.listbox.events.on('cancelDrop', create_proxy(event_handler))

    def on_can_drop(self, handler: Callable[[Dict[str, Any], Any], None]) -> None:
        """Fires when a dragged item is over a target item."""
        def event_handler(data, events):
            handler(data.to_py(), events)
        self.listbox.events.on('canDrop', create_proxy(event_handler))

    def on_click(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """Fires on clicking an item."""
        self.add_event_handler('click', handler)

    def on_double_click(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """Fires on double-clicking an item."""
        self.add_event_handler('doubleClick', handler)

    def on_drag_in(self, handler: Callable[[Dict[str, Any], Any], Union[bool, None]]) -> None:
        """Fires when an item is dragged to another potential target."""
        def event_handler(data, events):
            result = handler(data.to_py(), events)
            if result is False:
                return js.Boolean(False)
        self.listbox.events.on('dragIn', create_proxy(event_handler))

    def on_drag_out(self, handler: Callable[[Dict[str, Any], Any], None]) -> None:
        """Fires when an item is dragged out of a potential target."""
        def event_handler(data, events):
            handler(data.to_py(), events)
        self.listbox.events.on('dragOut', create_proxy(event_handler))

    def on_drag_start(self, handler: Callable[[Dict[str, Any], Any], None]) -> None:
        """Fires when dragging of an item has started."""
        def event_handler(data, events):
            handler(data.to_py(), events)
        self.listbox.events.on('dragStart', create_proxy(event_handler))

    def on_focus_change(self, handler: Callable[[int, Union[str, int]], None]) -> None:
        """Fires on moving focus to a new item."""
        self.add_event_handler('focusChange', handler)

    def on_item_mouse_over(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """Fires on moving the mouse pointer over an item."""
        self.add_event_handler('itemMouseOver', handler)

    def on_item_right_click(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """Fires on right-clicking an item."""
        self.add_event_handler('itemRightClick', handler)
