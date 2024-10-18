from typing import Any, Callable, Dict, List, Union


class GridColumnConfig:
    """
    Configuration class for Grid columns.
    """
    def __init__(self,
                 id: str,
                 header: List[Dict[str, Any]],
                 type: str = None,
                 width: int = None,
                 align: str = None,
                 adjust: bool = False,
                 hidden: bool = False,
                 sortable: bool = True,
                 resizable: bool = True,
                 tooltip: Union[bool, Dict[str, Any]] = True,
                 css: str = None,
                 htmlEnable: bool = True,
                 editable: bool = False,
                 filter: Dict[str, Any] = None,
                 format: str = None,
                 template: Callable[[Dict[str, Any]], str] = None,
                 editorType: str = None,
                 options: List[Dict[str, Any]] = None):
        """
        Initializes the GridColumnConfig.

        :param id: (Required) The unique ID of the column.
        :param header: (Required) The header configuration for the column.
        :param type: (Optional) The data type of the column (e.g., 'string', 'number', 'date').
        :param width: (Optional) The width of the column.
        :param align: (Optional) The alignment of the column content ('left', 'center', 'right').
        :param adjust: (Optional) Whether to auto-adjust the column width.
        :param hidden: (Optional) Whether the column is hidden.
        :param sortable: (Optional) Whether the column is sortable.
        :param resizable: (Optional) Whether the column is resizable.
        :param tooltip: (Optional) Tooltip configuration for the column.
        :param css: (Optional) CSS classes for the column.
        :param htmlEnable: (Optional) Whether to render HTML content in cells.
        :param editable: (Optional) Whether the column cells are editable.
        :param filter: (Optional) Filter configuration for the column.
        :param format: (Optional) Format string for displaying data.
        :param template: (Optional) Template function for custom cell rendering.
        :param editorType: (Optional) Type of editor for editing cells (e.g., 'input', 'select').
        :param options: (Optional) Options for select editors.
        """
        self.id = id
        self.header = header
        self.type = type
        self.width = width
        self.align = align
        self.adjust = adjust
        self.hidden = hidden
        self.sortable = sortable
        self.resizable = resizable
        self.tooltip = tooltip
        self.css = css
        self.htmlEnable = htmlEnable
        self.editable = editable
        self.filter = filter
        self.format = format
        self.template = template
        self.editorType = editorType
        self.options = options

    def to_dict(self) -> Dict[str, Any]:
        config_dict = {
            'id': self.id,
            'header': self.header,
            'type': self.type,
            'width': self.width,
            'align': self.align,
            'adjust': self.adjust,
            'hidden': self.hidden,
            'sortable': self.sortable,
            'resizable': self.resizable,
            'tooltip': self.tooltip,
            'css': self.css,
            'htmlEnable': self.htmlEnable,
            'editable': self.editable,
            'filter': self.filter,
            'format': self.format,
            'template': self.template,
            'editorType': self.editorType,
            'options': self.options,
        }
        return {k: v for k, v in config_dict.items() if v is not None}


