"""
Textarea control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .textarea_config import TextareaConfig


class Textarea:
    def __init__(self, config: TextareaConfig = None, widget_parent: Any = None):
        """Initializes the Textarea control."""
        if config is None:
            config = TextareaConfig()
        config_dict = config.to_dict()
        self.textarea = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Textarea API Functions """

    def blur(self) -> None:
        """Removes focus from the Textarea control."""
        self.textarea.blur()

    def clear(self) -> None:
        """Clears the value of the Textarea control."""
        self.textarea.clear()

    def clear_validate(self) -> None:
        """Clears validation of the Textarea control."""
        self.textarea.clearValidate()

    def destructor(self) -> None:
        """Removes the Textarea instance and releases the occupied resources."""
        self.textarea.destructor()

    def disable(self) -> None:
        """Disables the Textarea control."""
        self.textarea.disable()

    def enable(self) -> None:
        """Enables the Textarea control."""
        self.textarea.enable()

    def focus(self) -> None:
        """Sets focus to the Textarea control."""
        self.textarea.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.textarea.getProperties().to_py()

    def get_value(self) -> str:
        """Returns the current value of the Textarea control."""
        return self.textarea.getValue()

    def hide(self) -> None:
        """Hides the Textarea control."""
        self.textarea.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Textarea control is disabled."""
        return self.textarea.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Textarea control is visible on the page."""
        return self.textarea.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.textarea.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: str) -> None:
        """Sets the value for the Textarea control."""
        self.textarea.setValue(value)

    def show(self) -> None:
        """Shows the Textarea control on the page."""
        self.textarea.show()

    def validate(self, silent: bool = False, validate_value: str = None) -> bool:
        """Validates the Textarea control."""
        return self.textarea.validate(silent, validate_value)

    """ Textarea Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.textarea.events.on(event_name, event_proxy)

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
        self.textarea.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.textarea.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[str, bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.textarea.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.textarea.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.textarea.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[str], None]) -> None:
        """Fires when the Textarea control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[str], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[str], None]) -> None:
        """Fires when the Textarea control has received focus."""
        self.add_event_handler('focus', handler)

    def on_input(self, handler: Callable[[str], None]) -> None:
        """Fires when a user types some text in the textarea."""
        self.add_event_handler('input', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the Textarea control is in focus."""
        self.add_event_handler('keydown', handler)
