"""
Spacer control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .spacer_config import SpacerConfig


class Spacer:
    def __init__(self, config: SpacerConfig = None, widget_parent: Any = None):
        """Initializes the Spacer control."""
        if config is None:
            config = SpacerConfig()
        config_dict = config.to_dict()
        self.spacer = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Spacer API Functions """

    def destructor(self) -> None:
        """Removes the Spacer instance and releases the occupied resources."""
        self.spacer.destructor()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.spacer.getProperties().to_py()

    def hide(self) -> None:
        """Hides the Spacer control."""
        self.spacer.hide()

    def is_visible(self) -> bool:
        """Checks whether the Spacer control is visible on the page."""
        return self.spacer.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.spacer.setProperties(js.JSON.parse(json.dumps(properties)))

    def show(self) -> None:
        """Shows the Spacer control on the page."""
        self.spacer.show()

    """ Spacer Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.spacer.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.spacer.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(init):
            result = handler(init)
            if result is False:
                return js.Boolean(False)
        self.spacer.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler():
            result = handler()
            if result is False:
                return js.Boolean(False)
        self.spacer.events.on('beforeShow', create_proxy(event_handler))
