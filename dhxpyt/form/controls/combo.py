"""
Combo control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union, List
import json
from pyodide.ffi import create_proxy
import js

from .combo_config import ComboConfig


class Combo:
    def __init__(self, config: ComboConfig = None, widget_parent: Any = None):
        """Initializes the Combo control."""
        if config is None:
            config = ComboConfig()
        config_dict = config.to_dict()
        self.combo = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Combo API Functions """

    def blur(self) -> None:
        """Removes focus from the Combo control."""
        self.combo.blur()

    def clear(self) -> None:
        """Clears the value of the Combo control."""
        self.combo.clear()

    def clear_validate(self) -> None:
        """Clears validation of the Combo control."""
        self.combo.clearValidate()

    def destructor(self) -> None:
        """Removes the Combo instance and releases the occupied resources."""
        self.combo.destructor()

    def disable(self) -> None:
        """Disables the Combo control."""
        self.combo.disable()

    def enable(self) -> None:
        """Enables the Combo control."""
        self.combo.enable()

    def focus(self) -> None:
        """Sets focus to the Combo control."""
        self.combo.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.combo.getProperties().to_py()

    def get_value(self) -> Union[str, int, List[Union[str, int]]]:
        """Returns IDs of options which are currently selected in the Combo control."""
        value = self.combo.getValue()
        if isinstance(value, js.JsProxy):
            return value.to_py()
        else:
            return value

    def get_widget(self) -> Any:
        """Returns the ComboBox widget attached to the Combo control."""
        return self.combo.getWidget()

    def hide(self) -> None:
        """Hides the Combo control."""
        self.combo.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Combo control is disabled."""
        return self.combo.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Combo control is visible on the page."""
        return self.combo.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.combo.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, ids: Union[str, int, List[Union[str, int]]]) -> None:
        """Sets the value for the Combo control."""
        self.combo.setValue(ids)

    def show(self) -> None:
        """Shows the Combo control on the page."""
        self.combo.show()

    def validate(self, silent: bool = False, validate_value: Union[str, List[str]] = None) -> bool:
        """Validates the Combo control."""
        return self.combo.validate(silent, validate_value)

    """ Combo Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.combo.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Union[str, int, List[Union[str, int]]], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[Union[str, int, List[Union[str, int]]], bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(ids):
            result = handler(ids.to_py() if isinstance(ids, js.JsProxy) else ids)
            if result is False:
                return js.Boolean(False)
        self.combo.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.combo.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, int, List[Union[str, int]]], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(ids, init):
            result = handler(ids.to_py() if isinstance(ids, js.JsProxy) else ids, init)
            if result is False:
                return js.Boolean(False)
        self.combo.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(ids):
            result = handler(ids.to_py() if isinstance(ids, js.JsProxy) else ids)
            if result is False:
                return js.Boolean(False)
        self.combo.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(ids):
            result = handler(ids.to_py() if isinstance(ids, js.JsProxy) else ids)
            if result is False:
                return js.Boolean(False)
        self.combo.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], None]) -> None:
        """Fires when the control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], None]) -> None:
        """Fires when the control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any, Union[str, int, None]], None]) -> None:
        """Fires when any key is pressed and an option is in focus."""
        self.add_event_handler('keydown', handler)
