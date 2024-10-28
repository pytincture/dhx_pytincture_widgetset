from typing import Union, Dict, Any



class SpacerConfig:
    """
    Configuration class for the Spacer control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 css: str = None,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 width: Union[str, int] = "content"):
        """
        Initializes the SpacerConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param css: (Optional) Adds style classes to the control.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param width: (Optional) The width of the control.
        """
        self.type = "spacer"
        self.name = name
        self.id = id
        self.css = css
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.width = width

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the SpacerConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'css': self.css,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'width': self.width
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
