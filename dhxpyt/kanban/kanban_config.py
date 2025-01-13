from typing import Any, Dict, List, Union

class KanbanConfig:
    """
    Configuration class for the Kanban widget.
    """
    def __init__(self,
                 columns: List[Dict[str, Any]],
                 cards: List[Dict[str, Any]] = None,
                 dragMode: bool = True,
                 editable: bool = True,
                 multiselection: bool = False,
                 autosize: bool = True,
                 toolbar: Dict[str, Any] = None,
                 cardShape: Dict[str, Any] = None,
                 editorShape: List[Dict[str, Any]] = None,
                 rows: List[Dict[str, Any]] = None,
                 links: List[Dict[str, Any]] = None,
                 rowKey: str = None,
                 currentUser: Union[int, str] = None):
        """
        Initializes the KanbanConfig.

        :param columns: List of column configurations.
        :param cards: List of card configurations.
        :param dragMode: Enables drag-and-drop functionality.
        :param editable: Allows editing of card text.
        :param multiselection: Enables multi-card selection.
        :param autosize: Adjusts the Kanban board to fit its container.
        :param toolbar: Toolbar configuration for the Kanban.
        :param cardShape: Configuration for the shape and properties of cards.
        :param editorShape: Configuration for the Kanban editor.
        :param rows: List of row configurations.
        :param links: List of links between cards.
        :param rowKey: Key used for row-grouping of cards.
        :param currentUser: ID of the current user interacting with the Kanban.
        """
        self.columns = columns
        self.cards = cards
        self.dragMode = dragMode
        self.editable = editable
        self.multiselection = multiselection
        self.autosize = autosize
        self.toolbar = toolbar
        self.cardShape = cardShape
        self.editorShape = editorShape
        self.rows = rows
        self.links = links
        self.rowKey = rowKey
        self.currentUser = currentUser

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the KanbanConfig into a dictionary format.
        """
        config_dict = {
            "columns": self.columns,
            "cards": self.cards,
            "dragMode": self.dragMode,
            "editable": self.editable,
            "multiselection": self.multiselection,
            "autosize": self.autosize,
            "toolbar": self.toolbar,
            "cardShape": self.cardShape,
            "editorShape": self.editorShape,
            "rows": self.rows,
            "links": self.links,
            "rowKey": self.rowKey,
            "currentUser": self.currentUser
        }
        return {k: v for k, v in config_dict.items() if v is not None}
