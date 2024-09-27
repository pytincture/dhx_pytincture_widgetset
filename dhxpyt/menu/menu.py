"""
pyTincture Menu widget implementation
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .menu_config import MenuConfig, MenuItemConfig

class Menu:
    def __init__(self, config: MenuConfig = None, widget_parent: Any = None):
        """Initializes the Menu instance."""
        if config is None:
            config = MenuConfig()
        config_dict = config.to_dict()
        self.menu = js.dhx.Menu.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))
    
    """ Menu API Functions """
    
    def destructor(self) -> None:
        """Removes the Menu instance and releases occupied resources."""
        self.menu.destructor()
    
    def disable(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Disables and dims an item(s) of Menu."""
        self.menu.disable(ids)
    
    def enable(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Enables a disabled item(s) of Menu."""
        self.menu.enable(ids)
    
    def get_selected(self) -> List[Union[str, int]]:
        """Returns an array of IDs of selected items."""
        return list(self.menu.getSelected())
    
    def hide(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Hides an item(s) of Menu."""
        self.menu.hide(ids)
    
    def is_disabled(self, id: Union[str, int]) -> bool:
        """Checks whether an item of Menu is disabled."""
        return self.menu.isDisabled(id)
    
    def is_selected(self, id: Union[str, int]) -> bool:
        """Checks whether a specified Menu item is selected."""
        return self.menu.isSelected(id)
    
    def paint(self) -> None:
        """Repaints Menu on a page."""
        self.menu.paint()
    
    def select(self, id: Union[str, int], unselect: bool = True) -> None:
        """Selects a specified item of Menu."""
        self.menu.select(id, unselect)
    
    def show(self, ids: Union[str, int, List[Union[str, int]]] = None) -> None:
        """Shows an item(s) of Menu."""
        self.menu.show(ids)
    
    def show_at(self, elem: Union[str, Any], show_at: str = "bottom") -> None:
        """Shows a context menu."""
        self.menu.showAt(elem, show_at)
    
    def unselect(self, id: Union[str, int] = None) -> None:
        """Unselects a selected Menu item."""
        self.menu.unselect(id)
    
    """ Menu Events """
    
    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.menu.events.on(event_name, event_proxy)
    
    def on_after_hide(self, handler: Callable[[Any], None]) -> None:
        """Fires after hiding a sub-item of Menu."""
        self.add_event_handler('afterHide', handler)
    
    def on_before_hide(self, handler: Callable[[Union[str, int], Any], Union[bool, None]]) -> None:
        """Fires before hiding a sub-item of Menu."""
        def event_handler(id, events):
            result = handler(id, events)
            if result is False:
                return js.Boolean(False)
        event_proxy = create_proxy(event_handler)
        self.menu.events.on('beforeHide', event_proxy)
    
    def on_click(self, handler: Callable[[Union[str, int], Any], None]) -> None:
        """Fires after a click on a button or a menu option."""
        self.add_event_handler('click', handler)
    
    def on_keydown(self, handler: Callable[[Any, Union[str, int]], None]) -> None:
        """Fires when any key is pressed and an option of Menu is in focus."""
        self.add_event_handler('keydown', handler)
    
    def on_open_menu(self, handler: Callable[[Union[str, int]], None]) -> None:
        """Fires on expanding a menu item."""
        self.add_event_handler('openMenu', handler)
    
    """ Menu Properties """
    
    @property
    def css(self) -> str:
        """Gets or sets the CSS classes for Menu."""
        return self.menu.config.css
    
    @css.setter
    def css(self, value: str) -> None:
        self.menu.config.css = value
    
    @property
    def data(self) -> List[Dict[str, Any]]:
        """Gets or sets the data objects for Menu."""
        return self.menu.config.data
    
    @data.setter
    def data(self, value: List[Dict[str, Any]]) -> None:
        self.menu.data.parse(js.JSON.parse(json.dumps(value)))
    
    @property
    def menu_css(self) -> str:
        """Gets or sets the CSS classes for Menu controls with nested items."""
        return self.menu.config.menuCss
    
    @menu_css.setter
    def menu_css(self, value: str) -> None:
        self.menu.config.menuCss = value
    
    @property
    def navigation_type(self) -> str:
        """Gets or sets the action that opens menu options ('click' or 'pointer')."""
        return self.menu.config.navigationType
    
    @navigation_type.setter
    def navigation_type(self, value: str) -> None:
        self.menu.config.navigationType = value
