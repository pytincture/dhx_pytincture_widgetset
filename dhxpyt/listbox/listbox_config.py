from typing import Any, Callable, Dict, Union
from pyodide.ffi import create_proxy


class ListboxConfig:
    """
    Configuration class for the ListBox widget.
    """
    def __init__(self,
                 data: list = None,
                 css: str = None,
                 dragCopy: bool = False,
                 dragMode: str = None,
                 editable: bool = False,
                 eventHandlers: Dict[str, Dict[str, Callable]] = None,
                 height: Union[int, str] = "auto",
                 htmlEnable: bool = True,
                 itemHeight: Union[int, str] = 37,
                 keyNavigation: Union[bool, Callable[[], bool]] = True,
                 multiselection: Union[bool, str] = False,
                 selection: bool = True,
                 template: Callable[[Dict[str, Any]], str] = None,
                 virtual: bool = False):
        """
        Initializes the ListBoxConfig.

        :param data: (Optional) List of data items.
        :param css: (Optional) Adds a CSS class(es) to the component.
        :param dragCopy: (Optional) Defines that an item is copied to a target during drag-n-drop.
        :param dragMode: (Optional) Enables drag-n-drop in ListBox.
        :param editable: (Optional) Enables editing in ListBox.
        :param eventHandlers: (Optional) Adds event handlers to HTML elements of a custom template.
        :param height: (Optional) Sets the height of ListBox.
        :param htmlEnable: (Optional) Enables/disables rendering of HTML content.
        :param itemHeight: (Optional) Sets the height of an item.
        :param keyNavigation: (Optional) Enables/disables navigation by arrow keys.
        :param multiselection: (Optional) Enables multiselection mode.
        :param selection: (Optional) Enables selection of ListBox items.
        :param template: (Optional) Specifies a template for ListBox items.
        :param virtual: (Optional) Enables dynamic rendering of ListBox items.
        """
        self.data = data
        self.css = css
        self.dragCopy = dragCopy
        self.dragMode = dragMode
        self.editable = editable
        self.eventHandlers = eventHandlers
        self.height = height
        self.htmlEnable = htmlEnable
        self.itemHeight = itemHeight
        self.keyNavigation = keyNavigation
        self.multiselection = multiselection
        self.selection = selection
        self.template = template
        self.virtual = virtual

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ListBoxConfig into a dictionary format.
        """
        config_dict = {
            'data': self.data,
            'css': self.css,
            'dragCopy': self.dragCopy,
            'dragMode': self.dragMode,
            'editable': self.editable,
            'eventHandlers': self.eventHandlers,
            'height': self.height,
            'htmlEnable': self.htmlEnable,
            'itemHeight': self.itemHeight,
            'keyNavigation': self.keyNavigation,
            'multiselection': self.multiselection,
            'selection': self.selection,
            'template': self.template,
            'virtual': self.virtual,
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}

        # Handle functions (e.g., template, keyNavigation)
        if 'template' in config_dict and callable(config_dict['template']):
            # Assuming template is a JavaScript function or needs to be converted
            config_dict['template'] = create_proxy(self.template)

        if 'keyNavigation' in config_dict and callable(config_dict['keyNavigation']):
            config_dict['keyNavigation'] = create_proxy(self.keyNavigation)

        return config_dict
