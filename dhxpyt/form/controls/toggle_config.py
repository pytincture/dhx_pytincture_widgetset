from typing import Union, Dict, Any



class ToggleConfig:
    """
    Configuration class for the Toggle control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 hidden: bool = False,
                 disabled: bool = False,
                 selected: bool = False,
                 full: bool = False,
                 text: str = None,
                 offText: str = None,
                 icon: str = None,
                 offIcon: str = None,
                 value: Union[str, int, bool] = None,
                 css: str = None,
                 height: Union[str, int] = "content",
                 width: Union[str, int] = "content",
                 padding: Union[str, int] = None):
        """
        Initializes the ToggleConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param hidden: (Optional) Whether the toggle is hidden.
        :param disabled: (Optional) Whether the control is disabled.
        :param selected: (Optional) Initial state of the toggle as selected.
        :param full: (Optional) Whether the toggle extends to the specified width.
        :param text: (Optional) Text inside the toggle.
        :param offText: (Optional) Text when the toggle is unselected.
        :param icon: (Optional) CSS class of the icon in the toggle.
        :param offIcon: (Optional) CSS class of the icon when unselected.
        :param value: (Optional) Value in the selected state.
        :param css: (Optional) Adds style classes to the control.
        :param height: (Optional) The height of the control.
        :param width: (Optional) The width of the control.
        :param padding: (Optional) Sets padding between the cell and border.
        """
        self.type = "toggle"
        self.name = name
        self.id = id
        self.hidden = hidden
        self.disabled = disabled
        self.selected = selected
        self.full = full
        self.text = text
        self.offText = offText
        self.icon = icon
        self.offIcon = offIcon
        self.value = value
        self.css = css
        self.height = height
        self.width = width
        self.padding = padding

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ToggleConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'hidden': self.hidden,
            'disabled': self.disabled,
            'selected': self.selected,
            'full': self.full,
            'text': self.text,
            'offText': self.offText,
            'icon': self.icon,
            'offIcon': self.offIcon,
            'value': self.value,
            'css': self.css,
            'height': self.height,
            'width': self.width,
            'padding': self.padding
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
