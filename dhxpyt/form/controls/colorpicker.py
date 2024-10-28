"""
ColorPicker control implementation for the Form widget
"""

import json
from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .colorpicker_config import ColorpickerConfig


class Colorpicker:
    def __init__(self, config: ColorpickerConfig = None, widget_parent: Any = None):
        """Initializes the ColorPicker control."""
        if config is None:
            config = ColorPickerConfig()
        config_dict = config.to_dict()
        self.colorpicker = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ ColorPicker API Functions """

    def blur(self) -> None:
        """Removes focus from the ColorPicker control."""
        self.colorpicker.blur()

    def clear(self) -> None:
        """Clears the value of the ColorPicker control."""
        self.colorpicker.clear()

    def clear_validate(self) -> None:
        """Clears validation of the ColorPicker control."""
        self.colorpicker.clearValidate()

    def destructor(self) -> None:
        """Removes the ColorPicker instance and releases the occupied resources."""
        self.colorpicker.destructor()

    def disable(self) -> None:
        """Disables the ColorPicker control."""
        self.colorpicker.disable()

    def enable(self) -> None:
        """Enables the ColorPicker control."""
        self.colorpicker.enable()

    def focus(self) -> None:
        """Sets focus to the ColorPicker control."""
        self.colorpicker.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.colorpicker.getProperties().to_py()

    def get_value(self) -> str:
        """Returns the current value of the ColorPicker control (in Hex format)."""
        return self.colorpicker.getValue()

    def get_widget(self) -> Any:
        """Returns the DHTMLX ColorPicker widget attached to the control."""
        return self.colorpicker.getWidget()

    def hide(self) -> None:
        """Hides the ColorPicker control."""
        self.colorpicker.hide()

    def is_disabled(self) -> bool:
        """Checks whether the ColorPicker control is disabled."""
        return self.colorpicker.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the ColorPicker control is visible on the page."""
        return self.colorpicker.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.colorpicker.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: str) -> None:
        """Sets the value for the ColorPicker control (Hex format)."""
        self.colorpicker.setValue(value)

    def show(self) -> None:
        """Shows the ColorPicker control on the page."""
        self.colorpicker.show()

    def validate(self, silent: bool = False, validate_value: str = None) -> bool:
        """Validates the ColorPicker control."""
        return self.colorpicker.validate(silent, validate_value)

    """ ColorPicker Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.colorpicker.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[str, bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[str], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[str, bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.colorpicker.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.colorpicker.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[str, bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.colorpicker.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.colorpicker.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.colorpicker.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[str], None]) -> None:
        """Fires when the control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[str], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[str], None]) -> None:
        """Fires when the control has received focus."""
        self.add_event_handler('focus', handler)

    def on_input(self, handler: Callable[[str], None]) -> None:
        """Fires when a user enters the value manually."""
        self.add_event_handler('input', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the control is in focus."""
        self.add_event_handler('keydown', handler)
