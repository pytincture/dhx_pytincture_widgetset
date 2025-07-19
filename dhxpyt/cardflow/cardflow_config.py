from typing import Any, Dict, List, Union

class CardFlowColumnConfig:
    """
    Configuration class for CardFlow columns.
    Similar to GridColumnConfig, it lets you control properties like width, header text, etc.
    """
    def __init__(self,
                 id: str,
                 header: Union[str, Dict[str, Any]],
                 width: Union[int, str] = "100px",
                 align: str = None,
                 hidden: bool = False,
                 css: str = None,
                 dataType: str= "str",
                 dataFormat: str= "",
                 applyFormat: bool= False):
        """
        Initializes a CardFlow column configuration.
        
        :param id: Unique identifier for the column.
        :param header: Header text or configuration.
        :param width: Column width (e.g., "100px" or 100).
        :param align: Alignment for cell content.
        :param hidden: Whether the column is hidden.
        :param css: Additional CSS classes.
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
            "applyFormat": self.applyFormat
        }
        return {k: v for k, v in config_dict.items() if v is not None}

class CardFlowConfig:
    """
    Configuration class for the CardFlow widget.
    Expected structure:
    {
        "columns": [
            { "id": "name", "header": "Name:" },
            { "id": "vehicle", "header": "Vehicle:" },
            { "id": "status", "header": "Status:" },
            { "id": "promise_time", "header": "Promise Time:" }
        ],
        "editable": True,
        "group": {
            "order": ["animal_type"]
        },
        "groupable": True,
        "data": [ ... ]
    }
    """
    def __init__(self,
                 columns: List[Union[Dict[str, Any], Any]] = None,
                 data: List[Dict[str, Any]] = None,
                 editable: bool = True,
                 group: Dict[str, Any] = None,
                 groupable: bool = True,
                 hideExpandCollapse: bool = False,
                 autoCollapse bool = False,
                 optionItems: List[Dict[str, Any]] = None,
                 sortDisabled: bool = False,
                 sortHeader: str = ""):
        """
        Initializes the CardFlowConfig.
        
        Args:
            columns (List[Union[Dict[str, Any], Any]], optional): 
                List of column configurations. Each column should have at least an "id" and "header".
            data (List[Dict[str, Any]], optional): 
                A list of dictionaries containing the CardFlow data.
            editable (bool, optional): 
                Whether the CardFlow is editable. Defaults to True.
            group (Dict[str, Any], optional): 
                Group configuration (e.g. { "order": ["animal_type"] }). Defaults to an empty dict.
            groupable (bool, optional): 
                Whether grouping functionality is enabled. Defaults to True.
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
        self.optionItems = optionItems


    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the CardFlowConfig into a dictionary format.
        """
        config_dict = {
            "columns": [col.to_dict() if hasattr(col, "to_dict") else col for col in self.columns],
            "editable": self.editable,
            "group": self.group,
            "groupable": self.groupable,
            "hideExpandCollapse": self.hideExpandCollapse,
            "autoCollapse": self.autoCollapse,
            "optionItems": self.optionItems,
            "sortDisabled": self.sortDisabled,
            "sortHeader": self.sortHeader,
            "data": self.data
        }
        # Remove keys with None values
        return {k: v for k, v in config_dict.items() if v is not None}
