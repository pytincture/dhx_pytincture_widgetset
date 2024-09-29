"""
pyTincture Tabbar widget implementation
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .tabbar_config import TabbarConfig

from ..grid import Grid, GridConfig
from ..toolbar import Toolbar, ToolbarConfig
from ..sidebar import Sidebar, SidebarConfig
from ..form import Form, FormConfig
from ..menu import Menu, MenuConfig
#from ..layout import Layout, LayoutConfig, CellConfig
from ..listbox import Listbox, ListboxConfig
from ..calendar import Calendar, CalendarConfig
from ..chart import Chart, ChartConfig
from ..pagination import Pagination, PaginationConfig
from ..ribbon import Ribbon, RibbonConfig
from .tabbar_config import TabbarConfig, TabConfig
from ..timepicker import Timepicker, TimepickerConfig
from ..tree import Tree, TreeConfig



class Tabbar:
    def __init__(self, config: TabbarConfig = None, widget_parent: Any = None):
        """Initializes the Tabbar instance."""
        if config is None:
            config = TabbarConfig()
        config_dict = config.to_dict()
        self.tabbar = js.dhx.Tabbar.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Placeholder Widgets Adders """

    def add_grid(self, id: str = "mainwindow", grid_config: GridConfig = None) -> Grid:
        """Adds a Grid widget into a Layout cell."""
        grid_widget = Grid(config=grid_config)
        self.attach(id, grid_widget.grid)
        if grid_config.data:
            grid_widget.grid.data.parse(js.JSON.parse(json.dumps(grid_config.data)))
        return grid_widget
    
    #def add_layout(self, id: str = "mainwindow", layout_config: LayoutConfig = None) -> TLayout:
    #    """ Adds a Layout into a Layout cell """
    #    layout_widget = Layout(config=layout_config)
    #    self.attach(id, layout_widget.layout)
    #    return layout_widget
    
    def add_menu(self, id: str = "mainwindow_header", menu_config: MenuConfig = None) -> Menu:
        """ Adds a Layout into a Layout cell """
        menu_widget = Menu(config=menu_config)
        self.attach(id, menu_widget.menu)
        return menu_widget

    def add_toolbar(self, id: str = "mainwindow", toolbar_config: ToolbarConfig = None) -> Toolbar:
        """Adds a Toolbar widget into a Layout cell."""
        toolbar_widget = Toolbar(config=toolbar_config)
        self.attach(id, toolbar_widget.toolbar)
        return toolbar_widget

    def add_sidebar(self, id: str, sidebar_config: SidebarConfig = None) -> Sidebar:
        """Adds a Sidebar widget into a Layout cell."""
        sidebar_widget = Sidebar(config=sidebar_config)
        self.attach(id, sidebar_widget.sidebar)
        return sidebar_widget

    def add_form(self, id: str, form_config: FormConfig = None) -> Form:
        """Adds a Form widget into a Layout cell."""
        form_widget = Form(config=form_config)
        self.attach(id, form_widget.form)
        return form_widget
    
    def add_listbox(self, id: str, listbox_config: ListboxConfig = None) -> Any:
        """Adds a Listbox widget into a Layout cell."""
        listbox_widget = Listbox(config=listbox_config)
        self.attach(id, listbox_widget.listbox)
        return listbox_widget
    
    def add_calendar(self, id: str, calendar_config: CalendarConfig = None) -> Any:
        """Adds a Calendar widget into a Layout cell."""
        calendar_widget = Calendar(config=calendar_config)
        self.attach(id, calendar_widget.calendar)
        return calendar_widget
    
    def add_chart(self, id: str, chart_config: ChartConfig = None) -> Any:
        """Adds a Chart widget into a Layout cell."""
        chart_widget = Chart(config=chart_config)
        self.attach(id, chart_widget.chart)
        return chart_widget
    
    def add_pagination(self, id: str, pagination_config: PaginationConfig = None) -> Any:
        """Adds a Pagination widget into a Layout cell."""
        pagination_widget = Pagination(config=pagination_config)
        self.attach(id, pagination_widget.pagination)
        return pagination_widget
    
    def add_ribbon(self, id: str, ribbon_config: RibbonConfig = None) -> Any:
        """Adds a Ribbon widget into a Layout cell."""
        ribbon_widget = Ribbon(config=ribbon_config)
        self.attach(id, ribbon_widget.ribbon)
        return ribbon_widget
    
    def add_tabbar(self, id: str, tabbar_config: TabbarConfig = None) -> Any:
        """Adds a Tabbar widget into a Layout cell."""
        tabbar_widget = Tabbar(config=tabbar_config)
        self.attach(id, tabbar_widget.tabbar)
        return tabbar_widget
    
    def add_timepicker(self, id: str, timepicker_config: TimepickerConfig = None) -> Any:
        """Adds a Timepicker widget into a Layout cell."""
        timepicker_widget = Timepicker(config=timepicker_config)
        self.attach(id, timepicker_widget.timepicker)
        return timepicker_widget
    
    def add_tree(self, id: str, tree_config: TreeConfig = None) -> Any:
        """Adds a Tree widget into a Layout cell."""
        tree_widget = Tree(config=tree_config)
        self.attach(id, tree_widget.tree)
        return tree_widget

    """ Tabbar API Methods """

    def add_tab(self, config: Dict[str, Any], index: int) -> None:
        """Adds a new tab into a tabbar."""
        self.tabbar.addTab(js.JSON.parse(json.dumps(config)), index)

    def destructor(self) -> None:
        """Removes the Tabbar instance and releases occupied resources."""
        self.tabbar.destructor()

    def disable_tab(self, id: str) -> bool:
        """Disables a tab on a page."""
        return self.tabbar.disableTab(id)

    def enable_tab(self, id: str) -> None:
        """Enables a disabled tab."""
        self.tabbar.enableTab(id)

    def get_active(self) -> str:
        """Gets the id of the active tab."""
        return self.tabbar.getActive()

    def get_cell(self, id: str) -> Any:
        """Returns the config object of a cell."""
        return self.tabbar.getCell(id)

    def get_id(self, index: int) -> str:
        """Returns the id of a tab by its index."""
        return self.tabbar.getId(index)

    def get_widget(self) -> Any:
        """Returns the widget attached to Tabbar."""
        return self.tabbar.getWidget()

    def is_disabled(self, id: str) -> bool:
        """Checks whether a tab is disabled."""
        return self.tabbar.isDisabled(id)

    def paint(self) -> None:
        """Repaints the Tabbar on a page."""
        self.tabbar.paint()

    def remove_tab(self, id: str) -> None:
        """Removes a tab from a tabbar."""
        self.tabbar.removeTab(id)

    def set_active(self, id: str) -> None:
        """Sets an active tab."""
        self.tabbar.setActive(id)

    """ Tabbar Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.tabbar.events.on(event_name, event_proxy)

    def on_after_close(self, handler: Callable[[str], None]) -> None:
        """Fires after closing a tab in Tabbar."""
        self.add_event_handler('afterClose', handler)

    def on_before_change(self, handler: Callable[[str, str], Union[bool, None]]) -> None:
        """Fires before changing the active tab."""
        def event_handler(id, prev):
            result = handler(id, prev)
            if result is False:
                return js.Boolean(False)
        event_proxy = create_proxy(event_handler)
        self.tabbar.events.on('beforeChange', event_proxy)

    def on_before_close(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before closing a tab in Tabbar."""
        def event_handler(id):
            result = handler(id)
            if result is False:
                return js.Boolean(False)
        event_proxy = create_proxy(event_handler)
        self.tabbar.events.on('beforeClose', event_proxy)

    def on_change(self, handler: Callable[[str, str], None]) -> None:
        """Fires on changing the active tab."""
        self.add_event_handler('change', handler)

    """ Tabbar Properties """

    @property
    def active_tab(self) -> str:
        """Gets or sets the currently active tab."""
        return self.tabbar.config.activeTab

    @active_tab.setter
    def active_tab(self, value: str) -> None:
        self.tabbar.config.activeTab = value

    @property
    def closable(self) -> Union[bool, List[str]]:
        """Gets or sets the closable property for tabs."""
        return self.tabbar.config.closable

    @closable.setter
    def closable(self, value: Union[bool, List[str]]) -> None:
        self.tabbar.config.closable = value

    @property
    def css(self) -> str:
        """Gets or sets the CSS class(es) applied to Tabbar."""
        return self.tabbar.config.css

    @css.setter
    def css(self, value: str) -> None:
        self.tabbar.config.css = value

    @property
    def disabled(self) -> Union[str, List[str]]:
        """Gets or sets disabled tabs."""
        return self.tabbar.config.disabled

    @disabled.setter
    def disabled(self, value: Union[str, List[str]]) -> None:
        self.tabbar.config.disabled = value

    @property
    def mode(self) -> str:
        """Gets or sets the mode of displaying a tabbar."""
        return self.tabbar.config.mode

    @mode.setter
    def mode(self, value: str) -> None:
        self.tabbar.config.mode = value

    @property
    def no_content(self) -> bool:
        """Gets or sets whether tabs contain any content."""
        return self.tabbar.config.noContent

    @no_content.setter
    def no_content(self, value: bool) -> None:
        self.tabbar.config.noContent = value

    @property
    def tab_align(self) -> str:
        """Gets or sets alignment for tabs."""
        return self.tabbar.config.tabAlign

    @tab_align.setter
    def tab_align(self, value: str) -> None:
        self.tabbar.config.tabAlign = value

    @property
    def tab_auto_height(self) -> bool:
        """Gets or sets whether the height of tabs is automatically adjusted."""
        return self.tabbar.config.tabAutoHeight

    @tab_auto_height.setter
    def tab_auto_height(self, value: bool) -> None:
        self.tabbar.config.tabAutoHeight = value

    @property
    def tab_auto_width(self) -> bool:
        """Gets or sets whether the width of tabs is automatically adjusted."""
        return self.tabbar.config.tabAutoWidth

    @tab_auto_width.setter
    def tab_auto_width(self, value: bool) -> None:
        self.tabbar.config.tabAutoWidth = value

    @property
    def tab_height(self) -> Union[int, str]:
        """Gets or sets the height of a tab."""
        return self.tabbar.config.tabHeight

    @tab_height.setter
    def tab_height(self, value: Union[int, str]) -> None:
        self.tabbar.config.tabHeight = value

    @property
    def tab_width(self) -> Union[int, str]:
        """Gets or sets the width of a tab."""
        return self.tabbar.config.tabWidth

    @tab_width.setter
    def tab_width(self, value: Union[int, str]) -> None:
        self.tabbar.config.tabWidth = value

    @property
    def views(self) -> List[Dict[str, Any]]:
        """Gets or sets the configuration of tabs."""
        return self.tabbar.config.views

    @views.setter
    def views(self, value: List[Dict[str, Any]]) -> None:
        self.tabbar.config.views = value

    """ Tabbar Cell API Functions """

    def attach(self, id: str, component: Union[str, Any], config: Dict[str, Any] = None) -> Any:
        """Attaches a DHTMLX component into a Tabbar cell."""
        return self.tabbar.getCell(id).attach(component, js.JSON.parse(json.dumps(config or {})))

    def attach_html(self, id: str, html: str) -> None:
        """Adds HTML content into a Tabbar cell."""
        self.tabbar.getCell(id).attachHTML(html)

    def get_cell_parent(self, id: str) -> Any:
        """Returns the parent of a cell."""
        return self.tabbar.getCell(id).getParent()

    def get_cell_widget(self, id: str) -> Any:
        """Returns the widget attached to a Tabbar cell."""
        return self.tabbar.getCell(id).getWidget()
