from typing import Union, Dict, Any, Callable, List

from pyodide.ffi import create_proxy


class ComboConfig:
    """
    Configuration class for the Combo control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 data: List[Dict[str, Any]] = None,
                 value: Union[str, int, List[Union[str, int]]] = None,
                 css: str = None,
                 disabled: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 required: bool = False,
                 validation: Callable[[Any], bool] = None,
                 width: Union[str, int] = "content",
                 filter: Callable[[Any], bool] = None,
                 eventHandlers: Dict[str, Callable] = None,
                 itemHeight: int = 32,
                 itemsCount: bool = False,
                 listHeight: int = 224,
                 multiselection: bool = False,
                 newOptions: bool = False,
                 placeholder: str = None,
                 readOnly: bool = False,
                 selectAllButton: bool = False,
                 template: str = None,
                 virtual: bool = False,
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None):
        """
        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param data: (Optional) An array of Combo options.
        :param value: (Optional) The id(s) of options to be selected.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param required: (Optional) Whether the control is required.
        :param validation: (Optional) A callback function for validation.
        :param width: (Optional) The width of the control.
        :param filter: (Optional) Custom function for filtering options.
        :param eventHandlers: (Optional) Event handlers for custom templates.
        :param itemHeight: (Optional) Height of a cell in the options list.
        :param itemsCount: (Optional) Shows the total number of selected options.
        :param listHeight: (Optional) Height of the list of options.
        :param multiselection: (Optional) Enables multiple selection.
        :param newOptions: (Optional) Allows users to add new options.
        :param placeholder: (Optional) Placeholder in the input field.
        :param readOnly: (Optional) Makes Combo readonly.
        :param selectAllButton: (Optional) Shows the Select All button.
        :param template: (Optional) Template for displaying options.
        :param virtual: (Optional) Enables dynamic loading of data.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message after successful validation.
        :param errorMessage: (Optional) Message after validation error.
        """
        self.type = "combo"
        self.name = name
        self.id = id
        self.data = data
        self.value = value
        self.css = css
        self.disabled = disabled
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.required = required
        self.validation = validation
        self.width = width
        self.filter = filter
        self.eventHandlers = eventHandlers
        self.itemHeight = itemHeight
        self.itemsCount = itemsCount
        self.listHeight = listHeight
        self.multiselection = multiselection
        self.newOptions = newOptions
        self.placeholder = placeholder
        self.readOnly = readOnly
        self.selectAllButton = selectAllButton
        self.template = template
        self.virtual = virtual
        self.hiddenLabel = hiddenLabel
        self.label = label
        self.labelPosition = labelPosition
        self.labelWidth = labelWidth
        self.helpMessage = helpMessage
        self.preMessage = preMessage
        self.successMessage = successMessage
        self.errorMessage = errorMessage

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ComboConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'data': self.data,
            'value': self.value,
            'css': self.css,
            'disabled': self.disabled,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'required': self.required,
            'width': self.width,
            'validation': self.validation,
            'filter': self.filter,
            'eventHandlers': self.eventHandlers,
            'itemHeight': self.itemHeight,
            'itemsCount': self.itemsCount,
            'listHeight': self.listHeight,
            'multiselection': self.multiselection,
            'newOptions': self.newOptions,
            'placeholder': self.placeholder,
            'readOnly': self.readOnly,
            'selectAllButton': self.selectAllButton,
            'template': self.template,
            'virtual': self.virtual,
            'hiddenLabel': self.hiddenLabel,
            'label': self.label,
            'labelPosition': self.labelPosition,
            'labelWidth': self.labelWidth,
            'helpMessage': self.helpMessage,
            'preMessage': self.preMessage,
            'successMessage': self.successMessage,
            'errorMessage': self.errorMessage
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}

        # Handle functions
        if 'validation' in config_dict:
            config_dict['validation'] = create_proxy(self.validation)
        if 'filter' in config_dict:
            config_dict['filter'] = create_proxy(self.filter)
        if 'eventHandlers' in config_dict:
            event_handlers = {k: create_proxy(v) for k, v in config_dict['eventHandlers'].items()}
            config_dict['eventHandlers'] = event_handlers

        return config_dict
