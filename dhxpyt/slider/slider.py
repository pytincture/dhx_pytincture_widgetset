"""
Slider widget implementation
"""

from typing import Any, Callable, Dict, List, Optional, Union
import json
from pyodide.ffi import create_proxy
import js

from .slider_config import SliderConfig


class Slider:
    def __init__(self, config: SliderConfig, widget_parent: str = None):
        """
        Initializes the Slider widget.

        :param config: The SliderConfig object containing the slider configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the slider will be attached.
        """
        config_dict = config.to_dict()

        # Handle the tickTemplate function separately
        tick_template = None
        if 'tickTemplate' in config_dict:
            tick_template = config_dict.pop('tickTemplate')
            # Create a proxy for the JavaScript side
            config_dict['tickTemplate'] = create_proxy(tick_template)

        # Create the Slider instance
        self.slider = js.dhx.Slider.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))
        if tick_template:
            # Assign the tickTemplate function
            self.slider.config.tickTemplate = config_dict['tickTemplate']

    """ Slider API Functions """

    def blur(self) -> None:
        """Removes focus from a thumb of Slider."""
        self.slider.blur()

    def destructor(self) -> None:
        """Destroys the slider instance and releases occupied resources."""
        self.slider.destructor()

    def disable(self) -> None:
        """Disables the slider."""
        self.slider.disable()

    def enable(self) -> None:
        """Enables the slider."""
        self.slider.enable()

    def focus(self, extra: bool = None) -> None:
        """
        Sets focus to a thumb of Slider.

        :param extra: (Optional) If the range mode is activated, True will set focus to the second thumb.
        """
        if extra is not None:
            self.slider.focus(extra)
        else:
            self.slider.focus()

    def get_value(self) -> List[float]:
        """
        Returns the current value of Slider.

        :return: An array with the current value of the slider.
        """
        value = self.slider.getValue()
        return value.to_py()

    def is_disabled(self) -> bool:
        """
        Checks whether Slider is disabled.

        :return: True if the slider is disabled; otherwise, False.
        """
        return self.slider.isDisabled()

    def paint(self) -> None:
        """Repaints Slider on a page."""
        self.slider.paint()

    def set_value(self, value: Union[str, float, List[float]]) -> None:
        """
        Sets a value for the slider.

        :param value: The value to be set for Slider.
        """
        self.slider.setValue(value)

    """ Slider Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Adds an event handler for the specified event.

        :param event_name: The name of the event.
        :param handler: The handler function to attach.
        """
        event_proxy = create_proxy(handler)
        self.slider.events.on(event_name, event_proxy)

    def on_before_change(self, handler: Callable[[float, float, bool], Union[bool, None]]) -> None:
        """
        Fires before changing of the slider value.

        :param handler: The handler function with parameters value (float), oldValue (float), isRange (bool).
                        Return False to prevent changing the slider value.
        """
        def event_handler(value, oldValue, isRange):
            result = handler(value, oldValue, isRange)
            if result is False:
                return js.Boolean(False)
        self.slider.events.on('beforeChange', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[], None]) -> None:
        """
        Fires when a thumb of Slider has lost focus.

        :param handler: The handler function.
        """
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[float, float, bool], None]) -> None:
        """
        Fires on change of the slider value.

        :param handler: The handler function with parameters value (float), oldValue (float), isRange (bool).
        """
        def event_handler(value, oldValue, isRange):
            handler(value, oldValue, isRange)
        self.slider.events.on('change', create_proxy(event_handler))

    def on_focus(self, handler: Callable[[], None]) -> None:
        """
        Fires when a thumb of Slider has received focus.

        :param handler: The handler function.
        """
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """
        Fires when any key is pressed and a thumb of Slider is in focus.

        :param handler: The handler function with parameter event (KeyboardEvent).
        """
        def event_handler(event):
            handler(event)
        self.slider.events.on('keydown', create_proxy(event_handler))

    def on_mousedown(self, handler: Callable[[Any], None]) -> None:
        """
        Fires on pressing the left mouse button over the slider thumb.

        :param handler: The handler function with parameter event (Event).
        """
        def event_handler(event):
            handler(event)
        self.slider.events.on('mousedown', create_proxy(event_handler))

    def on_mouseup(self, handler: Callable[[Any], None]) -> None:
        """
        Fires on releasing the left mouse button over the slider thumb.

        :param handler: The handler function with parameter event (Event).
        """
        def event_handler(event):
            handler(event)
        self.slider.events.on('mouseUp', create_proxy(event_handler))

