"""
Input control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .input_config import InputConfig


class Input:
    def __init__(self, config: InputConfig = None, widget_parent: Any = None):
        """Initializes the Input control."""
        if config is None:
            config = InputConfig()
        config_dict = config.to_dict()
        self.input = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Input API Functions """

    def blur(self) -> None:
        """Removes focus from the Input control."""
        self.input.blur()

    def clear(self) -> None:
        """Clears the value of the Input control."""
        self.input.clear()

    def clear_validate(self) -> None:
        """Clears validation of the Input control."""
        self.input.clearValidate()

    def destructor(self) -> None:
        """Removes the Input instance and releases the occupied resources."""
        self.input.destructor()

    def disable(self) -> None:
        """Disables the Input control."""
        self.input.disable()

    def enable(self) -> None:
        """Enables the Input control."""
        self.input.enable()

    def focus(self) -> None:
        """Sets focus to the Input control."""
        self.input.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.input.getProperties().to_py()

    def get_value(self) -> Union[str, int]:
        """Returns the current value of the Input control."""
        return self.input.getValue()

    def hide(self) -> None:
        """Hides the Input control."""
        self.input.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Input control is disabled."""
        return self.input.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Input control is visible on the page."""
        return self.input.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.input.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: Union[str, int]) -> None:
        """Sets the value for the Input control."""
        self.input.setValue(value)

    def show(self) -> None:
        """Shows the Input control on the page."""
        self.input.show()

    def validate(self, silent: bool = False, validate_value: Union[str, int] = None) -> bool:
        """Validates the Input control."""
        return self.input.validate(silent, validate_value)

    """ Input Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.input.events.on(event_name, event_proxy)

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

    def on_before_change(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.input.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.input.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, int], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.input.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.input.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.input.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires when the control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires when the control has received focus."""
        self.add_event_handler('focus', handler)

    def on_input(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires when a user types some text in the input."""
        self.add_event_handler('input', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the control is in focus."""
        self.add_event_handler('keydown', handler)
