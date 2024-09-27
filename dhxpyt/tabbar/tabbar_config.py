from typing import List, Union, Dict, Any


class TabConfig:
    """
    Configuration class for individual tabs in the Tabbar.
    """
    def __init__(self,
                 id: str,
                 tab: str = None,
                 tabCss: str = None,
                 css: str = None,
                 header: str = None,
                 html: str = None,
                 padding: Union[int, str] = None,
                 tabWidth: Union[int, str] = None,
                 tabHeight: Union[int, str] = None):
        """
        :param id: (Required) The id of the tab.
        :param tab: (Optional) The name of the tab.
        :param tabCss: (Optional) The CSS class used for the tab.
        :param css: (Optional) The CSS class used for the cell.
        :param header: (Optional) The header of the cell.
        :param html: (Optional) HTML content for the tab.
        :param padding: (Optional) The distance between the content and border.
        :param tabWidth: (Optional) The width of the tab.
        :param tabHeight: (Optional) The height of the tab.
        """
        self.id = id
        self.tab = tab
        self.tabCss = tabCss
        self.css = css
        self.header = header
        self.html = html
        self.padding = padding
        self.tabWidth = tabWidth
        self.tabHeight = tabHeight

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the TabConfig into a dictionary format.
        """
        config_dict = {
            'id': self.id,
            'tab': self.tab,
            'tabCss': self.tabCss,
            'css': self.css,
            'header': self.header,
            'html': self.html,
            'padding': self.padding,
            'tabWidth': self.tabWidth,
            'tabHeight': self.tabHeight
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}


class TabbarConfig:
    """
    Configuration class for Tabbar.
    """
    def __init__(self,
                 views: List[TabConfig],
                 activeTab: str = None,
                 closable: Union[bool, List[str]] = None,
                 css: str = None,
                 disabled: Union[str, List[str]] = None,
                 mode: str = None,
                 noContent: bool = None,
                 tabAlign: str = None,
                 tabAutoHeight: bool = None,
                 tabAutoWidth: bool = None,
                 tabHeight: Union[int, str] = None,
                 tabWidth: Union[int, str] = None):
        """
        :param views: (Required) Defines the configuration of tabs.
        :param activeTab: (Optional) Sets the currently active tab.
        :param closable: (Optional) Adds close buttons for tabs.
        :param css: (Optional) The CSS class(es) applied to Tabbar.
        :param disabled: (Optional) Makes a tab or tabs disabled.
        :param mode: (Optional) Specifies the mode of displaying the tabbar.
        :param noContent: (Optional) Defines whether tabs contain any content.
        :param tabAlign: (Optional) Sets alignment for tabs.
        :param tabAutoHeight: (Optional) Adjusts tab height automatically.
        :param tabAutoWidth: (Optional) Adjusts tab width automatically.
        :param tabHeight: (Optional) Sets the height of a tab.
        :param tabWidth: (Optional) Sets the width of a tab.
        """
        self.views = views
        self.activeTab = activeTab
        self.closable = closable
        self.css = css
        self.disabled = disabled
        self.mode = mode
        self.noContent = noContent
        self.tabAlign = tabAlign
        self.tabAutoHeight = tabAutoHeight
        self.tabAutoWidth = tabAutoWidth
        self.tabHeight = tabHeight
        self.tabWidth = tabWidth

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the TabbarConfig into a dictionary format.
        """
        config_dict = {
            'views': [view.to_dict() for view in self.views],
            'activeTab': self.activeTab,
            'closable': self.closable,
            'css': self.css,
            'disabled': self.disabled,
            'mode': self.mode,
            'noContent': self.noContent,
            'tabAlign': self.tabAlign,
            'tabAutoHeight': self.tabAutoHeight,
            'tabAutoWidth': self.tabAutoWidth,
            'tabHeight': self.tabHeight,
            'tabWidth': self.tabWidth
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
