from typing import List, Union, Dict, Any, Callable
from pyodide.ffi import create_proxy


class ComboboxConfig:
    """
    Configuration class for Combobox.
    """
    def __init__(self,
                 css: str = None,
                 data: List[Dict[str, Any]] = None,
                 disabled: bool = False,
                 eventHandlers: Dict[str, Dict[str, Callable[[Any, Union[str, int]], Union[bool, None]]]] = None,
                 filter: Callable[[Dict[str, Any], str], bool] = None,
                 helpMessage: str = None,
                 hiddenLabel: bool = False,
                 htmlEnable: bool = True,
                 itemHeight: Union[int, str] = 32,
                 itemsCount: Union[bool, Callable[[int], str]] = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = "auto",
                 listHeight: Union[int, str] = 224,
                 multiselection: bool = False,
                 newOptions: bool = False,
                 placeholder: str = None,
                 readOnly: bool = False,
                 selectAllButton: bool = False,
                 template: Callable[[Any], str] = None,
                 value: Union[str, int, List[Union[str, int]]] = None,
                 virtual: bool = False):
        """
        :param css: (Optional) Adds style classes to Combobox.
        :param data: (Optional) Specifies an array of data objects to set into the combobox.
        :param disabled: (Optional) Makes Combobox disabled.
        :param eventHandlers: (Optional) Adds event handlers to HTML elements of a custom template.
        :param filter: (Optional) Sets a custom function for filtering Combobox options.
        :param helpMessage: (Optional) Adds an icon with a question mark next to the Combo input.
        :param hiddenLabel: (Optional) Adds a hidden label for a Combo box input.
        :param htmlEnable: (Optional) Enables rendering of HTML content in options.
        :param itemHeight: (Optional) Sets the height of an item in the list of options.
        :param itemsCount: (Optional) Shows the total number of selected options.
        :param label: (Optional) Adds a label for Combobox.
        :param labelPosition: (Optional) Defines the position of a label.
        :param labelWidth: (Optional) Sets the width of a label.
        :param listHeight: (Optional) Sets the height of the list of options.
        :param multiselection: (Optional) Enables selection of multiple options.
        :param newOptions: (Optional) Allows users to add new options into the data collection.
        :param placeholder: (Optional) Sets a placeholder in the input of Combobox.
        :param readOnly: (Optional) Makes Combobox read-only.
        :param selectAllButton: (Optional) Defines whether the Select All button should be shown.
        :param template: (Optional) Sets a template for displaying options.
        :param value: (Optional) Specifies the values that will appear in the input on initialization.
        :param virtual: (Optional) Enables dynamic loading of data on scrolling the list of options.
        """
        self.css = css
        self.data = data if data else []
        self.disabled = disabled
        self.eventHandlers = eventHandlers
        self.filter = filter
        self.helpMessage = helpMessage
        self.hiddenLabel = hiddenLabel
        self.htmlEnable = htmlEnable
        self.itemHeight = itemHeight
        self.itemsCount = itemsCount
        self.label = label
        self.labelPosition = labelPosition
        self.labelWidth = labelWidth
        self.listHeight = listHeight
        self.multiselection = multiselection
        self.newOptions = newOptions
        self.placeholder = placeholder
        self.readOnly = readOnly
        self.selectAllButton = selectAllButton
        self.template = template
        self.value = value
        self.virtual = virtual
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ComboboxConfig into a dictionary format that can be
        passed into the combobox constructor.
        """
        config_dict = {
            'css': self.css,
            'data': self.data,
            'disabled': self.disabled,
            'helpMessage': self.helpMessage,
            'hiddenLabel': self.hiddenLabel,
            'htmlEnable': self.htmlEnable,
            'itemHeight': self.itemHeight,
            'itemsCount': self.itemsCount,
            'label': self.label,
            'labelPosition': self.labelPosition,
            'labelWidth': self.labelWidth,
            'listHeight': self.listHeight,
            'multiselection': self.multiselection,
            'newOptions': self.newOptions,
            'placeholder': self.placeholder,
            'readOnly': self.readOnly,
            'selectAllButton': self.selectAllButton,
            'value': self.value,
            'virtual': self.virtual
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}
        
        # Handle eventHandlers separately
        if self.eventHandlers:
            # Convert Python functions to JavaScript proxies
            handlers = {}
            for event_name, classes in self.eventHandlers.items():
                handlers[event_name] = {}
                for class_name, func in classes.items():
                    handlers[event_name][class_name] = create_proxy(func)
            config_dict['eventHandlers'] = handlers
        
        # Handle filter function
        if self.filter:
            config_dict['filter'] = create_proxy(self.filter)
        
        # Handle template function
        if self.template:
            config_dict['template'] = create_proxy(self.template)
        
        return config_dict
