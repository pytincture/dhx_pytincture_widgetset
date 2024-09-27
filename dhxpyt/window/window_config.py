from typing import Any, Dict, Optional, Union


class WindowConfig:
    """
    Configuration class for the Window widget.
    """
    def __init__(self,
                 closable: Optional[bool] = False,
                 css: Optional[str] = None,
                 footer: Optional[bool] = None,
                 header: Optional[bool] = None,
                 height: Optional[Union[int, str]] = "50%",
                 html: Optional[str] = None,
                 left: Optional[int] = None,
                 minHeight: Optional[int] = 100,
                 minWidth: Optional[int] = 100,
                 modal: Optional[bool] = False,
                 movable: Optional[bool] = False,
                 node: Optional[Union[Any, str]] = None,
                 resizable: Optional[bool] = False,
                 title: Optional[str] = None,
                 top: Optional[int] = None,
                 viewportOverflow: Optional[bool] = False,
                 width: Optional[Union[int, str]] = "50%"):
        """
        Initializes the WindowConfig.

        :param closable: Defines whether a window can be closed.
        :param css: Adds style classes for the window.
        :param footer: Adds a footer to the window.
        :param header: Adds a header to the window.
        :param height: Sets the height of the window.
        :param html: Sets an HTML content into a window on initialization.
        :param left: The left coordinate of a window position.
        :param minHeight: Sets the minimal height of a window.
        :param minWidth: Sets the minimal width of a window.
        :param modal: Defines whether a window is modal.
        :param movable: Defines whether a window is movable.
        :param node: The container for a window or its ID.
        :param resizable: Defines whether a window can be resized.
        :param title: Adds some text into the header of a window.
        :param top: The top coordinate of a window position.
        :param viewportOverflow: Defines whether a window can go beyond borders of the browser.
        :param width: Sets the width of the window.
        """
        self.closable = closable
        self.css = css
        self.footer = footer
        self.header = header
        self.height = height
        self.html = html
        self.left = left
        self.minHeight = minHeight
        self.minWidth = minWidth
        self.modal = modal
        self.movable = movable
        self.node = node
        self.resizable = resizable
        self.title = title
        self.top = top
        self.viewportOverflow = viewportOverflow
        self.width = width

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the WindowConfig into a dictionary format.
        """
        config_dict = {
            'closable': self.closable,
            'css': self.css,
            'footer': self.footer,
            'header': self.header,
            'height': self.height,
            'html': self.html,
            'left': self.left,
            'minHeight': self.minHeight,
            'minWidth': self.minWidth,
            'modal': self.modal,
            'movable': self.movable,
            'node': self.node,
            'resizable': self.resizable,
            'title': self.title,
            'top': self.top,
            'viewportOverflow': self.viewportOverflow,
            'width': self.width
        }
        return {k: v for k, v in config_dict.items() if v is not None}
