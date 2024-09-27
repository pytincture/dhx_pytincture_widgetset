from typing import Union, Dict, Any, List



class ToggleOption:
    """
    Represents an individual toggle option in the ToggleGroup.
    """
    def __init__(self,
                 id: str = None,
                 hidden: bool = False,
                 disabled: bool = False,
                 selected: bool = False,
                 full: bool = False,
                 text: str = None,
                 offText: str = None,
                 icon: str = None,
                 offIcon: str = None,
                 value: Union[str, int, bool] = None):
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

    def to_dict(self) -> Dict[str, Any]:
        option_dict = {
            'id': self.id,
            'hidden': self.hidden,
            'disabled': self.disabled,
            'selected': self.selected,
            'full': self.full,
            'text': self.text,
            'offText': self.offText,
            'icon': self.icon,
            'offIcon': self.offIcon,
            'value': self.value
        }
        # Remove None values
        return {k: v for k, v in option_dict.items() if v is not None}


class ToggleGroupConfig:
    """
    Configuration class for the ToggleGroup control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 hidden: bool = False,
                 disabled: bool = False,
                 full: bool = False,
                 gap: int = 0,
                 multiselection: bool = False,
                 options: List[ToggleOption] = None,
                 value: Dict[str, bool] = None,
                 css: str = None,
                 height: Union[str, int] = "content",
                 width: Union[str, int] = "content",
                 padding: Union[str, int] = None):
        """
        Initializes the ToggleGroupConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param hidden: (Optional) Whether the ToggleGroup is hidden.
        :param disabled: (Optional) Whether the control is disabled.
        :param full: (Optional) Whether the ToggleGroup extends to the specified width.
        :param gap: (Optional) Offset between elements.
        :param multiselection: (Optional) Allows multiple selection.
        :param options: (Required) List of ToggleGroup elements.
        :param value: (Optional) Defines the state of elements on initialization.
        :param css: (Optional) Adds style classes to the control.
        :param height: (Optional) The height of the control.
        :param width: (Optional) The width of the control.
        :param padding: (Optional) Sets padding between the cell and border.
        """
        self.type = "toggleGroup"
        self.name = name
        self.id = id
        self.hidden = hidden
        self.disabled = disabled
        self.full = full
        self.gap = gap
        self.multiselection = multiselection
        self.options = options  # Should be a list of ToggleOption
        self.value = value
        self.css = css
        self.height = height
        self.width = width
        self.padding = padding

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ToggleGroupConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'hidden': self.hidden,
            'disabled': self.disabled,
            'full': self.full,
            'gap': self.gap,
            'multiselection': self.multiselection,
            'options': [option.to_dict() for option in self.options] if self.options else None,
            'value': self.value,
            'css': self.css,
            'height': self.height,
            'width': self.width,
            'padding': self.padding
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
