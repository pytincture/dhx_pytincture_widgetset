"""
Select control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union, List
import json
from pyodide.ffi import create_proxy
import js

from .select_config import SelectConfig


class Select:
    def __init__(self, config: SelectConfig = None, widget_parent: Any = None):
        """Initializes the Select control."""
        if config is None:
            config = SelectConfig()
        config_dict = config.to_dict()
        self.select = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Select API Functions """

    def blur(self) -> None:
        """Removes focus from the Select control."""
        self.select.blur()

    def clear(self) -> None:
        """Clears the value of the Select control."""
        self.select.clear()

    def clear_validate(self) -> None:
        """Clears validation of the Select control."""
        self.select.clearValidate()

    def destructor(self) -> None:
        """Removes the Select instance and releases the occupied resources."""
        self.select.destructor()

    def disable(self, value: Union[str, int] = None) -> None:
        """Disables the Select control or a specific option."""
        self.select.disable(value)

    def enable(self, value: Union[str, int] = None) -> None:
        """Enables the Select control or a specific option."""
        self.select.enable(value)

    def focus(self) -> None:
        """Sets focus to the Select control."""
        self.select.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.select.getProperties().to_py()

    def get_options(self) -> List[Dict[str, Any]]:
        """Returns an array of Select options."""
        options = self.select.getOptions()
        return [option.to_py() for option in options]

    def get_value(self) -> Union[str, int]:
        """Returns the current value of the Select control."""
        return self.select.getValue()

    def hide(self) -> None:
        """Hides the Select control."""
        self.select.hide()

    def is_disabled(self, value: Union[str, int] = None) -> bool:
        """Checks whether the Select control or a specific option is disabled."""
        return self.select.isDisabled(value)

    def is_visible(self) -> bool:
        """Checks whether the Select control is visible on the page."""
        return self.select.isVisible()

    def set_options(self, options: List[Dict[str, Any]]) -> None:
        """Allows changing a list of Select options dynamically."""
        self.select.setOptions(js.JSON.parse(json.dumps(options)))

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.select.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: Union[str, int]) -> None:
        """Sets the value for the Select control."""
        self.select.setValue(value)

    def show(self) -> None:
        """Shows the Select control on the page."""
        self.select.show()

    def validate(self, silent: bool = False) -> bool:
        """Validates the Select control."""
        return self.select.validate(silent)

    """ Select Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.select.events.on(event_name, event_proxy)

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
        self.select.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_options(self, handler: Callable[[List[Dict[str, Any]]], Union[bool, None]]) -> None:
        """Fires before changing a list of Select options."""
        def event_handler(options):
            options_py = [option.to_py() for option in options]
            result = handler(options_py)
            if result is False:
                return js.Boolean(False)
        self.select.events.on('beforeChangeOptions', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.select.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, int], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.select.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.select.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Union[str, int]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.select.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires when the control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_change_options(self, handler: Callable[[List[Dict[str, Any]]], None]) -> None:
        """Fires on changing a list of Select options."""
        self.add_event_handler('changeOptions', handler)

    def on_focus(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires when the control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the control is in focus."""
        self.add_event_handler('keydown', handler)
