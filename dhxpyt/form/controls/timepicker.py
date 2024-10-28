"""
TimePicker control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .timepicker_config import TimepickerConfig


class Timepicker:
    def __init__(self, config: TimepickerConfig = None, widget_parent: Any = None):
        """Initializes the TimePicker control."""
        if config is None:
            config = TimepickerConfig()
        config_dict = config.to_dict()
        self.timepicker = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ TimePicker API Functions """

    def blur(self) -> None:
        """Removes focus from the TimePicker control."""
        self.timepicker.blur()

    def clear(self) -> None:
        """Clears the value of the TimePicker control."""
        self.timepicker.clear()

    def clear_validate(self) -> None:
        """Clears validation of the TimePicker control."""
        self.timepicker.clearValidate()

    def destructor(self) -> None:
        """Removes the TimePicker instance and releases the occupied resources."""
        self.timepicker.destructor()

    def disable(self) -> None:
        """Disables the TimePicker control."""
        self.timepicker.disable()

    def enable(self) -> None:
        """Enables the TimePicker control."""
        self.timepicker.enable()

    def focus(self) -> None:
        """Sets focus to the TimePicker control."""
        self.timepicker.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.timepicker.getProperties().to_py()

    def get_value(self, as_object: bool = False) -> Union[str, Dict[str, Any]]:
        """Returns the current value of the TimePicker control."""
        return self.timepicker.getValue(as_object)

    def get_widget(self) -> Any:
        """Returns the DHTMLX TimePicker widget attached to the TimePicker control."""
        return self.timepicker.getWidget()

    def hide(self) -> None:
        """Hides the TimePicker control."""
        self.timepicker.hide()

    def is_disabled(self) -> bool:
        """Checks whether the TimePicker control is disabled."""
        return self.timepicker.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the TimePicker control is visible on the page."""
        return self.timepicker.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.timepicker.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: Union[str, int, float, Dict[str, Any], list]) -> None:
        """Sets the value for the TimePicker control."""
        self.timepicker.setValue(value)

    def show(self) -> None:
        """Shows the TimePicker control on the page."""
        self.timepicker.show()

    def validate(self, silent: bool = False, validate_value: str = None) -> bool:
        """Validates the TimePicker control."""
        return self.timepicker.validate(silent, validate_value)

    """ TimePicker Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.timepicker.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Union[str, Dict[str, Any]], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Union[str, Dict[str, Any]]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[Union[str, Dict[str, Any]], bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change(self, handler: Callable[[Union[str, Dict[str, Any]]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.timepicker.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.timepicker.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, Dict[str, Any]], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.timepicker.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Union[str, Dict[str, Any]]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.timepicker.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Union[str, Dict[str, Any]]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.timepicker.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Union[str, Dict[str, Any]]], None]) -> None:
        """Fires when the TimePicker control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Union[str, Dict[str, Any]]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Union[str, Dict[str, Any]]], None]) -> None:
        """Fires when the TimePicker control has received focus."""
        self.add_event_handler('focus', handler)

    def on_input(self, handler: Callable[[str], None]) -> None:
        """Fires when a user enters the value of a control in the input manually."""
        self.add_event_handler('input', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the TimePicker control is in focus."""
        self.add_event_handler('keydown', handler)
