"""
pyTincture Button control implementation
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .button_config import ButtonConfig


class Button:
    def __init__(self, config: ButtonConfig = None, widget_parent: Any = None):
        """Initializes the Button control."""
        if config is None:
            config = ButtonConfig()
        config_dict = config.to_dict()
        self.button = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Button API Functions """

    def blur(self) -> None:
        """Removes focus from the Button control."""
        self.button.blur()

    def destructor(self) -> None:
        """Removes the Button instance and releases the occupied resources."""
        self.button.destructor()

    def disable(self) -> None:
        """Disables the Button control."""
        self.button.disable()

    def enable(self) -> None:
        """Enables the Button control."""
        self.button.enable()

    def focus(self) -> None:
        """Sets focus to the Button control."""
        self.button.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns an object with the available configuration attributes of the control."""
        return self.button.getProperties().to_py()

    def hide(self) -> None:
        """Hides the Button control."""
        self.button.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Button control is disabled."""
        return self.button.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Button control is visible on the page."""
        return self.button.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing available configuration attributes of the control dynamically."""
        self.button.setProperties(js.JSON.parse(json.dumps(properties)))

    def show(self) -> None:
        """Shows the Button control on the page."""
        self.button.show()

    """ Button Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.button.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[str, bool], None]) -> None:
        """Fires after the Button control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[str], None]) -> None:
        """Fires after the Button control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.button.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[str, bool], Union[bool, None]]) -> None:
        """Fires before the Button control is hidden."""
        def event_handler(text, init):
            result = handler(text, init)
            if result is False:
                return js.Boolean(False)
        self.button.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before the Button control is shown."""
        def event_handler(text):
            result = handler(text)
            if result is False:
                return js.Boolean(False)
        self.button.events.on('beforeShow', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[str], None]) -> None:
        """Fires when the Button control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_click(self, handler: Callable[[Any], None]) -> None:
        """Fires after a click on the Button control."""
        self.add_event_handler('click', handler)

    def on_focus(self, handler: Callable[[str], None]) -> None:
        """Fires when the Button control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the Button control is in focus."""
        self.add_event_handler('keydown', handler)
