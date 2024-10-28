from typing import Union, Dict, Any, List



class FieldsetConfig:
    """
    Configuration class for the Fieldset control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 hidden: bool = False,
                 disabled: bool = False,
                 css: str = None,
                 width: Union[str, int] = "content",
                 height: Union[str, int] = "content",
                 padding: Union[str, int] = "5px",
                 label: str = None,
                 labelAlignment: str = "left",
                 rows: List[Any] = None,
                 cols: List[Any] = None,
                 align: str = "start"):
        """
        Initializes the FieldsetConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param disabled: (Optional) Whether the control is disabled.
        :param css: (Optional) Adds style classes to the control.
        :param width: (Optional) The width of the control.
        :param height: (Optional) The height of the control.
        :param padding: (Optional) Sets padding for the content inside the control.
        :param label: (Optional) Specifies a label for the control.
        :param labelAlignment: (Optional) Position of the label.
        :param rows: (Optional) Arranges controls vertically.
        :param cols: (Optional) Arranges controls horizontally.
        :param align: (Optional) Alignment of controls inside the control.
        """
        self.type = "fieldset"
        self.name = name
        self.id = id
        self.hidden = hidden
        self.disabled = disabled
        self.css = css
        self.width = width
        self.height = height
        self.padding = padding
        self.label = label
        self.labelAlignment = labelAlignment
        self.rows = rows
        self.cols = cols
        self.align = align

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the FieldsetConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'hidden': self.hidden,
            'disabled': self.disabled,
            'css': self.css,
            'width': self.width,
            'height': self.height,
            'padding': self.padding,
            'label': self.label,
            'labelAlignment': self.labelAlignment,
            'rows': self.rows,
            'cols': self.cols,
            'align': self.align
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
