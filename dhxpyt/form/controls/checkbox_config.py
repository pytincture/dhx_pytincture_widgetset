from typing import Union, Callable, Any, Dict
from pyodide.ffi import create_proxy


class CheckboxConfig:
    """
    Configuration class for the Checkbox control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 value: str = None,
                 checked: bool = False,
                 text: str = None,
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
        :param value: (Optional) The value of the checkbox.
        :param checked: (Optional) Defines the initial state of the checkbox.
        :param text: (Optional) The text value of the control displayed next to it.
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
        self.type = "checkbox"
        self.name = name
        self.id = id
        self.value = value
        self.checked = checked
        self.text = text
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
        Converts the CheckboxConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'value': self.value,
            'checked': self.checked,
            'text': self.text,
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
