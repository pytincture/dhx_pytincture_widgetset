from typing import Any, Dict, Optional



class PaginationConfig:
    """
    Configuration class for the Pagination widget.
    """
    def __init__(self,
                 data: Any,  # Should be a DataCollection instance from DHTMLX library
                 css: str = None,
                 inputWidth: int = 40,
                 page: int = 0,
                 pageSize: int = 10):
        """
        Initializes the PaginationConfig.

        :param data: (Required) The data collection of a widget to set into the pagination.
        :param css: (Optional) Adds style classes to the pagination.
        :param inputWidth: (Optional) Sets the width for the input of the pagination.
        :param page: (Optional) The index of the initial page set in the pagination.
        :param pageSize: (Optional) The number of items displayed per page of the related widget.
        """
        self.data = data
        self.css = css
        self.inputWidth = inputWidth
        self.page = page
        self.pageSize = pageSize

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the PaginationConfig into a dictionary format.
        """
        config_dict = {
            'data': self.data,
            'css': self.css,
            'inputWidth': self.inputWidth,
            'page': self.page,
            'pageSize': self.pageSize,
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
