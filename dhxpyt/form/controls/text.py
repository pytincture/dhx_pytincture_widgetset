"""
Text control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .text_config import TextConfig


class Text:
    def __init__(self, config: TextConfig = None, widget_parent: Any = None):
        """Initializes the Text control."""
        if config is None:
            config = TextConfig()
        config_dict = config.to_dict()
        self.text = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Text API Functions """

    def clear(self) -> None:
        """Clears the value of the Text control."""
        self.text.clear()

    def destructor(self) -> None:
        """Removes the Text instance and releases the occupied resources."""
        self.text.destructor()

    def disable(self) -> None:
        """Disables the Text control."""
        self.text.disable()

    def enable(self) -> None:
        """Enables the Text control."""
        self.text.enable()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.text.getProperties().to_py()

    def get_value(self) -> Union[str, int]:
        """Returns the current value of the Text control."""
        return self.text.getValue()

    def hide(self) -> None:
        """Hides the Text control."""
        self.text.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Text control is disabled."""
        return self.text.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Text control is visible on the page."""
        return self.text.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.text.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: Union[str, int]) -> None:
        """Sets the value for the Text control."""
        self.text.setValue(value)

    def show(self) -> None:
        """Shows the Text control on the page."""
        self.text.show()

    """ Text Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.text.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Union[str, int], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[Union[str, int], bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.text.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, int], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.text.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.text.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.text.events.on('beforeValidate', create_proxy(event_handler))

    def on_change(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)
