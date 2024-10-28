"""
Checkbox control implementation for the Form widget
"""

import json
from typing import Any, Callable, Dict, Union
from pyodide.ffi import create_proxy
import js

from .checkbox_config import CheckboxConfig


class Checkbox:
    def __init__(self, config: CheckboxConfig = None, widget_parent: Any = None):
        """Initializes the Checkbox control."""
        if config is None:
            config = CheckboxConfig()
        config_dict = config.to_dict()
        self.checkbox = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Checkbox API Functions """

    def blur(self) -> None:
        """Removes focus from the Checkbox control."""
        self.checkbox.blur()

    def clear(self) -> None:
        """Clears the value of the Checkbox control."""
        self.checkbox.clear()

    def clear_validate(self) -> None:
        """Clears validation of the Checkbox control."""
        self.checkbox.clearValidate()

    def destructor(self) -> None:
        """Removes the Checkbox instance and releases the occupied resources."""
        self.checkbox.destructor()

    def disable(self) -> None:
        """Disables the Checkbox control."""
        self.checkbox.disable()

    def enable(self) -> None:
        """Enables the Checkbox control."""
        self.checkbox.enable()

    def focus(self) -> None:
        """Sets focus to the Checkbox control."""
        self.checkbox.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.checkbox.getProperties().to_py()

    def get_value(self) -> Union[str, bool]:
        """Returns the current value/state of the Checkbox control."""
        return self.checkbox.getValue()

    def hide(self) -> None:
        """Hides the Checkbox control."""
        self.checkbox.hide()

    def is_checked(self) -> bool:
        """Checks whether the Checkbox control is checked."""
        return self.checkbox.isChecked()

    def is_disabled(self) -> bool:
        """Checks whether the Checkbox control is disabled."""
        return self.checkbox.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Checkbox control is visible on the page."""
        return self.checkbox.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.checkbox.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, checked: bool) -> None:
        """Sets the state for the Checkbox control."""
        self.checkbox.setValue(checked)

    def show(self) -> None:
        """Shows the Checkbox control on the page."""
        self.checkbox.show()

    def validate(self, silent: bool = False) -> bool:
        """Validates the Checkbox control."""
        return self.checkbox.validate(silent)

    """ Checkbox Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.checkbox.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Union[str, bool], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Union[str, bool]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[Union[str, bool], bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change(self, handler: Callable[[Union[str, bool]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.checkbox.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.checkbox.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, bool], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.checkbox.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Union[str, bool]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.checkbox.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Union[str, bool]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.checkbox.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Union[str, bool]], None]) -> None:
        """Fires when the control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Union[str, bool]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Union[str, bool]], None]) -> None:
        """Fires when the control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the control is in focus."""
        self.add_event_handler('keydown', handler)
