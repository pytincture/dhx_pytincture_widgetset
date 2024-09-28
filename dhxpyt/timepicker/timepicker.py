"""
TimePicker widget implementation
"""

from typing import Any, Callable, Dict, Optional, Union
import json
from pyodide.ffi import create_proxy
import js

from .timepicker_config import TimepickerConfig


class Timepicker:
    def __init__(self, config: TimepickerConfig = None, widget_parent: str = None):
        """
        Initializes the TimePicker widget.

        :param config: (Optional) The TimePickerConfig object containing the timepicker configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the timepicker will be attached.
        """
        if config is None:
            config = TimepickerConfig()
        config_dict = config.to_dict()

        # Create the TimePicker instance
        self.timepicker = js.dhx.TimePicker.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))


    """ TimePicker API Functions """

    def clear(self) -> None:
        """Clears the value set in the timepicker."""
        self.timepicker.clear()

    def destructor(self) -> None:
        """Destroys the timepicker instance and releases occupied resources."""
        self.timepicker.destructor()

    def get_value(self, as_object: bool = False) -> Union[Dict[str, int], str]:
        """
        Returns the current value of a TimePicker.

        :param as_object: (Optional) Specifies that the value will be returned as an object. False by default.
        :return: Either an object or a string with the value of the timepicker.
        """
        return self.timepicker.getValue(as_object)

    def paint(self) -> None:
        """Repaints a timepicker on a page."""
        self.timepicker.paint()

    def set_value(self, value: Union[Dict[str, int], str, int, list, object]) -> None:
        """
        Sets value for a TimePicker.

        :param value: The value to be set for a timepicker.
        """
        self.timepicker.setValue(value)

    """ TimePicker Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Adds an event handler for the specified event.

        :param event_name: The name of the event.
        :param handler: The handler function to attach.
        """
        event_proxy = create_proxy(handler)
        self.timepicker.events.on(event_name, event_proxy)

    def on_after_apply(self, handler: Callable[[Union[str, Dict[str, int]]], None]) -> None:
        """
        Fires after saving the timepicker value.

        :param handler: The handler function with parameter value (str or dict).
        """
        def event_handler(value):
            handler(value)
        self.timepicker.events.on('afterApply', create_proxy(event_handler))

    def on_after_close(self, handler: Callable[[Union[str, Dict[str, int]]], None]) -> None:
        """
        Fires after closing the timepicker.

        :param handler: The handler function with parameter value (str or dict).
        """
        def event_handler(value):
            handler(value)
        self.timepicker.events.on('afterClose', create_proxy(event_handler))

    def on_before_apply(self, handler: Callable[[Union[str, Dict[str, int]]], Union[bool, None]]) -> None:
        """
        Fires before saving the timepicker value.

        :param handler: The handler function with parameter value (str or dict). Return False to prevent saving.
        """
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.timepicker.events.on('beforeApply', create_proxy(event_handler))

    def on_before_change(self, handler: Callable[[Union[str, Dict[str, int]]], Union[bool, None]]) -> None:
        """
        Fires before change of the timepicker value.

        :param handler: The handler function with parameter value (str or dict). Return False to prevent changing.
        """
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.timepicker.events.on('beforeChange', create_proxy(event_handler))

    def on_before_close(self, handler: Callable[[Union[str, Dict[str, int]]], Union[bool, None]]) -> None:
        """
        Fires before closing the timepicker.

        :param handler: The handler function with parameter value (str or dict). Return False to prevent closing.
        """
        def event_handler(value):
            result = handler(value)
            if result is False:
                return js.Boolean(False)
        self.timepicker.events.on('beforeClose', create_proxy(event_handler))

    def on_change(self, handler: Callable[[Union[str, Dict[str, int]]], None]) -> None:
        """
        Fires on change of the timepicker value.

        :param handler: The handler function with parameter value (str or dict).
        """
        def event_handler(value):
            handler(value)
        self.timepicker.events.on('change', create_proxy(event_handler))
