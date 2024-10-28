"""
CheckboxGroup control implementation for the Form widget
"""

import json
from typing import Any, Callable, Dict, Union
from pyodide.ffi import create_proxy
import js

from .checkboxgroup_config import CheckboxGroupConfig


class CheckboxGroup:
    def __init__(self, config: CheckboxGroupConfig = None, widget_parent: Any = None):
        """Initializes the CheckboxGroup control."""
        if config is None:
            config = CheckboxGroupConfig()
        config_dict = config.to_dict()
        self.checkboxgroup = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ CheckboxGroup API Functions """

    def blur(self) -> None:
        """Removes focus from the CheckboxGroup control."""
        self.checkboxgroup.blur()

    def clear(self) -> None:
        """Clears the value of the CheckboxGroup control."""
        self.checkboxgroup.clear()

    def clear_validate(self) -> None:
        """Clears validation of the CheckboxGroup control."""
        self.checkboxgroup.clearValidate()

    def destructor(self) -> None:
        """Removes the CheckboxGroup instance and releases the occupied resources."""
        self.checkboxgroup.destructor()

    def disable(self, id: str = None) -> None:
        """Disables the CheckboxGroup control or a specific checkbox."""
        self.checkboxgroup.disable(id)

    def enable(self, id: str = None) -> None:
        """Enables the CheckboxGroup control or a specific checkbox."""
        self.checkboxgroup.enable(id)

    def focus(self, id: str = None) -> None:
        """Sets focus to a checkbox of the CheckboxGroup control."""
        self.checkboxgroup.focus(id)

    def get_properties(self, id: str = None) -> Dict[str, Any]:
        """Returns configuration attributes of the control or a specific checkbox."""
        return self.checkboxgroup.getProperties(id).to_py()

    def get_value(self, id: str = None) -> Union[str, bool, Dict[str, Union[str, bool]]]:
        """Returns the current value/state of the control or a specific checkbox."""
        return self.checkboxgroup.getValue(id)

    def hide(self, id: str = None) -> None:
        """Hides the CheckboxGroup control or a specific checkbox."""
        self.checkboxgroup.hide(id)

    def is_checked(self, id: str = None) -> Union[bool, Dict[str, bool]]:
        """Checks whether a checkbox is checked."""
        return self.checkboxgroup.isChecked(id)

    def is_disabled(self, id: str = None) -> bool:
        """Checks whether the control or a specific checkbox is disabled."""
        return self.checkboxgroup.isDisabled(id)

    def is_visible(self, id: str = None) -> bool:
        """Checks whether the control or a specific checkbox is visible."""
        return self.checkboxgroup.isVisible(id)

    def set_properties(self, arg: Union[str, Dict[str, Any]] = None, properties: Dict[str, Any] = None) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        if isinstance(arg, str):
            self.checkboxgroup.setProperties(arg, js.JSON.parse(json.dumps(properties)))
        elif isinstance(arg, dict):
            props = {k: js.JSON.parse(json.dumps(v)) for k, v in arg.items()}
            self.checkboxgroup.setProperties(props)
        else:
            self.checkboxgroup.setProperties(js.JSON.parse(json.dumps(properties or {})))

    def set_value(self, value: Dict[str, Union[str, bool]]) -> None:
        """Sets the value for the CheckboxGroup control."""
        self.checkboxgroup.setValue(js.JSON.parse(json.dumps(value)))

    def show(self, id: str = None) -> None:
        """Shows the CheckboxGroup control or a specific checkbox."""
        self.checkboxgroup.show(id)

    def validate(self, silent: bool = False) -> bool:
        """Validates the CheckboxGroup control."""
        return self.checkboxgroup.validate(silent)

    """ CheckboxGroup Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.checkboxgroup.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Dict[str, Union[str, bool]], str, bool], None]) -> None:
        """Fires after the control or its checkbox is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Dict[str, Union[str, bool]], str], None]) -> None:
        """Fires after the control or its checkbox is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[Dict[str, Union[str, bool]], bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change(self, handler: Callable[[Dict[str, Union[str, bool]]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.checkboxgroup.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.checkboxgroup.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Dict[str, Union[str, bool]], str, bool], Union[bool, None]]) -> None:
        """Fires before the control or its checkbox is hidden."""
        def event_handler(value, id=None, init=None):
            result = handler(value.to_py(), id, init)
            if result is False:
                return js.Boolean(False)
        self.checkboxgroup.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Dict[str, Union[str, bool]], str], Union[bool, None]]) -> None:
        """Fires before the control or its checkbox is shown."""
        def event_handler(value, id=None):
            result = handler(value.to_py(), id)
            if result is False:
                return js.Boolean(False)
        self.checkboxgroup.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Dict[str, Union[str, bool]]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.checkboxgroup.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Dict[str, Union[str, bool]], str], None]) -> None:
        """Fires when the control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Dict[str, Union[str, bool]]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Dict[str, Union[str, bool]], str], None]) -> None:
        """Fires when the control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any, str], None]) -> None:
        """Fires when any key is pressed and a checkbox is in focus."""
        self.add_event_handler('keydown', handler)
