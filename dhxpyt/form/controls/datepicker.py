"""
DatePicker control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .datepicker_config import DatepickerConfig


class Datepicker:
    def __init__(self, config: DatepickerConfig = None, widget_parent: Any = None):
        """Initializes the DatePicker control."""
        if config is None:
            config = DatePickerConfig()
        config_dict = config.to_dict()
        self.datepicker = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ DatePicker API Functions """

    def blur(self) -> None:
        """Removes focus from the DatePicker control."""
        self.datepicker.blur()

    def clear(self) -> None:
        """Clears the value of the DatePicker control."""
        self.datepicker.clear()

    def clear_validate(self) -> None:
        """Clears validation of the DatePicker control."""
        self.datepicker.clearValidate()

    def destructor(self) -> None:
        """Removes the DatePicker instance and releases the occupied resources."""
        self.datepicker.destructor()

    def disable(self) -> None:
        """Disables the DatePicker control."""
        self.datepicker.disable()

    def enable(self) -> None:
        """Enables the DatePicker control."""
        self.datepicker.enable()

    def focus(self) -> None:
        """Sets focus to the DatePicker control."""
        self.datepicker.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.datepicker.getProperties().to_py()

    def get_value(self, as_date: bool = False) -> Union[str, Any]:
        """Returns the current value of the DatePicker control."""
        return self.datepicker.getValue(as_date)

    def get_widget(self) -> Any:
        """Returns the DHTMLX Calendar widget attached to the DatePicker control."""
        return self.datepicker.getWidget()

    def hide(self) -> None:
        """Hides the DatePicker control."""
        self.datepicker.hide()

    def is_disabled(self) -> bool:
        """Checks whether the DatePicker control is disabled."""
        return self.datepicker.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the DatePicker control is visible on the page."""
        return self.datepicker.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.datepicker.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: Union[str, Any]) -> None:
        """Sets a date in the DatePicker control."""
        self.datepicker.setValue(value)

    def show(self) -> None:
        """Shows the DatePicker control on the page."""
        self.datepicker.show()

    def validate(self, silent: bool = False, validate_value: Union[str, Any] = None) -> bool:
        """Validates the DatePicker control."""
        return self.datepicker.validate(silent, validate_value)

    """ DatePicker Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.datepicker.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Union[str, Any], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Union[str, Any]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[Union[str, Any], bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change(self, handler: Callable[[Union[str, Any]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.datepicker.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.datepicker.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, Any], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.datepicker.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Union[str, Any]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.datepicker.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Union[str, Any]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.datepicker.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Union[str, Any]], None]) -> None:
        """Fires when the control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Union[str, Any]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Union[str, Any]], None]) -> None:
        """Fires when the control has received focus."""
        self.add_event_handler('focus', handler)

    def on_input(self, handler: Callable[[str], None]) -> None:
        """Fires when a user enters the value manually."""
        self.add_event_handler('input', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the control is in focus."""
        self.add_event_handler('keydown', handler)
