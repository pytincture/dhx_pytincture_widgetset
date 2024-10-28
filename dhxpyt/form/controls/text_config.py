from typing import Union, Dict, Any



class TextConfig:
    """
    Configuration class for the Text control.
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
                 width: Union[str, int] = "content",
                 inputType: str = "text",
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None):
        """
        Initializes the TextConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param value: (Optional) The value of the text control.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param width: (Optional) The width of the control.
        :param inputType: (Optional) Type of input: "text", "password", "number".
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message after successful validation.
        :param errorMessage: (Optional) Message after validation error.
        """
        self.type = "text"
        self.name = name
        self.id = id
        self.value = value
        self.css = css
        self.disabled = disabled
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.width = width
        self.inputType = inputType
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
        Converts the TextConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'value': self.value,
            'css': self.css,
            'disabled': self.disabled,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'width': self.width,
            'inputType': self.inputType,
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
