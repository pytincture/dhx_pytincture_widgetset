from typing import Any, Dict, List, Optional, Union


class ControlConfig:
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


class CustomHTMLConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 html: Optional[str] = None,
                 css: Optional[str] = None,
                 hidden: Optional[bool] = None):
        self.type = "customHTML"
        self.id = id
        self.parent = parent
        self.html = html
        self.css = css
        self.hidden = hidden


class MenuItemConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 value: Optional[str] = None,
                 items: Optional[List['ControlConfig']] = None,
                 count: Optional[int] = None,
                 countColor: Optional[str] = None,
                 hotkey: Optional[str] = None,
                 html: Optional[str] = None,
                 icon: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = "menuItem"
        self.id = id
        self.parent = parent
        self.value = value
        self.items = items
        self.count = count
        self.countColor = countColor
        self.hotkey = hotkey
        self.html = html
        self.icon = icon
        self.tooltip = tooltip
        self.css = css
        self.disabled = disabled
        self.hidden = hidden

    def to_dict(self) -> Dict[str, Any]:
        config = {k: v for k, v in self.__dict__.items() if v is not None}
        if self.items:
            config['items'] = [item.to_dict() for item in self.items]
        return config


class NavItemConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 value: Optional[str] = None,
                 items: Optional[List['ControlConfig']] = None,
                 active: Optional[bool] = None,
                 count: Optional[int] = None,
                 countColor: Optional[str] = None,
                 group: Optional[str] = None,
                 hotkey: Optional[str] = None,
                 html: Optional[str] = None,
                 icon: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 twoState: Optional[bool] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = "navItem"
        self.id = id
        self.parent = parent
        self.value = value
        self.items = items
        self.active = active
        self.count = count
        self.countColor = countColor
        self.group = group
        self.hotkey = hotkey
        self.html = html
        self.icon = icon
        self.tooltip = tooltip
        self.twoState = twoState
        self.css = css
        self.disabled = disabled
        self.hidden = hidden

    def to_dict(self) -> Dict[str, Any]:
        config = {k: v for k, v in self.__dict__.items() if v is not None}
        if self.items:
            config['items'] = [item.to_dict() for item in self.items]
        return config


class SeparatorConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None):
        self.type = "separator"
        self.id = id


class SpacerConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None):
        self.type = "spacer"
        self.id = id


class TitleConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 value: Optional[str] = None,
                 html: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = "title"
        self.id = id
        self.parent = parent
        self.value = value
        self.html = html
        self.tooltip = tooltip
        self.css = css
        self.disabled = disabled
        self.hidden = hidden


class SidebarConfig:
    """
    Configuration class for the Sidebar widget.
    """
    def __init__(self,
                 data: Optional[List[ControlConfig]] = None,
                 collapsed: Optional[bool] = None,
                 css: Optional[str] = None,
                 menuCss: Optional[str] = None,
                 minWidth: Union[int, str] = None,
                 width: Union[int, str] = None):
        """
        Initializes the SidebarConfig.

        :param data: (Optional) List of control configurations to set into Sidebar.
        :param collapsed: (Optional) Defines that a sidebar is initialized in the collapsed state.
        :param css: (Optional) Adds style classes to Sidebar.
        :param menuCss: (Optional) Adds style classes to all containers of Sidebar controls with nested items.
        :param minWidth: (Optional) Sets the minimal width of a sidebar in the collapsed state.
        :param width: (Optional) Sets the width of a sidebar.
        """
        self.data = data
        self.collapsed = collapsed
        self.css = css
        self.menuCss = menuCss
        self.minWidth = minWidth
        self.width = width

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the SidebarConfig into a dictionary format.
        """
        data_dicts = [item.to_dict() for item in self.data] if self.data else None
        config_dict = {
            'data': data_dicts,
            'collapsed': self.collapsed,
            'css': self.css,
            'menuCss': self.menuCss,
            'minWidth': self.minWidth,
            'width': self.width
        }
        return {k: v for k, v in config_dict.items() if v is not None}
