from typing import List, Union, Dict, Any


class CellConfig:
    """
    Configuration class for individual cells in the Layout.
    Defines properties like header, id, width, height, etc.
    """
    def __init__(self,
                 header: str = None,
                 id: str = None,
                 width: Union[str, int] = None,
                 height: Union[str, int] = None,
                 css: str = None,
                 collapsable: bool = False,
                 hidden: bool = False):
        """
        :param header: (Optional) Header text of the cell.
        :param id: (Optional) Unique identifier for the cell.
        :param width: (Optional) Width of the cell, can be percentage or fixed.
        :param height: (Optional) Height of the cell, can be percentage or fixed.
        :param css: (Optional) CSS class to apply to the cell.
        :param collapsable: (Optional) Whether the cell can be collapsed.
        :param hidden: (Optional) Whether the cell is hidden by default.
        """
        self.header = header
        self.id = id
        self.width = width
        self.height = height
        self.css = css
        self.collapsable = collapsable
        self.hidden = hidden

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the CellConfig into a dictionary format that can be
        passed into the layout constructor.
        """
        return {k: v for k, v in self.__dict__.items() if v is not None}


class LayoutConfig:
    """
    Configuration class for Layout. Contains rows and columns with nested cells.
    """
    def __init__(self,
                 type: str = "line",
                 rows: List[List[CellConfig]] = None,
                 cols: List[List[CellConfig]] = None,
                 css: str = None):
        """
        :param type: (Optional) Type of the layout ("line", "wide", etc.)
        :param rows: (Optional) A list of rows, where each row is a list of CellConfig objects.
        :param cols: (Optional) A list of columns, where each column is a list of CellConfig objects.
        :param css: (Optional) CSS class to apply to the entire layout.
        """
        self.type = type
        self.rows = rows if rows else None
        self.cols = cols if cols else None
        self.css = css

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the LayoutConfig into a dictionary format that can be
        passed into the layout constructor. Handles nested rows and cols.
        """
        config_dict = super().to_dict()

        # Convert rows and columns to dictionaries using nested to_dict calls
        if self.rows:
            config_dict['rows'] = [cell.to_dict() for cell in self.rows]

        if self.cols:
            config_dict['cols'] = [cell.to_dict() for cell in self.cols]

        return config_dict
