"""
RadioGroup control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union, List
import json
from pyodide.ffi import create_proxy
import js

from .radiogroup_config import RadioGroupConfig


class RadioGroup:
    def __init__(self, config: RadioGroupConfig = None, widget_parent: Any = None):
        """Initializes the RadioGroup control."""
        if config is None:
            config = RadioGroupConfig()
        config_dict = config.to_dict()
        print(config_dict)
        self.radiogroup = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ RadioGroup API Functions """

    def blur(self) -> None:
        """Removes focus from the RadioGroup control."""
        self.radiogroup.blur()

    def clear(self) -> None:
        """Clears the value of the RadioGroup control."""
        self.radiogroup.clear()

    def clear_validate(self) -> None:
        """Clears validation of the RadioGroup control."""
        self.radiogroup.clearValidate()

    def destructor(self) -> None:
        """Removes the RadioGroup instance and releases the occupied resources."""
        self.radiogroup.destructor()

    def disable(self, id: str = None) -> None:
        """Disables the RadioGroup control or a specific element inside the control."""
        self.radiogroup.disable(id)

    def enable(self, id: str = None) -> None:
        """Enables the RadioGroup control or a specific element inside the control."""
        self.radiogroup.enable(id)

    def focus(self, id: str = None) -> None:
        """Sets focus to the radio button of the RadioGroup control by its id."""
        self.radiogroup.focus(id)

    def get_properties(self, id: str = None) -> Dict[str, Any]:
        """Returns the configuration attributes of the control or a specific radio button."""
        props = self.radiogroup.getProperties(id)
        return props.to_py() if props else {}

    def get_value(self) -> str:
        """Returns the current value of the RadioGroup control."""
        return self.radiogroup.getValue()

    def hide(self, id: str = None) -> None:
        """Hides either a radio button of RadioGroup or the whole RadioGroup."""
        self.radiogroup.hide(id)

    def is_disabled(self, id: str = None) -> bool:
        """Checks whether the RadioGroup control or a specific element is disabled."""
        return self.radiogroup.isDisabled(id)

    def is_visible(self, id: str = None) -> bool:
        """Checks whether the RadioGroup control or a specific element is visible."""
        return self.radiogroup.isVisible(id)

    def set_properties(self, arg: Union[str, Dict[str, Any]], props: Dict[str, Any] = None) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        if isinstance(arg, str):
            # arg is id, props is properties
            self.radiogroup.setProperties(arg, js.JSON.parse(json.dumps(props)))
        else:
            # arg is properties, props is None
            self.radiogroup.setProperties(js.JSON.parse(json.dumps(arg)))

    def set_value(self, value: str) -> None:
        """Sets the value for the RadioGroup control."""
        self.radiogroup.setValue(value)

    def show(self, id: str = None) -> None:
        """Shows either a radio button of RadioGroup or the whole RadioGroup."""
        self.radiogroup.show(id)

    def validate(self, silent: bool = False) -> bool:
        """Validates the RadioGroup control."""
        return self.radiogroup.validate(silent)

    """ RadioGroup Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.radiogroup.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[str, str, bool], None]) -> None:
        """Fires after the control or its radio button is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[str, str], None]) -> None:
        """Fires after the control or its radio button is shown."""
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
        self.radiogroup.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.radiogroup.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[str, str, bool], Union[bool, None]]) -> None:
        """Fires before the control or its radio button is hidden."""
        def event_handler(value, id, init):
            result = handler(value, id, init)
            if result is False:
                return js.Boolean(False)
        self.radiogroup.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[str, str], Union[bool, None]]) -> None:
        """Fires before the control or its radio button is shown."""
        def event_handler(value, id):
            result = handler(value, id)
            if result is False:
                return js.Boolean(False)
        self.radiogroup.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.radiogroup.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[str, str], None]) -> None:
        """Fires when the RadioGroup control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[str], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[str, str], None]) -> None:
        """Fires when the RadioGroup control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any, str], None]) -> None:
        """Fires when any key is pressed and a radio button is in focus."""
        self.add_event_handler('keydown', handler)
