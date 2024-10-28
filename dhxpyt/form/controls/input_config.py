from typing import Union, Dict, Any, Callable

from pyodide.ffi import create_proxy


class InputConfig:
    """
    Configuration class for the Input control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 value: Union[str, int] = None,
                 css: str = None,
                 disabled: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 required: bool = False,
                 validation: Union[str, Callable[[Any], bool]] = None,
                 width: Union[str, int] = "content",
                 autocomplete: bool = False,
                 icon: str = None,
                 inputType: str = "input",
                 max: Union[int, None] = None,
                 maxlength: Union[int, None] = None,
                 min: Union[int, None] = None,
                 minlength: Union[int, None] = None,
                 placeholder: str = None,
                 readOnly: bool = False,
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None):
        """
        Initializes the InputConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param value: (Optional) The initial value of the input.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param required: (Optional) Whether the control is required.
        :param validation: (Optional) The validation rule or function.
        :param width: (Optional) The width of the control.
        :param autocomplete: (Optional) Enables autocomplete functionality.
        :param icon: (Optional) The CSS class name of an icon.
        :param inputType: (Optional) Sets the type of input: "text", "password", "number".
        :param max: (Optional) The maximal value allowed in the input (for "number" type).
        :param maxlength: (Optional) The maximum number of characters allowed.
        :param min: (Optional) The minimal value allowed in the input (for "number" type).
        :param minlength: (Optional) The minimum number of characters allowed.
        :param placeholder: (Optional) A tip for the input.
        :param readOnly: (Optional) Whether the input is readonly.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message after successful validation.
        :param errorMessage: (Optional) Message after validation error.
        """
        self.name = name
        self.id = id
        self.value = value
        self.css = css
        self.disabled = disabled
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.required = required
        self.validation = validation
        self.width = width
        self.autocomplete = autocomplete
        self.icon = icon
        self.inputType = inputType
        self.max = max
        self.maxlength = maxlength
        self.min = min
        self.minlength = minlength
        self.placeholder = placeholder
        self.readOnly = readOnly
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
        Converts the InputConfig into a dictionary format.
        """
        config_dict = {
            'name': self.name,
            'id': self.id,
            'value': self.value,
            'css': self.css,
            'disabled': self.disabled,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'required': self.required,
            'validation': self.validation,
            'width': self.width,
            'autocomplete': self.autocomplete,
            'icon': self.icon,
            'type': self.inputType,
            'max': self.max,
            'maxlength': self.maxlength,
            'min': self.min,
            'minlength': self.minlength,
            'placeholder': self.placeholder,
            'readOnly': self.readOnly,
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

        # Handle validation function
        if 'validation' in config_dict and callable(config_dict['validation']):
            config_dict['validation'] = create_proxy(self.validation)
    

        return config_dict
