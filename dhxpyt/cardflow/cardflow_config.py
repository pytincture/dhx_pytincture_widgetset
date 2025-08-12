from typing import Any, Callable, TypeVar, List, Dict, Union

class CardFlowColumnConfig:
    """
    Configuration class for CardFlow columns.
    Similar to GridColumnConfig, lets you control properties like width, header text, etc.
    """
    def __init__(
        self,
        id: str,
        header: Union[str, Dict[str, Any]],
        width: Union[int, str] = "100px",
        align: str = None,
        hidden: bool = False,
        css: str = None,
        dataType: str = "str",
        dataFormat: str = "",
        applyFormat: bool = False,
        coltype: str = ""
    ):
        """
        Initializes a CardFlow column configuration.
        
        :param id: Unique identifier for the column.
        :param header: Header text or a more complex header config.
        :param width: Column width (e.g., "100px" or 100).
        :param align: Alignment for cell content.
        :param hidden: Whether the column is hidden.
        :param css: Additional CSS classes.
        :param dataType: Type of the data (e.g., "str", "int", "time").
        :param dataFormat: Used if dataType is "time" (e.g. "HH:MM AM/PM").
        :param applyFormat: Whether to apply the dataFormat for display.
        """
        self.id = id
        self.header = header
        self.width = width
        self.align = align
        self.hidden = hidden
        self.css = css
        self.dataType = dataType
        self.dataFormat = dataFormat
        self.applyFormat = applyFormat
        self.coltype = coltype

    def to_dict(self) -> Dict[str, Any]:
        config_dict = {
            "id": self.id,
            "header": self.header,
            "width": self.width,
            "align": self.align,
            "hidden": self.hidden,
            "css": self.css,
            "dataType": self.dataType,
            "dataFormat": self.dataFormat,
            "applyFormat": self.applyFormat,
            "type": self.coltype
        }
        # Remove keys that are None so we don't pass unnecessary data to JS
        return {k: v for k, v in config_dict.items() if v is not None}


class CardFlowConfig:
    """
    Configuration class for the CardFlow widget.
    Example structure:
    {
        "columns": [
            { "id": "name", "header": "Name:" },
            { "id": "vehicle", "header": "Vehicle:" },
            { "id": "status", "header": "Status:" },
            { "id": "promise_time", "header": "Promise Time:" }
        ],
        "data": [ ... ],
        "cardHeight": "120px",
        "stacked": True
    }
    """
    def __init__(
        self,
        columns: List[Union[Dict[str, Any], CardFlowColumnConfig]] = None,
        data: List[Dict[str, Any]] = None,
        editable: bool = True,
        group: Dict[str, Any] = None,
        groupable: bool = True,
        hideExpandCollapse: bool = False,
        autoCollapse: bool = False,
        optionItems: List[Dict[str, Any]] = None,
        sortDisabled: bool = False,
        showHeader: bool = True,
        showSort: bool = True,
        sortHeader: str = "",
        showDataHeaders: bool = True,
        showOptions: bool = True,
        fontSize: str = "",
        cardHeight: str = None,  # NEW: pass a string like "120px" (defaults to "auto" in JS)
        stacked: bool = False   # NEW: pass True/False for stacked layout
    ):
        """
        Initializes the CardFlowConfig.

        :param columns: List of column configurations (dict or CardFlowColumnConfig).
        :param data: A list of dictionaries containing the CardFlow data (each representing one card).
        :param editable: Whether the CardFlow is editable.
        :param group: Optional grouping config (not always used).
        :param groupable: Whether grouping is enabled (not always used).
        :param hideExpandCollapse: If set to True, you might hide the expand/collapse UI.
        :param optionItems: Specifies items for the "options" dropdown.
        :param sortDisabled: Disables the sorting toolbar if True.
        :param sortHeader: Label/text to show on the sorting toolbar.
        :param cardHeight: Height (CSS) of each card row, e.g. "100px". Defaults to "auto" in JS if not set.
        :param stacked: If True, card data displays in vertical (stacked) format rather than side-by-side grid.
        """
        self.columns = columns if columns is not None else []
        self.data = data if data is not None else []
        self.editable = editable
        self.group = group if group is not None else {}
        self.groupable = groupable
        self.hideExpandCollapse = hideExpandCollapse
        self.autoCollapse = autoCollapse
        self.sortDisabled = sortDisabled
        self.sortHeader = sortHeader
        self.cardHeight = cardHeight
        self.stacked = stacked
        self.optionItems = optionItems
        self.showHeader = showHeader
        self.showSort = showSort
        self.showDataHeaders = showDataHeaders
        self.fontSize = fontSize
        self.showOptions = showOptions

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the CardFlowConfig into a dictionary format for the JS code.
        """
        config_dict = {
            "columns": [
                col.to_dict() if hasattr(col, "to_dict") else col 
                for col in self.columns
            ],
            "data": self.data,
            "editable": self.editable,
            "group": self.group,
            "groupable": self.groupable,
            "hideExpandCollapse": self.hideExpandCollapse,
            "autoCollapse": self.autoCollapse,
            "optionItems": self.optionItems,
            "sortDisabled": self.sortDisabled,
            "sortHeader": self.sortHeader,
            # new parameters
            "cardHeight": self.cardHeight,
            "stacked": self.stacked,
            "showHeader": self.showHeader,
            "showSort": self.showSort,
            "showDataHeaders": self.showDataHeaders,
            "fontSize": self.fontSize,
            "showOptions": self.showOptions
        }
        # Remove keys with None values
        return {k: v for k, v in config_dict.items() if v is not None}
