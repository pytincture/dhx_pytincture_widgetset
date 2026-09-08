"""
Grid widget implementation
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .grid_config import GridConfig


class Grid:
    def __init__(self, config: GridConfig = None, widget_parent: str = None):
        """
        Initializes the Grid widget.

        :param config: (Optional) The GridConfig object containing the grid configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the grid will be attached.
        """
        if config is None:
            config = GridConfig()
        config_dict = config.to_dict()
        self._event_proxies: Dict[str, List[Any]] = {}
        self.grid = js.dhx.Grid.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Grid API Functions """

    def add_cell_css(self, row_id: Union[str, int], col_id: Union[str, int], css: str) -> None:
        """Adds a CSS class to a cell."""
        self.grid.addCellCss(row_id, col_id, css)

    def add_row_css(self, row_id: Union[str, int], css: str) -> None:
        """Adds a CSS class to a row."""
        self.grid.addRowCss(row_id, css)

    def add_span(self, span_obj: Dict[str, Any]) -> None:
        """Adds a span to the grid."""
        self.grid.addSpan(js.JSON.parse(json.dumps(span_obj)))

    def adjust_column_width(self, col_id: Union[str, int], adjust: Union[str, bool] = None) -> None:
        """Adjusts the width of a column."""
        self.grid.adjustColumnWidth(col_id, adjust)

    def destructor(self) -> None:
        """Destroys the grid instance and releases resources."""
        self.grid.destructor()

    def edit_cell(self, row_id: Union[str, int], col_id: Union[str, int], editor_type: str = None) -> None:
        """Enables editing of a grid cell."""
        self.grid.editCell(row_id, col_id, editor_type)

    def edit_end(self, without_save: bool = False) -> None:
        """Finishes editing in a cell."""
        self.grid.editEnd(without_save)

    def get_cell_rect(self, row_id: Union[str, int], col_id: Union[str, int]) -> Dict[str, Any]:
        """Returns the parameters of a cell."""
        rect = self.grid.getCellRect(row_id, col_id)
        return rect.to_py()

    def get_column(self, col_id: Union[str, int]) -> Dict[str, Any]:
        """Returns an object with attributes of a column."""
        column = self.grid.getColumn(col_id)
        return column.to_py()

    def get_header_filter(self, col_id: Union[str, int]) -> Any:
        """Returns an object with methods for the header filter of the specified column."""
        return self.grid.getHeaderFilter(col_id)

    def get_scroll_state(self) -> Dict[str, int]:
        """Returns the coordinates of the scroll position."""
        state = self.grid.getScrollState()
        return state.to_py()

    def get_sorting_state(self) -> Dict[str, Any]:
        """Returns the current state of sorting data in the grid."""
        state = self.grid.getSortingState()
        return state.to_py()

    def get_span(self, row_id: Union[str, int], col_id: Union[str, int]) -> Dict[str, Any]:
        """Returns an object with spans."""
        span = self.grid.getSpan(row_id, col_id)
        return span.to_py()

    def hide_column(self, col_id: Union[str, int]) -> None:
        """Hides a column of the grid."""
        self.grid.hideColumn(col_id)

    def hide_row(self, row_id: Union[str, int]) -> None:
        """Hides a row of the grid."""
        self.grid.hideRow(row_id)

    def is_column_hidden(self, col_id: Union[str, int]) -> bool:
        """Checks whether a column is hidden."""
        return self.grid.isColumnHidden(col_id)

    def is_row_hidden(self, row_id: Union[str, int]) -> bool:
        """Checks whether a row is hidden."""
        return self.grid.isRowHidden(row_id)

    def paint(self) -> None:
        """Repaints the grid on the page."""
        self.grid.paint()

    def remove_cell_css(self, row_id: Union[str, int], col_id: Union[str, int], css: str) -> None:
        """Removes a CSS class from a cell."""
        self.grid.removeCellCss(row_id, col_id, css)

    def remove_row_css(self, row_id: Union[str, int], css: str) -> None:
        """Removes a CSS class from a row."""
        self.grid.removeRowCss(row_id, css)

    def remove_span(self, row_id: Union[str, int], col_id: Union[str, int]) -> None:
        """Removes a span from the grid."""
        self.grid.removeSpan(row_id, col_id)

    def scroll(self, x: int = None, y: int = None) -> None:
        """Scrolls the grid to the specified coordinates."""
        self.grid.scroll(x, y)

    def scroll_to(self, row_id: Union[str, int], col_id: Union[str, int]) -> None:
        """Scrolls the grid to a specified cell."""
        self.grid.scrollTo(row_id, col_id)

    def set_columns(self, columns: List[Dict[str, Any]]) -> None:
        """Sets configuration for grid columns."""
        self.grid.setColumns(js.JSON.parse(json.dumps(columns)))

    def show_column(self, col_id: Union[str, int]) -> None:
        """Shows a hidden column."""
        self.grid.showColumn(col_id)

    def show_row(self, row_id: Union[str, int]) -> None:
        """Shows a hidden row."""
        self.grid.showRow(row_id)

    """ Grid Event Handlers """

    def _bind(self, event_name: str, handler: Callable) -> Any:
        """Registers a handler and retains its proxy so destroy() can free it.

        `create_proxy` objects are owned by Python; dropping the reference
        without destroying it leaks the handler across navigation, which is
        what `destroy()` exists to prevent.
        """
        event_proxy = create_proxy(handler)
        self._event_proxies.setdefault(event_name, []).append(event_proxy)
        self.grid.events.on(event_name, event_proxy)
        return event_proxy

    def destroy(self) -> None:
        """Destroys the grid and releases every retained event proxy."""
        try:
            if hasattr(self.grid, "destructor"):
                self.grid.destructor()
        finally:
            for proxies in self._event_proxies.values():
                for proxy in proxies:
                    try:
                        proxy.destroy()
                    except Exception:
                        pass
            self._event_proxies.clear()

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Adds an event handler for the specified event."""
        self._bind(event_name, handler)

    # Example event: afterEditEnd
    def on_after_edit_end(self, handler: Callable[[Any, Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires after editing of a cell is ended."""
        def event_handler(value, row, column):
            handler(value, row.to_py(), column.to_py())
        self._bind('afterEditEnd', event_handler)

    def on_cell_click(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires when a cell is clicked."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self._bind('cellClick', event_handler)

    def on_cell_dbl_click(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires when a cell is double-clicked."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self._bind('cellDblClick', event_handler)

    def on_cell_mouse_down(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires before releasing the left mouse button when clicking on a grid cell."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self._bind('cellMouseDown', event_handler)

    def on_cell_mouse_over(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires on moving the mouse pointer over a grid cell."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self._bind('cellMouseOver', event_handler)

    def on_cell_right_click(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires on right click on a grid cell."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self._bind('cellRightClick', event_handler)

    """ Grid Drag-and-Drop Event Handlers """

    def on_before_row_drag(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires before dragging a row starts."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('beforeRowDrag', event_handler)

    def on_after_row_drag(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires after dragging a row finishes."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('afterRowDrag', event_handler)

    def on_before_column_drag(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires before dragging a column starts."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('beforeColumnDrag', event_handler)

    def on_after_column_drag(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires after dragging a column finishes."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('afterColumnDrag', event_handler)

    def on_row_drop(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when a row is dropped."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('afterRowDrop', event_handler)

    def on_column_drop(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when a column is dropped."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('afterColumnDrop', event_handler)

    # Dragging callbacks
    def on_drag_row_in(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when a row is dragged over a potential target."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('dragRowIn', event_handler)

    def on_drag_row_out(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when a row is dragged out of a potential target."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('dragRowOut', event_handler)

    def on_drag_column_in(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when a column is dragged over a potential target."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('dragColumnIn', event_handler)

    def on_drag_column_out(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when a column is dragged out of a potential target."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('dragColumnOut', event_handler)

    def on_drag_row_start(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when the dragging of a row starts."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('dragRowStart', event_handler)

    def on_drag_column_start(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when the dragging of a column starts."""
        def event_handler(data, event):
            handler(data.to_py(), event)
        self._bind('dragColumnStart', event_handler)

    # Similarly, other events can be added following the documentation provided.

    """ Grid Selection Functions """

    def select_cell(self, row: Union[Dict[str, Any], str, int] = None, column: Union[Dict[str, Any], str, int] = None,
                    ctrl_up: bool = False, shift_up: bool = False) -> None:
        """Sets selection to specified cells."""
        self.grid.selection.setCell(row, column, ctrl_up, shift_up)

    def get_selected_cells(self) -> List[Dict[str, Any]]:
        """Returns an array with config objects of selected cells."""
        cells = self.grid.selection.getCells()
        return [cell.to_py() for cell in cells]

    def unselect_cell(self, row_id: Union[str, int] = None, col_id: Union[str, int] = None) -> None:
        """Unselects previously selected cells."""
        self.grid.selection.removeCell(row_id, col_id)

    """ Grid Export Functions """

    def export_to_csv(self, config: Dict[str, Any] = None) -> str:
        """Exports data from the grid into a CSV string or file."""
        if config is None:
            config = {}
        result = self.grid.csv(js.JSON.parse(json.dumps(config)))
        return result

    def export_to_pdf(self, config: Dict[str, Any] = None) -> None:
        """Exports data from the grid to a PDF file."""
        if config is None:
            config = {}
        self.grid.pdf(js.JSON.parse(json.dumps(config)))

    def export_to_png(self, config: Dict[str, Any] = None) -> None:
        """Exports data from the grid to a PNG file."""
        if config is None:
            config = {}
        self.grid.png(js.JSON.parse(json.dumps(config)))

    def export_to_xlsx(self, config: Dict[str, Any] = None) -> None:
        """Exports data from the grid to an Excel file."""
        if config is None:
            config = {}
        self.grid.xlsx(js.JSON.parse(json.dumps(config)))
