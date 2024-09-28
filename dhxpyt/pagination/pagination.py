"""
Pagination widget implementation
"""

from typing import Any, Callable
import json
from pyodide.ffi import create_proxy
import js

from .pagination_config import PaginationConfig


class Pagination:
    def __init__(self, config: PaginationConfig = None, widget_parent: str = None):
        """
        Initializes the Pagination widget.

        :param config: (Required) The PaginationConfig object containing the pagination configuration.
        :param widget_parent: (Optional) The ID of the HTML element where the pagination will be attached.
        """
        if config is None:
            raise ValueError("PaginationConfig is required for initializing Pagination widget.")
        config_dict = config.to_dict()
        # Assuming that `config.data` is a DHTMLX DataCollection instance
        # We need to handle data initialization appropriately
        # For now, we will pass the data collection directly

        # Create the Pagination instance
        self.pagination = js.dhx.Pagination.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Pagination API Functions """

    def destructor(self) -> None:
        """Destroys the Pagination instance and releases resources."""
        self.pagination.destructor()

    def get_page(self) -> int:
        """Returns the index of the active page."""
        return self.pagination.getPage()

    def get_pages_count(self) -> int:
        """Gets the total number of pages in the pagination."""
        return self.pagination.getPagesCount()

    def get_page_size(self) -> int:
        """Returns the number of items displayed per page."""
        return self.pagination.getPageSize()

    def set_page(self, page: int) -> None:
        """Sets an active page in the related widget."""
        self.pagination.setPage(page)

    def set_page_size(self, size: int) -> None:
        """Sets the number of items displayed on a page."""
        self.pagination.setPageSize(size)

    """ Pagination Event Handlers """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Adds an event handler for the specified event."""
        event_proxy = create_proxy(handler)
        self.pagination.events.on(event_name, event_proxy)

    def on_change(self, handler: Callable[[int, int], None]) -> None:
        """Fires on changing the active page."""
        def event_handler(index, previousIndex):
            handler(index, previousIndex)
        self.pagination.events.on('change', create_proxy(event_handler))
