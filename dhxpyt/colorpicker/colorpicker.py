"""
pyTincture Colorpicker widget implementation
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .colorpicker_config import ColorpickerConfig

class Colorpicker:
    def __init__(self, config: ColorpickerConfig = None, widget_parent: Any = None):
        """Initializes the Colorpicker instance."""
        if config is None:
            config = ColorpickerConfig()
        self.colorpicker = js.dhx.Colorpicker.new(widget_parent, js.JSON.parse(json.dumps(config.to_dict())))
    
    """ Colorpicker API Functions """

    def clear(self) -> None:
        """Clears the value set in the colorpicker and removes focus."""
        self.colorpicker.clear()

    def destructor(self) -> None:
        """Releases the occupied resources."""
        self.colorpicker.destructor()

    def get_current_mode(self) -> str:
        """Returns the current mode of displaying Colorpicker ('palette' or 'picker')."""
        return self.colorpicker.getCurrentMode()

    def get_custom_colors(self) -> List[str]:
        """Returns an array of selected custom colors."""
        return list(self.colorpicker.getCustomColors())

    def get_value(self) -> str:
        """Returns the code of a selected color in the Hex format."""
        return self.colorpicker.getValue()

    def paint(self) -> None:
        """Repaints Colorpicker on a page."""
        self.colorpicker.paint()

    def set_current_mode(self, view: str) -> None:
        """Shows Colorpicker either in the 'palette' or 'picker' mode."""
        self.colorpicker.setCurrentMode(view)

    def set_custom_colors(self, custom_colors: List[str]) -> None:
        """Sets custom colors that will be displayed at the bottom of the palette."""
        self.colorpicker.setCustomColors(custom_colors)

    def set_focus(self, value: str) -> None:
        """Sets focus on the specified color value."""
        self.colorpicker.setFocus(value)

    def set_value(self, value: str) -> None:
        """Selects a color in Colorpicker."""
        self.colorpicker.setValue(value)

    """ Colorpicker Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.colorpicker.events.on(event_name, event_proxy)

    def on_apply(self, handler: Callable[[], None]) -> None:
        """Fires on clicking the 'Select' button."""
        self.add_event_handler('apply', handler)

    def on_before_change(self, handler: Callable[[str], Union[bool, None]]) -> None:
        """Fires before changing the selected color in Colorpicker."""
        def event_handler(color):
            result = handler(color)
            if result is False:
                return js.Boolean(False)
            # Do not return anything to allow the change
        event_proxy = create_proxy(event_handler)
        self.colorpicker.events.on('beforeChange', event_proxy)

    def on_cancel_click(self, handler: Callable[[], None]) -> None:
        """Fires on clicking the 'Cancel' button."""
        self.add_event_handler('cancelClick', handler)

    def on_change(self, handler: Callable[[str], None]) -> None:
        """Fires on changing the selected color in Colorpicker."""
        self.add_event_handler('change', handler)

    def on_mode_change(self, handler: Callable[[str], None]) -> None:
        """Fires on changing the mode of the colorpicker."""
        self.add_event_handler('modeChange', handler)

    """ Colorpicker Properties """

    @property
    def css(self) -> str:
        """Gets or sets custom CSS classes for Colorpicker."""
        return self.colorpicker.config.css

    @css.setter
    def css(self, value: str) -> None:
        self.colorpicker.config.css = value

    @property
    def custom_colors(self) -> List[str]:
        """Gets or sets custom colors displayed at the bottom of Colorpicker."""
        return self.colorpicker.config.customColors

    @custom_colors.setter
    def custom_colors(self, value: List[str]) -> None:
        self.colorpicker.config.customColors = value

    @property
    def gray_shades(self) -> bool:
        """Gets or sets whether the gray shades are displayed in the palette."""
        return self.colorpicker.config.grayShades

    @gray_shades.setter
    def gray_shades(self, value: bool) -> None:
        self.colorpicker.config.grayShades = value

    @property
    def mode(self) -> str:
        """Gets or sets the mode of displaying the colorpicker ('palette' or 'picker')."""
        return self.colorpicker.config.mode

    @mode.setter
    def mode(self, value: str) -> None:
        self.colorpicker.config.mode = value

    @property
    def palette(self) -> List[List[str]]:
        """Gets or sets the arrays of colors shown in the colorpicker."""
        return self.colorpicker.config.palette

    @palette.setter
    def palette(self, value: List[List[str]]) -> None:
        self.colorpicker.config.palette = value

    @property
    def palette_only(self) -> bool:
        """Gets or sets whether Colorpicker is shown only in the palette mode."""
        return self.colorpicker.config.paletteOnly

    @palette_only.setter
    def palette_only(self, value: bool) -> None:
        self.colorpicker.config.paletteOnly = value

    @property
    def picker_only(self) -> bool:
        """Gets or sets whether Colorpicker is shown only in the picker mode."""
        return self.colorpicker.config.pickerOnly

    @picker_only.setter
    def picker_only(self, value: bool) -> None:
        self.colorpicker.config.pickerOnly = value

    @property
    def transparency(self) -> bool:
        """Gets or sets whether the transparency scale is displayed in the picker mode."""
        return self.colorpicker.config.transparency

    @transparency.setter
    def transparency(self, value: bool) -> None:
        self.colorpicker.config.transparency = value

    @property
    def width(self) -> Union[str, int]:
        """Gets or sets the width of Colorpicker."""
        return self.colorpicker.config.width

    @width.setter
    def width(self, value: Union[str, int]) -> None:
        self.colorpicker.config.width = value
