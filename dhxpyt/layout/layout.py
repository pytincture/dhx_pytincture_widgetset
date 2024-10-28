"""
pyTincture layout widget implementation
"""

from typing import Any, Callable, Dict, List, Union, TypeVar
import json
from pyodide.ffi import create_proxy
import js

from ..grid import Grid, GridConfig
from ..toolbar import Toolbar, ToolbarConfig
from ..sidebar import Sidebar, SidebarConfig
from ..form import Form, FormConfig
from ..menu import Menu, MenuConfig
from .layout_config import LayoutConfig, CellConfig
from ..listbox import Listbox, ListboxConfig
from ..calendar import Calendar, CalendarConfig
from ..chart import Chart, ChartConfig
from ..pagination import Pagination, PaginationConfig
from ..ribbon import Ribbon, RibbonConfig
from ..tabbar import Tabbar, TabbarConfig
from ..timepicker import Timepicker, TimepickerConfig
from ..tree import Tree, TreeConfig


TLayout = TypeVar("TLayout", bound="Layout")

class LoadUICaller(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj.load_ui()
        return obj

class Layout(object, metaclass=LoadUICaller):
    layout_config = None
    def __init__(self, config: LayoutConfig = None, mainwindow=False, **kwargs):
        self.parent = kwargs.get("parent", None)
        """Initializes the layout instance."""
        if mainwindow:
            if not config:
                config = LayoutConfig(
                    css="dhx_layout-cell--bordered",
                    type="line",
                    rows=[
                      CellConfig(id="mainwindow_header", width="98vw", height="auto", header=None),
                      CellConfig(id="mainwindow", width="98vw", header=None)
                    ]
                )
            self.layout = js.dhx.Layout.new("maindiv", js.JSON.parse(json.dumps(config.to_dict())))
        elif self.layout_config:
            self.layout = js.dhx.Layout.new(None, js.JSON.parse(json.dumps(self.layout_config.to_dict())))
        else:
            self.layout = js.dhx.Layout.new(None, js.JSON.parse(json.dumps(config.to_dict())))
        self.initialized = False

    """ Placeholder Widgets Adders """

    def load_ui(self, *args, **kwargs):
        """Subclass this to build your UI"""
        pass

    def add_grid(self, id: str = "mainwindow", grid_config: GridConfig = None) -> Grid:
        """Adds a Grid widget into a Layout cell."""
        grid_widget = Grid(config=grid_config)
        self.attach(id, grid_widget.grid)
        if grid_config.data:
            grid_widget.grid.data.removeAll()
            grid_widget.grid.data.parse(js.JSON.parse(json.dumps(grid_config.data)))
        return grid_widget
    
    def add_layout(self, id: str = "mainwindow", layout_config: LayoutConfig = None) -> TLayout:
        """ Adds a Layout into a Layout cell """
        layout_widget = Layout(config=layout_config)
        self.attach(id, layout_widget.layout)
        return layout_widget
    
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
        
    """ Layout API Functions """

    def destructor(self) -> None:
        """Destroys the layout instance."""
        self.layout.destructor()

    def for_each(self, callback: Callable[[Any, int, List[Any]], Any], parent_id: str = None, level: int = None) -> None:
        """Iterates over layout cells, applying the callback function to each."""
        proxy_callback = create_proxy(callback)
        self.layout.forEach(proxy_callback, parent_id, level)

    def get_cell(self, id: str) -> Any:
        """Retrieves a specific layout cell by its ID."""
        return self.layout.getCell(id)

    def progress_hide(self) -> None:
        """Hides the loading progress bar in the layout."""
        self.layout.progressHide()

    def progress_show(self) -> None:
        """Displays the loading progress bar in the layout."""
        self.layout.progressShow()

    def remove_cell(self, id: str) -> None:
        """Removes a specific layout cell by ID."""
        self.layout.removeCell(id)

    def resize(self, id: str) -> None:
        """Manually triggers a resize on a cell."""
        self.layout.resize(id)

    """ Layout API Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.layout.events[event_name] = event_proxy

    def after_add(self, handler: Callable) -> None:
        """Fires after a cell is added."""
        self.add_event_handler('afterAdd', handler)

    def after_collapse(self, handler: Callable) -> None:
        """Fires after a cell is collapsed."""
        self.add_event_handler('afterCollapse', handler)

    def after_expand(self, handler: Callable) -> None:
        """Fires after a cell is expanded."""
        self.add_event_handler('afterExpand', handler)

    def after_hide(self, handler: Callable) -> None:
        """Fires after a cell is hidden."""
        self.add_event_handler('afterHide', handler)

    def after_remove(self, handler: Callable) -> None:
        """Fires after a cell is removed."""
        self.add_event_handler('afterRemove', handler)

    def after_resize_end(self, handler: Callable) -> None:
        """Fires after a cell resize ends."""
        self.add_event_handler('afterResizeEnd', handler)

    def after_show(self, handler: Callable) -> None:
        """Fires after a cell is shown."""
        self.add_event_handler('afterShow', handler)

    def before_add(self, handler: Callable) -> None:
        """Fires before adding a cell, returns false to prevent."""
        self.add_event_handler('beforeAdd', handler)

    def before_collapse(self, handler: Callable) -> None:
        """Fires before collapsing a cell, returns false to prevent."""
        self.add_event_handler('beforeCollapse', handler)

    def before_expand(self, handler: Callable) -> None:
        """Fires before expanding a cell, returns false to prevent."""
        self.add_event_handler('beforeExpand', handler)

    def before_hide(self, handler: Callable) -> None:
        """Fires before hiding a cell, returns false to prevent."""
        self.add_event_handler('beforeHide', handler)

    def before_remove(self, handler: Callable) -> None:
        """Fires before removing a cell, returns false to prevent."""
        self.add_event_handler('beforeRemove', handler)

    def before_resize_start(self, handler: Callable) -> None:
        """Fires before resizing a cell, returns false to prevent."""
        self.add_event_handler('beforeResizeStart', handler)

    def before_show(self, handler: Callable) -> None:
        """Fires before showing a cell, returns false to prevent."""
        self.add_event_handler('beforeShow', handler)

    """ Layout API Properties """

    @property
    def cols(self) -> List[Dict[Any, Any]]:
        """Gets or sets the columns of the layout."""
        return self.layout.cols

    @cols.setter
    def cols(self, value: List[Dict[Any, Any]]) -> None:
        self.layout.cols = value

    @property
    def css(self) -> str:
        """Gets or sets the CSS class for the layout."""
        return self.layout.css

    @css.setter
    def css(self, value: str) -> None:
        self.layout.css = value

    @property
    def rows(self) -> List[Dict[Any, Any]]:
        """Gets or sets the rows of the layout."""
        return self.layout.rows

    @rows.setter
    def rows(self, value: List[Dict[Any, Any]]) -> None:
        self.layout.rows = value

    @property
    def type(self) -> str:
        """Gets or sets the layout type ('line', 'wide', 'space', 'none')."""
        return self.layout.type

    @type.setter
    def type(self, value: str) -> None:
        self.layout.type = value

    """ Cell API Functions """

    def attach(self, id: str, component: Union[str, Any], config: Dict[str, Any] = None) -> Any:
        """Attaches a component or HTML content to a cell."""
        return self.layout.getCell(id).attach(component, js.JSON.parse(json.dumps(config or {})))

    def attach_html(self, id: str, html: str) -> None:
        """Inserts HTML content into a cell."""
        self.layout.getCell(id).attachHTML(html)

    def collapse(self, id: str) -> None:
        """Collapses the specified cell."""
        self.layout.getCell(id).collapse()

    def detach(self, id: str) -> None:
        """Removes an attached component or content from a cell."""
        self.layout.getCell(id).detach()

    def expand(self, id: str) -> None:
        """Expands the collapsed cell."""
        self.layout.getCell(id).expand()

    def get_parent(self, id: str) -> Any:
        """Returns the parent cell of the current cell."""
        return self.layout.getCell(id).getParent()

    def get_widget(self, id: str) -> Any:
        """Returns the attached widget in the layout cell."""
        return self.layout.getCell(id).getWidget()

    def hide(self, id: str) -> None:
        """Hides the specified cell."""
        self.layout.getCell(id).hide()

    def is_visible(self, id: str) -> bool:
        """Checks if the cell is visible."""
        return self.layout.getCell(id).isVisible()

    def paint(self) -> None:
        """Repaints the layout."""
        self.layout.paint()

    def toggle(self, id: str) -> None:
        """Toggles between collapsing and expanding the cell."""
        self.layout.getCell(id).toggle()

    """ Cell API Properties """

    @property
    def align(self) -> str:
        """Gets or sets the alignment of the content inside a cell."""
        return self.layout.align

    @align.setter
    def align(self, value: str) -> None:
        self.layout.align = value

    @property
    def resizable(self) -> bool:
        """Gets or sets whether the cell can be resized."""
        return self.layout.resizable

    @resizable.setter
    def resizable(self, value: bool) -> None:
        self.layout.resizable = value

    # Add other properties similarly...

class MainWindow(Layout):
    def __init__(self) -> None:
        """Initialize the Main Window layout."""
        super().__init__(mainwindow=True)
        self.initialized = True

    def set_theme(self, theme: str) -> None:
        """Sets the layout theme."""
        js.dhx.setTheme(theme)
