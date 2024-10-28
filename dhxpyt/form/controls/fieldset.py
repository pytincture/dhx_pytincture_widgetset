"""
Fieldset control implementation for the Form widget
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .fieldset_config import FieldsetConfig


class Fieldset:
    def __init__(self, config: FieldsetConfig = None, widget_parent: Any = None):
        """Initializes the Fieldset control."""
        if config is None:
            config = FieldsetConfig()
        config_dict = config.to_dict()
        self.fieldset = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Fieldset API Functions """

    def destructor(self) -> None:
        """Removes the Fieldset instance and releases the occupied resources."""
        self.fieldset.destructor()

    def disable(self) -> None:
        """Disables the Fieldset control."""
        self.fieldset.disable()

    def enable(self) -> None:
        """Enables the Fieldset control."""
        self.fieldset.enable()

    def for_each(self, callback: Callable[[Any, int, List[Any]], None], tree: bool = False) -> None:
        """Allows iterating through all the nested items."""
        def py_callback(item, index, array):
            item_py = item.to_py()
            array_py = array.to_py()
            callback(item_py, index, array_py)
        self.fieldset.forEach(create_proxy(py_callback), tree)

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.fieldset.getProperties().to_py()

    def hide(self) -> None:
        """Hides the Fieldset control."""
        self.fieldset.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Fieldset control is disabled."""
        return self.fieldset.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Fieldset control is visible on the page."""
        return self.fieldset.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.fieldset.setProperties(js.JSON.parse(json.dumps(properties)))

    def show(self) -> None:
        """Shows the Fieldset control on the page."""
        self.fieldset.show()

    """ Fieldset Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.fieldset.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.fieldset.events.on('beforeChangeProperties', create_proxy(event_handler))
