from typing import List, Union, Dict, Any


class MenuItemConfig:
    """
    Configuration class for individual items in the Menu.
    """
    def __init__(self,
                 id: Union[str, int] = None,
                 value: str = None,
                 type: str = "menuItem",
                 parent: Union[str, int] = None,
                 items: List['MenuItemConfig'] = None,
                 count: Union[int, str] = None,
                 countColor: str = "danger",
                 hotkey: str = None,
                 html: str = None,
                 icon: str = None,
                 css: str = None,
                 disabled: bool = False,
                 hidden: bool = False):
        """
        :param id: (Optional) The id of the menu item.
        :param value: (Optional) The text value of the menu item.
        :param type: (Optional) The type of control, should be "menuItem".
        :param parent: (Optional) The parent id of the menu item.
        :param items: (Optional) An array of child MenuItemConfig objects.
        :param count: (Optional) A badge with a number.
        :param countColor: (Optional) The color of the badge ("danger", "secondary", "primary", "success").
        :param hotkey: (Optional) The name of a keyboard shortcut for the menu item.
        :param html: (Optional) A string with HTML to insert into the menu item.
        :param icon: (Optional) The name of an icon from the used icon font.
        :param css: (Optional) Adds style classes.
        :param disabled: (Optional) Defines whether an item is disabled.
        :param hidden: (Optional) Defines whether the control is hidden.
        """
        self.id = id
        self.value = value
        self.type = type
        self.parent = parent
        self.items = items if items else []
        self.count = count
        self.countColor = countColor
        self.hotkey = hotkey
        self.html = html
        self.icon = icon
        self.css = css
        self.disabled = disabled
        self.hidden = hidden

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the MenuItemConfig into a dictionary format that can be
        passed into the menu constructor.
        """
        config_dict = {
            'id': self.id,
            'value': self.value,
            'type': self.type,
            'parent': self.parent,
            'items': [item.to_dict() for item in self.items] if self.items else None,
            'count': self.count,
            'countColor': self.countColor,
            'hotkey': self.hotkey,
            'html': self.html,
            'icon': self.icon,
            'css': self.css,
            'disabled': self.disabled,
            'hidden': self.hidden
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}

class MenuConfig:
    """
    Configuration class for Menu.
    """
    def __init__(self,
                 css: str = None,
                 data: List[MenuItemConfig] = None,
                 menuCss: str = None,
                 navigationType: str = "pointer"):
        """
        :param css: (Optional) Adds style classes to Menu.
        :param data: (Optional) Specifies an array of MenuItemConfig objects to set into Menu.
        :param menuCss: (Optional) Adds style classes to all containers of Menu controls with nested items.
        :param navigationType: (Optional) Defines the action that opens menu options ('click' or 'pointer').
        """
        self.css = css
        self.data = data if data else []
        self.menuCss = menuCss
        self.navigationType = navigationType

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the MenuConfig into a dictionary format that can be
        passed into the menu constructor.
        """
        config_dict = {
            'css': self.css,
            'data': [item.to_dict() for item in self.data],
            'menuCss': self.menuCss,
            'navigationType': self.navigationType
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
