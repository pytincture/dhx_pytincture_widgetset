"""
Toggle control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .toggle_config import ToggleConfig


class Toggle:
    def __init__(self, config: ToggleConfig = None, widget_parent: Any = None):
        """Initializes the Toggle control."""
        if config is None:
            config = ToggleConfig()
        config_dict = config.to_dict()
        self.toggle = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Toggle API Functions """

    def blur(self) -> None:
        """Removes focus from the Toggle control."""
        self.toggle.blur()

    def destructor(self) -> None:
        """Removes the Toggle instance and releases the occupied resources."""
        self.toggle.destructor()

    def disable(self) -> None:
        """Disables the Toggle control."""
        self.toggle.disable()

    def enable(self) -> None:
        """Enables the Toggle control."""
        self.toggle.enable()

    def focus(self) -> None:
        """Sets focus to the Toggle control."""
        self.toggle.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.toggle.getProperties().to_py()

    def get_value(self) -> Union[str, int, bool]:
        """Returns the current value/state of the Toggle control."""
        return self.toggle.getValue()

    def hide(self) -> None:
        """Hides the Toggle control."""
        self.toggle.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Toggle control is disabled."""
        return self.toggle.isDisabled()

    def is_selected(self) -> bool:
        """Checks whether the selected state is enabled."""
        return self.toggle.isSelected()

    def is_visible(self) -> bool:
        """Checks whether the Toggle control is visible on the page."""
        return self.toggle.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.toggle.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, selected: bool) -> None:
        """Sets the state for the Toggle control."""
        self.toggle.setValue(selected)

    def show(self) -> None:
        """Shows the Toggle control on the page."""
        self.toggle.show()

    """ Toggle Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.toggle.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Union[str, int, bool], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Union[str, int, bool]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_before_change(self, handler: Callable[[Union[str, int, bool]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.toggle.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.toggle.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, int, bool], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value, init)
            if result is False:
                return js.Boolean(False)
        self.toggle.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Union[str, int, bool]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.toggle.events.on('beforeShow', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Union[str, int, bool]], None]) -> None:
        """Fires when the Toggle control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Union[str, int, bool]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Union[str, int, bool]], None]) -> None:
        """Fires when the Toggle control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the Toggle control is in focus."""
        self.add_event_handler('keydown', handler)
