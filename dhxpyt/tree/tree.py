"""
Tree widget implementation
"""

from typing import Any, Callable, Dict, List, Optional, Union
import json
from pyodide.ffi import create_proxy
import js

from .tree_config import TreeConfig


class Tree:
    def __init__(self, config: TreeConfig = None, widget_parent: str = None):
        """
        Initializes the Tree widget.

        :param config: (Optional) The TreeConfig object containing the tree configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the tree will be attached.
        """
        if config is None:
            config = TreeConfig()
        config_dict = config.to_dict()
        # Create the Tree instance
        self.tree = js.dhx.Tree.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Tree API Functions """

    def check_item(self, id: Union[str, int]) -> None:
        """Checks the checkbox of a tree item and all its sub-items."""
        self.tree.checkItem(id)

    def collapse(self, id: Union[str, int]) -> None:
        """Collapses a tree item by ID."""
        self.tree.collapse(id)

    def collapse_all(self) -> None:
        """Collapses all expanded tree items."""
        self.tree.collapseAll()

    def destructor(self) -> None:
        """Releases the occupied resources."""
        self.tree.destructor()

    def edit_item(self, id: Union[str, int], config: dict = None) -> None:
        """Edits a tree item."""
        self.tree.editItem(id, config)

    def expand(self, id: Union[str, int]) -> None:
        """Expands a tree item by ID."""
        self.tree.expand(id)

    def expand_all(self) -> None:
        """Expands all collapsed tree items."""
        self.tree.expandAll()

    def focus_item(self, id: Union[str, int]) -> None:
        """Sets focus to a tree item and moves the scroll to it."""
        self.tree.focusItem(id)

    def get_checked(self) -> List[Union[str, int]]:
        """Gets all checked tree items."""
        return self.tree.getChecked().to_py()

    def get_state(self) -> Dict[str, Dict[str, Union[int, bool]]]:
        """Gets the state of the tree."""
        return self.tree.getState().to_py()

    def paint(self) -> None:
        """Repaints the tree on the page."""
        self.tree.paint()

    def set_state(self, state: Dict[str, Dict[str, Union[int, bool]]]) -> None:
        """Sets the state for the tree."""
        self.tree.setState(js.JSON.parse(json.dumps(state)))

    def toggle(self, id: Union[str, int]) -> None:
        """Opens or closes a tree item by ID."""
        self.tree.toggle(id)

    def uncheck_item(self, id: Union[str, int]) -> None:
        """Unchecks the checkbox of a tree item and all its sub-items."""
        self.tree.uncheckItem(id)

    """ Tree Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Adds an event handler for the specified event.
        
        :param event_name: The name of the event.
        :param handler: The handler function to attach.
        """
        event_proxy = create_proxy(handler)
        self.tree.events.on(event_name, event_proxy)

    def on_after_check(self, handler: Callable[[int, Union[str, int], bool], None]) -> None:
        """Fires after the state of an item is changed (checked)."""
        self.add_event_handler('afterCheck', handler)

    def on_after_collapse(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires after collapsing a tree item."""
        self.add_event_handler('afterCollapse', handler)

    def on_after_drag(self, handler: Callable[[dict, Any], Any]) -> None:
        """Fires after dragging an item is finished."""
        self.add_event_handler('afterDrag', handler)

    def on_after_drop(self, handler: Callable[[dict, Any], None]) -> None:
        """Fires before the user has finished dragging an item but after the mouse button is released."""
        self.add_event_handler('afterDrop', handler)

    def on_after_edit_end(self, handler: Callable[[str, Union[str, int]], None]) -> None:
        """Fires after editing a tree item is finished."""
        self.add_event_handler('afterEditEnd', handler)

    def on_after_edit_start(self, handler: Callable[[str, Union[str, int]], None]) -> None:
        """Fires after editing of a tree item has started."""
        self.add_event_handler('afterEditStart', handler)

    def on_after_expand(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires after expanding a tree item."""
        self.add_event_handler('afterExpand', handler)

    def on_before_check(self, handler: Callable[[int, Union[str, int]], Union[bool, None]]) -> None:
        """Fires before the state of an item is changed (checking)."""
        def event_handler(index, id):
            result = handler(index, id)
            if result is False:
                return js.Boolean(False)
        self.tree.events.on('beforeCheck', create_proxy(event_handler))

    def on_before_collapse(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before collapsing a tree item."""
        def event_handler(id):
            result = handler(id)
            if result is False:
                return js.Boolean(False)
        self.tree.events.on('beforeCollapse', create_proxy(event_handler))

    def on_before_drag(self, handler: Callable[[dict, Any, Any], Union[bool, None]]) -> None:
        """Fires before dragging of an item starts."""
        def event_handler(data, event, ghost):
            result = handler(data, event, ghost)
            if result is False:
                return js.Boolean(False)
        self.tree.events.on('beforeDrag', create_proxy(event_handler))

    def on_before_drop(self, handler: Callable[[dict, Any], Union[bool, None]]) -> None:
        """Fires before the user has finished dragging an item and released the mouse button."""
        def event_handler(data, event):
            result = handler(data, event)
            if result is False:
                return js.Boolean(False)
        self.tree.events.on('beforeDrop', create_proxy(event_handler))

    def on_before_edit_end(self, handler: Callable[[str, Union[str, int]], Union[bool, None]]) -> None:
        """Fires before editing a tree item is finished."""
        def event_handler(value, id):
            result = handler(value, id)
            if result is False:
                return js.Boolean(False)
        self.tree.events.on('beforeEditEnd', create_proxy(event_handler))

    def on_before_edit_start(self, handler: Callable[[str, Union[str, int]], Union[bool, None]]) -> None:
        """Fires before editing of a tree item starts."""
        def event_handler(value, id):
            result = handler(value, id)
            if result is False:
                return js.Boolean(False)
        self.tree.events.on('beforeEditStart', create_proxy(event_handler))

    def on_before_expand(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before expanding a tree item."""
        def event_handler(id):
            result = handler(id)
            if result is False:
                return js.Boolean(False)
        self.tree.events.on('beforeExpand', create_proxy(event_handler))
    
    # Additional event handlers like dragStart, itemClick, itemDblClick can also be added similarly
