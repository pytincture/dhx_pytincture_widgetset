from typing import Union, Dict, Any, Callable

from pyodide.ffi import create_proxy


class TimepickerConfig:
    """
    Configuration class for the TimePicker control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 value: Union[str, int, float, Dict[str, Any], list] = None,
                 css: str = None,
                 disabled: bool = False,
                 editable: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 required: bool = False,
                 validation: Callable[[Any], bool] = None,
                 width: Union[str, int] = "content",
                 controls: bool = False,
                 icon: str = None,
                 placeholder: str = None,
                 timeFormat: int = 24,
                 valueFormat: str = "string",
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None):
        """
        Initializes the TimePickerConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param value: (Optional) The initial value of the TimePicker control.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param editable: (Optional) Allows user to enter the value manually.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param required: (Optional) Whether the control is required.
        :param validation: (Optional) The validation function.
        :param width: (Optional) The width of the control.
        :param controls: (Optional) Whether the timepicker has Close and Save buttons.
        :param icon: (Optional) The CSS class name of an icon.
        :param placeholder: (Optional) A tip for the input.
        :param timeFormat: (Optional) Clock format: 12 or 24.
        :param valueFormat: (Optional) Format of the value in events: "string", "timeObject".
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message after successful validation.
        :param errorMessage: (Optional) Message after validation error.
        """
        self.type = "timepicker"
        self.name = name
        self.id = id
        self.value = value
        self.css = css
        self.disabled = disabled
        self.editable = editable
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.required = required
        self.validation = validation
        self.width = width
        self.controls = controls
        self.icon = icon
        self.placeholder = placeholder
        self.timeFormat = timeFormat
        self.valueFormat = valueFormat
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
        Converts the TimePickerConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'value': self.value,
            'css': self.css,
            'disabled': self.disabled,
            'editable': self.editable,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'required': self.required,
            'validation': self.validation,
            'width': self.width,
            'controls': self.controls,
            'icon': self.icon,
            'placeholder': self.placeholder,
            'timeFormat': self.timeFormat,
            'valueFormat': self.valueFormat,
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
