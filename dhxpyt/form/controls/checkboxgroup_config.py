from typing import Union, Dict, Any, List, Callable
from pyodide.ffi import create_proxy


class CheckboxGroupConfig:
    """
    Configuration class for the CheckboxGroup control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 options: Dict[str, Any] = None,
                 value: Dict[str, Union[str, bool]] = None,
                 css: str = None,
                 disabled: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 required: bool = False,
                 width: Union[str, int] = "content",
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None,
                 validation: Callable[[Any], bool] = None):
        """
        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param options: (Required) An object with options of the CheckboxGroup.
        :param value: (Optional) An object with the initial value of the CheckboxGroup.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param required: (Optional) Whether the control is required.
        :param width: (Optional) The width of the control.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Defines the position of the label.
        :param labelWidth: (Optional) Sets the width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message shown after successful validation.
        :param errorMessage: (Optional) Message shown after validation error.
        :param validation: (Optional) The validation function.
        """
        self.type = "checkboxGroup"
        self.name = name
        self.id = id
        self.options = options or {}
        self.value = value
        self.css = css
        self.disabled = disabled
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.required = required
        self.width = width
        self.hiddenLabel = hiddenLabel
        self.label = label
        self.labelPosition = labelPosition
        self.labelWidth = labelWidth
        self.helpMessage = helpMessage
        self.preMessage = preMessage
        self.successMessage = successMessage
        self.errorMessage = errorMessage
        self.validation = validation

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the CheckboxGroupConfig into a dictionary format.
        """
        def process_option(option):
            if isinstance(option, dict) and 'rows' in option:
                option['rows'] = [process_option(item) for item in option['rows']]
            elif hasattr(option, 'to_dict'):
                return option.to_dict()
            return option

        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'options': process_option(self.options),
            'value': self.value,
            'css': self.css,
            'disabled': self.disabled,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'required': self.required,
            'width': self.width,
            'hiddenLabel': self.hiddenLabel,
            'label': self.label,
            'labelPosition': self.labelPosition,
            'labelWidth': self.labelWidth,
            'helpMessage': self.helpMessage,
            'preMessage': self.preMessage,
            'successMessage': self.successMessage,
            'errorMessage': self.errorMessage,
            'validation': self.validation
        }

        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}

        # Handle functions
        if 'validation' in config_dict:
            config_dict['validation'] = create_proxy(self.validation)

        return config_dict

