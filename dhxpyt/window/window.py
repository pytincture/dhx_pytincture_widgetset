"""
Window widget implementation
"""

from typing import Any, Callable, Dict, Optional, Union
import json
from pyodide.ffi import create_proxy
import js

from .window_config import WindowConfig


class Window:
    def __init__(self, config: WindowConfig = None, widget_parent: str = None):
        """
        Initializes the Window widget.

        :param config: (Optional) The WindowConfig object containing the window configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the window will be attached.
        """
        if config is None:
            config = WindowConfig()
        config_dict = config.to_dict()
        # Create the Window instance
        self.window = js.dhx.Window.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Window API Functions """

    def attach(self, name: Union[str, Any], config: dict = None) -> None:
        """Attaches a DHTMLX component to the window."""
        self.window.attach(name, config)

    def attach_html(self, html: str) -> None:
        """Adds an HTML content into a DHTMLX window."""
        self.window.attachHTML(html)

    def destructor(self) -> None:
        """Releases the occupied resources."""
        self.window.destructor()

    def get_container(self) -> Any:
        """Returns the HTML element of the window."""
        return self.window.getContainer()

    def get_position(self) -> Dict[str, int]:
        """Gets the position of the window."""
        return self.window.getPosition().to_py()

    def get_size(self) -> Dict[str, int]:
        """Gets the size of the window."""
        return self.window.getSize().to_py()

    def get_widget(self) -> Any:
        """Returns the widget attached to the window."""
        return self.window.getWidget()

    def hide(self) -> None:
        """Hides the window."""
        self.window.hide()

    def is_full_screen(self) -> bool:
        """Checks whether the window is in full-screen mode."""
        return self.window.isFullScreen()

    def is_visible(self) -> bool:
        """Checks whether the window is visible."""
        return self.window.isVisible()

    def paint(self) -> None:
        """Repaints the window on the page."""
        self.window.paint()

    def set_full_screen(self) -> None:
        """Switches the window to full-screen mode."""
        self.window.setFullScreen()

    def set_position(self, left: int, top: int) -> None:
        """Sets the position of the window."""
        self.window.setPosition(left, top)

    def set_size(self, width: int, height: int) -> None:
        """Sets the size of the window."""
        self.window.setSize(width, height)

    def show(self, left: Optional[int] = None, top: Optional[int] = None) -> None:
        """Shows the window on the page."""
        self.window.show(left, top)

    def unset_full_screen(self) -> None:
        """Switches the window from full-screen mode to windowed mode."""
        self.window.unsetFullScreen()

    """ Window Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Adds an event handler for the specified event.

        :param event_name: The name of the event.
        :param handler: The handler function to attach.
        """
        event_proxy = create_proxy(handler)
        self.window.events.on(event_name, event_proxy)

    def on_after_hide(self, handler: Callable[[Dict[str, int], Optional[Any]], None]) -> None:
        """Fires after the window is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Dict[str, int]], None]) -> None:
        """Fires after the window is shown."""
        self.add_event_handler('afterShow', handler)

    def on_before_hide(self, handler: Callable[[Dict[str, int], Optional[Any]], Union[bool, None]]) -> None:
        """Fires before the window is hidden."""
        def event_handler(position, event=None):
            result = handler(position, event)
            if result is False:
                return js.Boolean(False)
        self.window.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Dict[str, int]], Union[bool, None]]) -> None:
        """Fires before the window is shown."""
        def event_handler(position):
            result = handler(position)
            if result is False:
                return js.Boolean(False)
        self.window.events.on('beforeShow', create_proxy(event_handler))

    def on_header_double_click(self, handler: Callable[[Any], None]) -> None:
        """Fires on double-clicking the window's header."""
        self.add_event_handler('headerDoubleClick', handler)

    def on_move(self, handler: Callable[[Dict[str, int], Dict[str, int], Dict[str, bool]], None]) -> None:
        """Fires on moving the window."""
        self.add_event_handler('move', handler)

    def on_resize(self, handler: Callable[[Dict[str, int], Dict[str, int], Dict[str, bool]], None]) -> None:
        """Fires on resizing the window."""
        self.add_event_handler('resize', handler)
