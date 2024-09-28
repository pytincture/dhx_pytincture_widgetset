"""
Popup widget implementation
"""

from typing import Any, Callable, Dict, Optional, Union
import json
from pyodide.ffi import create_proxy
import js

from .popup_config import PopupConfig, PopupShowConfig


class Popup:
    def __init__(self, config: PopupConfig = None):
        """
        Initializes the Popup widget.

        :param config: (Optional) The PopupConfig object containing the popup configuration.
        """
        if config is None:
            config = PopupConfig()
        config_dict = config.to_dict()
        # Create the Popup instance
        self.popup = js.dhx.Popup.new(None, js.JSON.parse(json.dumps(config_dict)))

    """ Popup API Functions """

    def attach(self, name: Union[str, Any], config: Dict[str, Any] = None) -> Any:
        """
        Attaches a DHTMLX component to the Popup.

        :param name: The name or object of a component.
        :param config: (Optional) The configuration settings of a component.
        :return: The object of the attached component.
        """
        if config is None:
            config = {}
        component = self.popup.attach(name, js.JSON.parse(json.dumps(config)))
        return component

    def attach_html(self, html: str) -> None:
        """
        Adds HTML content into the Popup.

        :param html: An HTML content to be added into the popup.
        """
        self.popup.attachHTML(html)

    def destructor(self) -> None:
        """
        Removes the Popup instance and releases occupied resources.
        """
        self.popup.destructor()

    def get_container(self) -> Any:
        """
        Returns the HTML element of the Popup.

        :return: The HTML element.
        """
        return self.popup.getContainer()

    def get_widget(self) -> Any:
        """
        Returns the widget attached to the Popup.

        :return: The widget attached to the Popup.
        """
        return self.popup.getWidget()

    def hide(self) -> None:
        """
        Hides the Popup.
        """
        self.popup.hide()

    def is_visible(self) -> bool:
        """
        Checks whether the Popup is visible.

        :return: True if the Popup is visible; otherwise, False.
        """
        return self.popup.isVisible()

    def paint(self) -> None:
        """
        Repaints the Popup on the page.
        """
        self.popup.paint()

    def show(self, node: Any, config: PopupShowConfig = None) -> None:
        """
        Shows the Popup.

        :param node: The container to place the Popup in.
        :param config: (Optional) The configuration object of the Popup.
        """
        if config is None:
            config = {}
        self.popup.show(node, js.JSON.parse(json.dumps(config)))

    """ Popup Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """
        Adds an event handler for the specified event.

        :param event_name: The name of the event.
        :param handler: The handler function to attach.
        """
        event_proxy = create_proxy(handler)
        self.popup.events.on(event_name, event_proxy)

    def on_after_hide(self, handler: Callable[[Any], None]) -> None:
        """
        Fires after the Popup is hidden.

        :param handler: The handler function with parameter e (Event).
        """
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Any], None]) -> None:
        """
        Fires after the Popup is shown.

        :param handler: The handler function with parameter node (HTMLElement).
        """
        self.add_event_handler('afterShow', handler)

    def on_before_hide(self, handler: Callable[[bool, Any], Union[bool, None]]) -> None:
        """
        Fires before the Popup is hidden.

        :param handler: The handler function with parameters fromOuterClick (bool), e (Event).
        """
        def event_handler(fromOuterClick, e):
            result = handler(fromOuterClick, e)
            if result is False:
                return js.Boolean(False)
        self.popup.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Any], Union[bool, None]]) -> None:
        """
        Fires before the Popup is shown.

        :param handler: The handler function with parameter node (HTMLElement).
        """
        def event_handler(node):
            result = handler(node)
            if result is False:
                return js.Boolean(False)
        self.popup.events.on('beforeShow', create_proxy(event_handler))

    def on_click(self, handler: Callable[[Any], None]) -> None:
        """
        Fires on clicking the Popup.

        :param handler: The handler function with parameter e (Event).
        """
        self.add_event_handler('click', handler)
