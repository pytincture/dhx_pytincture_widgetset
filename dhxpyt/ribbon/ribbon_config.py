from typing import Any, Dict, List, Optional, Union


class ControlConfig:
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


class BlockConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 items: Optional[List['ControlConfig']] = None,
                 direction: Optional[str] = None,
                 title: Optional[str] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = "block"
        self.id = id
        self.parent = parent
        self.items = items
        self.direction = direction
        self.title = title
        self.css = css
        self.disabled = disabled
        self.hidden = hidden

    def to_dict(self) -> Dict[str, Any]:
        config = {k: v for k, v in self.__dict__.items() if v is not None}
        # Convert items to dicts if they are present
        if self.items:
            config['items'] = [item.to_dict() for item in self.items]
        return config


class ButtonConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 value: Optional[str] = None,
                 items: Optional[List['ControlConfig']] = None,
                 active: Optional[bool] = None,
                 circle: Optional[bool] = None,
                 color: Optional[str] = None,
                 count: Optional[int] = None,
                 countColor: Optional[str] = None,
                 full: Optional[bool] = None,
                 group: Optional[str] = None,
                 hotkey: Optional[str] = None,
                 html: Optional[str] = None,
                 icon: Optional[str] = None,
                 loading: Optional[bool] = None,
                 multiClick: Optional[bool] = None,
                 size: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 twoState: Optional[bool] = None,
                 view: Optional[str] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = "button"
        self.id = id
        self.parent = parent
        self.value = value
        self.items = items
        self.active = active
        self.circle = circle
        self.color = color
        self.count = count
        self.countColor = countColor
        self.full = full
        self.group = group
        self.hotkey = hotkey
        self.html = html
        self.icon = icon
        self.loading = loading
        self.multiClick = multiClick
        self.size = size
        self.tooltip = tooltip
        self.twoState = twoState
        self.view = view
        self.css = css
        self.disabled = disabled
        self.hidden = hidden

    def to_dict(self) -> Dict[str, Any]:
        config = {k: v for k, v in self.__dict__.items() if v is not None}
        if self.items:
            config['items'] = [item.to_dict() for item in self.items]
        return config


class CustomHTMLButtonConfig(ControlConfig):
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


class DatepickerConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 value: Optional[str] = None,
                 valueFormat: Optional[str] = None,
                 dateFormat: Optional[str] = None,
                 disabledDates: Optional[List[Any]] = None,
                 icon: Optional[str] = None,
                 label: Optional[str] = None,
                 mark: Optional[List[Any]] = None,
                 mode: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 thisMonthOnly: Optional[bool] = None,
                 timeFormat: Optional[str] = None,
                 timePicker: Optional[bool] = None,
                 weekNumbers: Optional[bool] = None,
                 weekStart: Optional[int] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 editable: Optional[bool] = None,
                 hidden: Optional[bool] = None,
                 width: Optional[int] = None):
        self.type = "datePicker"
        self.id = id
        self.parent = parent
        self.value = value
        self.valueFormat = valueFormat
        self.dateFormat = dateFormat
        self.disabledDates = disabledDates
        self.icon = icon
        self.label = label
        self.mark = mark
        self.mode = mode
        self.placeholder = placeholder
        self.thisMonthOnly = thisMonthOnly
        self.timeFormat = timeFormat
        self.timePicker = timePicker
        self.weekNumbers = weekNumbers
        self.weekStart = weekStart
        self.css = css
        self.disabled = disabled
        self.editable = editable
        self.hidden = hidden
        self.width = width


class ImageButtonConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 src: str = None,
                 active: Optional[bool] = None,
                 count: Optional[int] = None,
                 countColor: Optional[str] = None,
                 group: Optional[str] = None,
                 hotkey: Optional[str] = None,
                 size: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 twoState: Optional[bool] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = "imageButton"
        self.id = id
        self.parent = parent
        self.src = src
        self.active = active
        self.count = count
        self.countColor = countColor
        self.group = group
        self.hotkey = hotkey
        self.size = size
        self.tooltip = tooltip
        self.twoState = twoState
        self.css = css
        self.disabled = disabled
        self.hidden = hidden


class InputConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 value: Optional[str] = None,
                 icon: Optional[str] = None,
                 label: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 width: Optional[int] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = "input"
        self.id = id
        self.parent = parent
        self.value = value
        self.icon = icon
        self.label = label
        self.placeholder = placeholder
        self.tooltip = tooltip
        self.width = width
        self.css = css
        self.disabled = disabled
        self.hidden = hidden


class NavItemConfig(ControlConfig):
    def __init__(self,
                 type: Optional[str] = "navItem",
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
                 size: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 twoState: Optional[bool] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = type
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
        self.size = size
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


class SelectButtonConfig(ControlConfig):
    def __init__(self,
                 id: Optional[str] = None,
                 parent: Optional[str] = None,
                 value: Optional[str] = None,
                 items: Optional[List['ControlConfig']] = None,
                 count: Optional[int] = None,
                 countColor: Optional[str] = None,
                 icon: Optional[str] = None,
                 size: Optional[str] = None,
                 tooltip: Optional[str] = None,
                 css: Optional[str] = None,
                 disabled: Optional[bool] = None,
                 hidden: Optional[bool] = None):
        self.type = "selectButton"
        self.id = id
        self.parent = parent
        self.value = value
        self.items = items
        self.count = count
        self.countColor = countColor
        self.icon = icon
        self.size = size
        self.tooltip = tooltip
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


class RibbonConfig:
    """
    Configuration class for the Ribbon widget.
    """
    def __init__(self,
                 data: Optional[List[ControlConfig]] = None,
                 css: Optional[str] = None,
                 menuCss: Optional[str] = None):
        """
        Initializes the RibbonConfig.

        :param data: (Optional) List of control configurations to set into Ribbon.
        :param css: (Optional) Adds style classes to Ribbon.
        :param menuCss: (Optional) Adds style classes to all containers of Ribbon controls with nested items.
        """
        self.data = data
        self.css = css
        self.menuCss = menuCss

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the RibbonConfig into a dictionary format.
        """
        data_dicts = [item.to_dict() for item in self.data] if self.data else None
        config_dict = {
            'data': data_dicts,
            'css': self.css,
            'menuCss': self.menuCss
        }
        return {k: v for k, v in config_dict.items() if v is not None}
