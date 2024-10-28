"""
Container control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union
import json
from pyodide.ffi import create_proxy
import js

from .container_config import ContainerConfig


class Container:
    def __init__(self, config: ContainerConfig = None, widget_parent: Any = None):
        """Initializes the Container control."""
        if config is None:
            config = ContainerConfig()
        config_dict = config.to_dict()
        self.container = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Container API Functions """

    def attach(self, widget: Any) -> None:
        """Attaches a DHTMLX widget into the Container control."""
        self.container.attach(widget)

    def attach_html(self, html: str) -> None:
        """Attaches an HTML content into the Container control."""
        self.container.attachHTML(html)

    def disable(self) -> None:
        """Disables the Container control."""
        self.container.disable()

    def enable(self) -> None:
        """Enables the Container control."""
        self.container.enable()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration properties of the control."""
        return self.container.getProperties().to_py()

    def hide(self) -> None:
        """Hides the Container control."""
        self.container.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Container control is disabled."""
        return self.container.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Container control is visible on the page."""
        return self.container.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration properties of the control dynamically."""
        self.container.setProperties(js.JSON.parse(json.dumps(properties)))

    def show(self) -> None:
        """Shows the Container control on the page."""
        self.container.show()

    """ Container Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.container.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after properties have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before properties are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.container.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(init):
            result = handler(init)
            if result is False:
                return js.Boolean(False)
        self.container.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler():
            result = handler()
            if result is False:
                return js.Boolean(False)
        self.container.events.on('beforeShow', create_proxy(event_handler))
