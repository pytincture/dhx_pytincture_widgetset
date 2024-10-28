"""
Slider control implementation for the Form widget
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .slider_config import SliderConfig


class Slider:
    def __init__(self, config: SliderConfig = None, widget_parent: Any = None):
        """Initializes the Slider control."""
        if config is None:
            config = SliderConfig()
        config_dict = config.to_dict()
        self.slider = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Slider API Functions """

    def blur(self) -> None:
        """Removes focus from a thumb of a Slider control."""
        self.slider.blur()

    def clear(self) -> None:
        """Clears the value of the Slider control."""
        self.slider.clear()

    def destructor(self) -> None:
        """Removes the Slider instance and releases the occupied resources."""
        self.slider.destructor()

    def disable(self) -> None:
        """Disables the Slider control."""
        self.slider.disable()

    def enable(self) -> None:
        """Enables the Slider control."""
        self.slider.enable()

    def focus(self, extra: bool = False) -> None:
        """Sets focus to a thumb of a Slider control."""
        self.slider.focus(extra)

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.slider.getProperties().to_py()

    def get_value(self) -> List[float]:
        """Returns the current value of the Slider control."""
        return self.slider.getValue().to_py()

    def get_widget(self) -> Any:
        """Returns the DHTMLX Slider widget attached to a Slider control."""
        return self.slider.getWidget()

    def hide(self) -> None:
        """Hides the Slider control."""
        self.slider.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Slider control is disabled."""
        return self.slider.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Slider control is visible on the page."""
        return self.slider.isVisible()

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.slider.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: Union[float, List[float]]) -> None:
        """Sets the value for the Slider control."""
        self.slider.setValue(value)

    def show(self) -> None:
        """Shows the Slider control on the page."""
        self.slider.show()

    """ Slider Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.slider.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[List[float], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[List[float]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_before_change(self, handler: Callable[[List[float]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.slider.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.slider.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[List[float], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value.to_py(), init)
            if result is False:
                return js.Boolean(False)
        self.slider.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[List[float]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.slider.events.on('beforeShow', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[List[float]], None]) -> None:
        """Fires when the Slider control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[List[float]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[List[float]], None]) -> None:
        """Fires when the Slider control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the Slider control is in focus."""
        self.add_event_handler('keydown', handler)
