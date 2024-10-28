from typing import Union, Dict, Any, List



class RadioButtonOption:
    """
    Represents an individual radio button option in the RadioGroup.
    """
    def __init__(self,
                 id: str = None,
                 value: str = None,
                 checked: bool = False,
                 disabled: bool = False,
                 css: str = None,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 text: str = None,
                 width: Union[str, int] = "content"):
        self.type = "radioButton"
        self.id = id
        self.value = value
        self.checked = checked
        self.disabled = disabled
        self.css = css
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.text = text
        self.width = width

    def to_dict(self) -> Dict[str, Any]:
        option_dict = {
            'type': self.type,
            'id': self.id,
            'value': self.value,
            'checked': self.checked,
            'disabled': self.disabled,
            'css': self.css,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'text': self.text,
            'width': self.width
        }
        # Remove None values
        return {k: v for k, v in option_dict.items() if v is not None}


class RadioGroupConfig:
    """
    Configuration class for the RadioGroup control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 options: List[RadioButtonOption] = None,
                 value: str = None,
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
                 errorMessage: str = None):
        """
        Initializes the RadioGroupConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param options: (Required) An object with options of a RadioGroup.
        :param value: (Optional) The initial value of the RadioGroup.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param required: (Optional) Whether the control is required.
        :param width: (Optional) The width of the control.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message after successful validation.
        :param errorMessage: (Optional) Message after validation error.
        """
        self.type = "radioGroup"
        self.name = name
        self.id = id
        self.options = options  # Should be a list of RadioButtonOption
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

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the RadioGroupConfig into a dictionary format.
        """
        def process_option(option):
            if hasattr(option, 'to_dict'):
                return option.to_dict()
            return option

        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'options': self.options,
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
            'errorMessage': self.errorMessage
        }

        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