class GridConfig:
    """
    Configuration class for the Grid widget.
    """
    def __init__(self,
                 columns: List[GridColumnConfig],
                 data: List[Dict[str, Any]] = None,
                 adjust: Union[str, bool] = False,
                 autoEmptyRow: bool = False,
                 autoHeight: bool = False,
                 autoWidth: bool = False,
                 bottomSplit: int = None,
                 css: str = None,
                 dragCopy: bool = None,
                 dragItem: str = None,
                 dragMode: str = None,
                 editable: bool = False,
                 eventHandlers: Dict[str, Any] = None,
                 exportStyles: Union[bool, List[str]] = False,
                 footerAutoHeight: bool = False,
                 footerRowHeight: int = 0,
                 footerTooltip: Union[bool, Dict[str, Any]] = True,
                 headerAutoHeight: bool = False,
                 headerRowHeight: int = 40,
                 headerTooltip: Union[bool, Dict[str, Any]] = True,
                 height: Union[int, str] = None,
                 htmlEnable: bool = False,
                 keyNavigation: bool = True,
                 leftSplit: int = None,
                 multiselection: bool = False,
                 resizable: bool = False,
                 rightSplit: int = None,
                 rowCss: Callable[[Dict[str, Any]], str] = None,
                 rowHeight: int = 40,
                 selection: Union[bool, str] = False,
                 sortable: bool = True,
                 spans: List[Dict[str, Any]] = None,
                 tooltip: Union[bool, Dict[str, Any]] = True,
                 topSplit: int = None,
                 width: int = None):
        """
        Initializes the GridConfig.

        :param columns: (Required) List of column configurations.
        :param data: (Optional) List of data objects.
        :param adjust: (Optional) Auto adjust columns.
        :param autoEmptyRow: (Optional) Adds an empty row after the last filled row.
        :param autoHeight: (Optional) Makes long text split into multiple lines.
        :param autoWidth: (Optional) Makes grid's columns fit the size of the grid.
        :param bottomSplit: (Optional) Number of frozen rows from the bottom.
        :param css: (Optional) Adds style classes to Grid.
        :param dragCopy: (Optional) Defines whether a row is copied during drag-n-drop.
        :param dragItem: (Optional) Enables reordering columns or rows by drag and drop.
        :param dragMode: (Optional) Enables drag-n-drop in Grid.
        :param editable: (Optional) Enables editing in Grid columns.
        :param eventHandlers: (Optional) Adds event handlers to HTML elements in the grid.
        :param exportStyles: (Optional) Defines the styles to be sent when exporting.
        :param footerAutoHeight: (Optional) Allows adjusting the footer height.
        :param footerRowHeight: (Optional) Sets the height of rows in the footer.
        :param footerTooltip: (Optional) Controls the footer tooltips.
        :param headerAutoHeight: (Optional) Allows adjusting the header height.
        :param headerRowHeight: (Optional) Sets the height of rows in the header.
        :param headerTooltip: (Optional) Controls the header tooltips.
        :param height: (Optional) Sets the height of the grid.
        :param htmlEnable: (Optional) Specifies the HTML content of Grid columns.
        :param keyNavigation: (Optional) Enables keyboard navigation in Grid.
        :param leftSplit: (Optional) Number of frozen columns from the left.
        :param multiselection: (Optional) Enables multi-row/multi-cell selection.
        :param resizable: (Optional) Defines whether columns can be resized.
        :param rightSplit: (Optional) Number of frozen columns from the right.
        :param rowCss: (Optional) Sets style for a row.
        :param rowHeight: (Optional) Defines the height of a row.
        :param selection: (Optional) Enables selection in the grid.
        :param sortable: (Optional) Defines whether sorting is enabled.
        :param spans: (Optional) Describes the configuration of spans.
        :param tooltip: (Optional) Enables/disables all the tooltips of a column.
        :param topSplit: (Optional) Number of frozen rows from the top.
        :param width: (Optional) Sets the width of the grid.
        """
        self.columns = columns
        self.data = data
        self.adjust = adjust
        self.autoEmptyRow = autoEmptyRow
        self.autoHeight = autoHeight
        self.autoWidth = autoWidth
        self.bottomSplit = bottomSplit
        self.css = css
        self.dragCopy = dragCopy
        self.dragItem = dragItem
        self.dragMode = dragMode
        self.editable = editable
        self.eventHandlers = eventHandlers
        self.exportStyles = exportStyles
        self.footerAutoHeight = footerAutoHeight
        self.footerRowHeight = footerRowHeight
        self.footerTooltip = footerTooltip
        self.headerAutoHeight = headerAutoHeight
        self.headerRowHeight = headerRowHeight
        self.headerTooltip = headerTooltip
        self.height = height
        self.htmlEnable = htmlEnable
        self.keyNavigation = keyNavigation
        self.leftSplit = leftSplit
        self.multiselection = multiselection
        self.resizable = resizable
        self.rightSplit = rightSplit
        self.rowCss = rowCss
        self.rowHeight = rowHeight
        self.selection = selection
        self.sortable = sortable
        self.spans = spans
        self.tooltip = tooltip
        self.topSplit = topSplit
        self.width = width

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the GridConfig into a dictionary format.
        """
        config_dict = {
            'columns': self.columns,
            'data': self.data,
            'adjust': self.adjust,
            'autoEmptyRow': self.autoEmptyRow,
            'autoHeight': self.autoHeight,
            'autoWidth': self.autoWidth,
            'bottomSplit': self.bottomSplit,
            'css': self.css,
            'dragCopy': self.dragCopy,
            'dragItem': self.dragItem,
            'dragMode': self.dragMode,
            'editable': self.editable,
            'eventHandlers': self.eventHandlers,
            'exportStyles': self.exportStyles,
            'footerAutoHeight': self.footerAutoHeight,
            'footerRowHeight': self.footerRowHeight,
            'footerTooltip': self.footerTooltip,
            'headerAutoHeight': self.headerAutoHeight,
            'headerRowHeight': self.headerRowHeight,
            'headerTooltip': self.headerTooltip,
            'height': self.height,
            'htmlEnable': self.htmlEnable,
            'keyNavigation': self.keyNavigation,
            'leftSplit': self.leftSplit,
            'multiselection': self.multiselection,
            'resizable': self.resizable,
            'rightSplit': self.rightSplit,
            'rowCss': self.rowCss,
            'rowHeight': self.rowHeight,
            'selection': self.selection,
            'sortable': self.sortable,
            'spans': self.spans,
            'tooltip': self.tooltip,
            'topSplit': self.topSplit,
            'width': self.width
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}

        if self.columns:
            config_dict['columns'] = [column.to_dict() for column in self.columns]

        # Handle functions (e.g., rowCss)
        if 'rowCss' in config_dict and callable(config_dict['rowCss']):
            # Assuming rowCss is a JavaScript function
            config_dict['rowCss'] = self.rowCss  # This may require further adaptation

        return config_dict

