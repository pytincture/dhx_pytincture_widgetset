"""
pyTincture ContextMenu widget implementation
"""

from typing import Any, Union
import json
import js

from .menu import Menu
from .menu_config import MenuConfig


class ContextMenu(Menu):
    """A menu positioned at the cursor rather than mounted in a cell.

    dhx exposes `showAt` only on `ContextMenu.prototype`, so a plain `Menu`
    cannot be shown at a point. Everything else -- items, events, enable and
    disable -- is inherited unchanged, because the two widgets share an API.

    Like `Window`, this owns its own DOM and is constructed directly rather
    than through a `Layout`/`Tabbar` `add_*` helper.
    """

    def __init__(self, config: MenuConfig = None, widget_parent: Any = None):
        """Initializes the ContextMenu instance."""
        if config is None:
            config = MenuConfig()
        config_dict = config.to_dict()
        self.menu = js.dhx.ContextMenu.new(
            widget_parent, js.JSON.parse(json.dumps(config_dict))
        )

    def show_at(self, elem: Union[str, Any], show_at: str = "bottom") -> None:
        """Shows the menu at an element, or at a MouseEvent/TouchEvent's cursor.

        `on_cell_right_click` hands back the raw `MouseEvent`, which can be
        passed straight through -- dhx reads the cursor position off it, so no
        coordinate arithmetic is needed here.
        """
        self.menu.showAt(elem, show_at)

    def hide_menu(self) -> None:
        """Hides the context menu."""
        self.menu.hide()
