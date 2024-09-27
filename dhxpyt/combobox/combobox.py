"""
pyTincture Combobox widget implementation
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .combobox_config import ComboboxConfig

class Combobox:
    def __init__(self, config: ComboboxConfig = None, widget_parent: Any = None):
        """Initializes the Combobox instance."""
        if config is None:
            config = ComboboxConfig()
        config_dict = config.to_dict()
        self.combobox = js.dhx.Combobox.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))
    
    """ Combobox API Functions """
    
    def add_option(self, value: Union[Dict[str, Any], str], join: bool = True) -> None:
        """Adds a new item into the list of Combobox options."""
        self.combobox.addOption(value, join)
    
    def blur(self) -> None:
        """Removes focus from Combobox."""
        self.combobox.blur()
    
    def clear(self) -> None:
        """Clears the value set in the Combobox."""
        self.combobox.clear()
    
    def destructor(self) -> None:
        """Removes a Combobox instance and releases occupied resources."""
        self.combobox.destructor()
    
    def disable(self) -> None:
        """Disables Combobox on a page."""
        self.combobox.disable()
    
    def enable(self) -> None:
        """Enables a disabled Combobox."""
        self.combobox.enable()
    
    def focus(self) -> None:
        """Sets focus in the input without opening a popup with options."""
        self.combobox.focus()
    
    def get_value(self, as_array: bool = False) -> Union[str, int, List[Union[str, int]]]:
        """Gets id(s) of items from data collection selected in Combobox."""
        return self.combobox.getValue(as_array)
    
    def is_disabled(self) -> bool:
        """Checks whether a Combobox is disabled."""
        return self.combobox.isDisabled()
    
    def paint(self) -> None:
        """Repaints the Combobox."""
        self.combobox.paint()
    
    def set_value(self, ids: Union[str, int, List[Union[str, int]]]) -> None:
        """Selects option(s) in Combobox."""
        self.combobox.setValue(ids)
    
    """ Combobox Events """
    
    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.combobox.events.on(event_name, event_proxy)
    
    def on_after_close(self, handler: Callable[[], None]) -> None:
        """Fires after closing a list with options."""
        self.add_event_handler('afterClose', handler)
    
    def on_after_open(self, handler: Callable[[], None]) -> None:
        """Fires after opening a list with options."""
        self.add_event_handler('afterOpen', handler)
    
    def on_before_change(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], Union[bool, None]]) -> None:
        """Fires before selection of a new option."""
        def event_handler(ids):
            result = handler(ids)
            if result is False:
                return js.Boolean(False)
        event_proxy = create_proxy(event_handler)
        self.combobox.events.on('beforeChange', event_proxy)
    
    def on_before_close(self, handler: Callable[[], Union[bool, None]]) -> None:
        """Fires before closing a list with options."""
        def event_handler():
            result = handler()
            if result is False:
                return js.Boolean(False)
        event_proxy = create_proxy(event_handler)
        self.combobox.events.on('beforeClose', event_proxy)
    
    def on_before_open(self, handler: Callable[[], Union[bool, None]]) -> None:
        """Fires before opening a list with options."""
        def event_handler():
            result = handler()
            if result is False:
                return js.Boolean(False)
        event_proxy = create_proxy(event_handler)
        self.combobox.events.on('beforeOpen', event_proxy)
    
    def on_blur(self, handler: Callable[[], None]) -> None:
        """Fires when Combobox has lost focus."""
        self.add_event_handler('blur', handler)
    
    def on_change(self, handler: Callable[[Union[str, int, List[Union[str, int]]]], None]) -> None:
        """Fires when a new option is selected."""
        self.add_event_handler('change', handler)
    
    def on_focus(self, handler: Callable[[], None]) -> None:
        """Fires when Combobox has received focus."""
        self.add_event_handler('focus', handler)
    
    def on_input(self, handler: Callable[[str], None]) -> None:
        """Fires on typing text in an input of Combobox."""
        self.add_event_handler('input', handler)
    
    def on_keydown(self, handler: Callable[[Any, Union[str, int, None]], None]) -> None:
        """Fires when any key is pressed and an option of Combobox is in focus."""
        self.add_event_handler('keydown', handler)
    
    """ Combobox Properties """
    
    @property
    def css(self) -> str:
        """Gets or sets the CSS classes for Combobox."""
        return self.combobox.config.css
    
    @css.setter
    def css(self, value: str) -> None:
        self.combobox.config.css = value
    
    @property
    def data(self) -> List[Dict[str, Any]]:
        """Gets or sets the data objects for Combobox."""
        return self.combobox.config.data
    
    @data.setter
    def data(self, value: List[Dict[str, Any]]) -> None:
        self.combobox.data.parse(js.JSON.parse(json.dumps(value)))
    
    @property
    def disabled(self) -> bool:
        """Gets or sets whether the Combobox is disabled."""
        return self.combobox.config.disabled
    
    @disabled.setter
    def disabled(self, value: bool) -> None:
        self.combobox.config.disabled = value
    
    @property
    def multiselection(self) -> bool:
        """Gets or sets whether multiple selection is enabled."""
        return self.combobox.config.multiselection
    
    @multiselection.setter
    def multiselection(self, value: bool) -> None:
        self.combobox.config.multiselection = value
    
    @property
    def placeholder(self) -> str:
        """Gets or sets the placeholder text."""
        return self.combobox.config.placeholder
    
    @placeholder.setter
    def placeholder(self, value: str) -> None:
        self.combobox.config.placeholder = value
    
    @property
    def read_only(self) -> bool:
        """Gets or sets whether the Combobox is read-only."""
        return self.combobox.config.readOnly
    
    @read_only.setter
    def read_only(self, value: bool) -> None:
        self.combobox.config.readOnly = value
    
    @property
    def value(self) -> Union[str, int, List[Union[str, int]]]:
        """Gets or sets the selected value(s) of the Combobox."""
        return self.get_value()
    
    @value.setter
    def value(self, ids: Union[str, int, List[Union[str, int]]]) -> None:
        self.set_value(ids)
    
    # Add other properties similarly...
    
    # For properties that are functions or complex types, you may need to handle them differently
    
    @property
    def filter(self) -> Callable[[Dict[str, Any], str], bool]:
        """Gets or sets a custom function for filtering Combobox options."""
        return self._filter_function
    
    @filter.setter
    def filter(self, value: Callable[[Dict[str, Any], str], bool]) -> None:
        self._filter_function = value
        def js_filter(item, target):
            return value(item.to_py(), target)
        self.combobox.config.filter = create_proxy(js_filter)
    
    # For the 'template' property
    @property
    def template(self) -> Callable[[Any], str]:
        """Gets or sets a template for displaying options."""
        return self._template_function
    
    @template.setter
    def template(self, value: Callable[[Any], str]) -> None:
        self._template_function = value
        self.combobox.config.template = create_proxy(value)
