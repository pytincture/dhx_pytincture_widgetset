from typing import Any, Dict, List, Optional, Union, Callable


class TreeItemConfig:
    def __init__(self,
                 id: Optional[Union[str, int]] = None,
                 value: Optional[str] = None,
                 opened: Optional[bool] = None,
                 checkbox: Optional[bool] = None,
                 items: Optional[List['TreeItemConfig']] = None,
                 icon: Optional[dict] = None):
        """
        Initializes the configuration for a tree item.

        :param id: The ID of the tree item.
        :param value: The value of the tree item.
        :param opened: Whether the tree item is opened by default.
        :param checkbox: Whether the checkbox is displayed for the tree item.
        :param items: Nested child tree items.
        :param icon: Custom icons for the tree item.
        """
        self.id = id
        self.value = value
        self.opened = opened
        self.checkbox = checkbox
        self.items = items
        self.icon = icon

    def to_dict(self) -> Dict[str, Any]:
        config = {
            "id": self.id,
            "value": self.value,
            "opened": self.opened,
            "checkbox": self.checkbox,
            "items": [item.to_dict() for item in self.items] if self.items else None,
            "icon": self.icon
        }
        return {k: v for k, v in config.items() if v is not None}


class TreeConfig:
    """
    Configuration class for the Tree widget.
    """
    def __init__(self,
                 data: Optional[List[TreeItemConfig]] = None,
                 checkbox: Optional[bool] = None,
                 collapsed: Optional[bool] = None,
                 css: Optional[str] = None,
                 dragCopy: Optional[bool] = None,
                 dragMode: Optional[str] = None,
                 dropBehaviour: Optional[str] = None,
                 editable: Optional[bool] = None,
                 icon: Optional[dict] = None,
                 itemHeight: Optional[Union[int, str]] = None,
                 keyNavigation: Optional[bool] = None,
                 rootId: Optional[Union[str, int]] = None,
                 selection: Optional[bool] = None,
                 template: Optional[Callable[[dict, bool], str]] = None):
        """
        Initializes the configuration for the Tree widget.

        :param data: List of TreeItemConfig to define the tree structure.
        :param checkbox: Whether checkboxes are enabled in the tree.
        :param collapsed: Whether the tree is initialized in the collapsed state.
        :param css: Adds custom style classes to the tree.
        :param dragCopy: Defines if the tree item should be copied during drag-and-drop.
        :param dragMode: Defines drag-and-drop mode ("target", "source", "both").
        :param dropBehaviour: Defines the behavior of dragged items ("child", "sibling", "complex").
        :param editable: Enables inline editing of tree items.
        :param icon: Custom icons for tree items.
        :param itemHeight: Sets the height of tree items.
        :param keyNavigation: Enables key navigation for tree.
        :param rootId: The ID for the root tree element.
        :param selection: Enables selection of tree items.
        :param template: Custom template function for rendering tree items.
        """
        self.data = data
        self.checkbox = checkbox
        self.collapsed = collapsed
        self.css = css
        self.dragCopy = dragCopy
        self.dragMode = dragMode
        self.dropBehaviour = dropBehaviour
        self.editable = editable
        self.icon = icon
        self.itemHeight = itemHeight
        self.keyNavigation = keyNavigation
        self.rootId = rootId
        self.selection = selection
        self.template = template

    def to_dict(self) -> Dict[str, Any]:
        config = {
            "data": [item.to_dict() for item in self.data] if self.data else None,
            "checkbox": self.checkbox,
            "collapsed": self.collapsed,
            "css": self.css,
            "dragCopy": self.dragCopy,
            "dragMode": self.dragMode,
            "dropBehaviour": self.dropBehaviour,
            "editable": self.editable,
            "icon": self.icon,
            "itemHeight": self.itemHeight,
            "keyNavigation": self.keyNavigation,
            "rootId": self.rootId,
            "selection": self.selection,
            "template": self.template
        }
        return {k: v for k, v in config.items() if v is not None}
