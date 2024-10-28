from typing import Union, Dict, Any



class ContainerConfig:
    """
    Configuration class for the Container control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 html: str = None,
                 css: str = None,
                 disabled: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 width: Union[str, int] = "content",
                 label: str = None,
                 labelWidth: Union[str, int] = None,
                 labelPosition: str = "top",
                 hiddenLabel: bool = False,
                 helpMessage: str = None):
        """
        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param html: (Optional) The HTML content of the control.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param width: (Optional) The width of the control.
        :param label: (Optional) Specifies a label for the control.
        :param labelWidth: (Optional) Width of the label.
        :param labelPosition: (Optional) Position of the label.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param helpMessage: (Optional) Adds a help message to the control.
        """
        self.type = "container"
        self.name = name
        self.id = id
        self.html = html
        self.css = css
        self.disabled = disabled
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.width = width
        self.label = label
        self.labelWidth = labelWidth
        self.labelPosition = labelPosition
        self.hiddenLabel = hiddenLabel
        self.helpMessage = helpMessage

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ContainerConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'html': self.html,
            'css': self.css,
            'disabled': self.disabled,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'width': self.width,
            'label': self.label,
            'labelWidth': self.labelWidth,
            'labelPosition': self.labelPosition,
            'hiddenLabel': self.hiddenLabel,
            'helpMessage': self.helpMessage
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
