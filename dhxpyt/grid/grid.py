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

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Adds an event handler for the specified event."""
        event_proxy = create_proxy(handler)
        self.grid.events.on(event_name, event_proxy)

    # Example event: afterEditEnd
    def on_after_edit_end(self, handler: Callable[[Any, Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires after editing of a cell is ended."""
        def event_handler(value, row, column):
            handler(value, row.to_py(), column.to_py())
        self.grid.events.on('afterEditEnd', create_proxy(event_handler))

    def on_cell_click(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires when a cell is clicked."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self.grid.events.on('cellClick', create_proxy(event_handler))

    def on_cell_dbl_click(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires when a cell is double-clicked."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self.grid.events.on('cellDblClick', create_proxy(event_handler))

    def on_cell_mouse_down(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires before releasing the left mouse button when clicking on a grid cell."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self.grid.events.on('cellMouseDown', create_proxy(event_handler))

    def on_cell_mouse_over(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires on moving the mouse pointer over a grid cell."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self.grid.events.on('cellMouseOver', create_proxy(event_handler))

    def on_cell_right_click(self, handler: Callable[[Dict[str, Any], Dict[str, Any], Any], None]) -> None:
        """Fires on right click on a grid cell."""
        def event_handler(row, column, event):
            handler(row.to_py(), column.to_py(), event)
        self.grid.events.on('cellRightClick', create_proxy(event_handler))


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
