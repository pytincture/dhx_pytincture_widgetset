"""
ToggleGroup control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union, List
import json
from pyodide.ffi import create_proxy
import js

from .togglegroup_config import ToggleGroupConfig


class ToggleGroup:
    def __init__(self, config: ToggleGroupConfig = None, widget_parent: Any = None):
        """Initializes the ToggleGroup control."""
        if config is None:
            config = ToggleGroupConfig()
        config_dict = config.to_dict()
        self.togglegroup = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ ToggleGroup API Functions """

    def blur(self) -> None:
        """Removes focus from the ToggleGroup control."""
        self.togglegroup.blur()

    def destructor(self) -> None:
        """Removes the ToggleGroup instance and releases the occupied resources."""
        self.togglegroup.destructor()

    def disable(self, id: str = None) -> None:
        """Disables the ToggleGroup control or a specific element."""
        self.togglegroup.disable(id)

    def enable(self, id: str = None) -> None:
        """Enables the ToggleGroup control or a specific element."""
        self.togglegroup.enable(id)

    def focus(self, id: str = None) -> None:
        """Sets focus to an option of the ToggleGroup control by its id."""
        self.togglegroup.focus(id)

    def get_properties(self, id: str = None) -> Dict[str, Any]:
        """Returns the configuration attributes of the control or its toggle."""
        props = self.togglegroup.getProperties(id)
        return props.to_py() if props else {}

    def get_value(self, id: str = None) -> Union[str, int, bool, Dict[str, Union[str, int, bool]]]:
        """Returns the current value/state of a toggle(s)."""
        return self.togglegroup.getValue(id).to_py()

    def hide(self, id: str = None) -> None:
        """Hides either an option of ToggleGroup or the whole ToggleGroup."""
        self.togglegroup.hide(id)

    def is_disabled(self, id: str = None) -> bool:
        """Checks whether the ToggleGroup control or a specific element is disabled."""
        return self.togglegroup.isDisabled(id)

    def is_selected(self, id: str = None) -> Union[bool, Dict[str, bool]]:
        """Checks whether a toggle of the ToggleGroup control is selected."""
        result = self.togglegroup.isSelected(id)
        return result.to_py() if isinstance(result, js.Object) else result

    def is_visible(self, id: str = None) -> bool:
        """Checks whether the ToggleGroup control or a specific element is visible."""
        return self.togglegroup.isVisible(id)

    def set_properties(self, config: Dict[str, Any], id: str = None) -> None:
        """Allows changing configuration attributes dynamically."""
        self.togglegroup.setProperties(js.JSON.parse(json.dumps(config)), id)

    def set_value(self, value: Dict[str, bool]) -> None:
        """Defines the state of the option's elements."""
        self.togglegroup.setValue(js.JSON.parse(json.dumps(value)))

    def show(self, id: str = None) -> None:
        """Shows either an option of ToggleGroup or the whole ToggleGroup."""
        self.togglegroup.show(id)

    """ ToggleGroup Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.togglegroup.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any], str], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Dict[str, Any], str, bool], None]) -> None:
        """Fires after the control or its toggle is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Dict[str, Any], str], None]) -> None:
        """Fires after the control or its toggle is shown."""
        self.add_event_handler('afterShow', handler)

    def on_before_change(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.togglegroup.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any], str], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties, id=None):
            result = handler(properties.to_py(), id)
            if result is False:
                return js.Boolean(False)
        self.togglegroup.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Dict[str, Any], str, bool], Union[bool, None]]) -> None:
        """Fires before the control or its toggle is hidden."""
        def event_handler(value, id=None, init=False):
            result = handler(value.to_py(), id, init)
            if result is False:
                return js.Boolean(False)
        self.togglegroup.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Dict[str, Any], str], Union[bool, None]]) -> None:
        """Fires before the control or its toggle is shown."""
        def event_handler(value, id=None):
            result = handler(value.to_py(), id)
            if result is False:
                return js.Boolean(False)
        self.togglegroup.events.on('beforeShow', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Dict[str, Any], str], None]) -> None:
        """Fires when the ToggleGroup control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Dict[str, Any], str], None]) -> None:
        """Fires when the ToggleGroup control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any, str], None]) -> None:
        """Fires when any key is pressed and a toggle is in focus."""
        self.add_event_handler('keydown', handler)
