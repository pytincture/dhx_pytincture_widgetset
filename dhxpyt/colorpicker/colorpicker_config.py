from typing import List, Union, Dict, Any


class ColorpickerConfig:
    """
    Configuration class for Colorpicker. Contains properties to customize the colorpicker.
    """
    def __init__(self,
                 css: str = None,
                 customColors: List[str] = None,
                 grayShades: bool = True,
                 mode: str = "palette",
                 palette: List[List[str]] = None,
                 paletteOnly: bool = False,
                 pickerOnly: bool = False,
                 transparency: bool = True,
                 width: Union[str, int] = "238px"):
        """
        :param css: (Optional) Adds custom CSS classes to Colorpicker.
        :param customColors: (Optional) Shows custom colors at the bottom of Colorpicker.
        :param grayShades: (Optional) Displays the section with gray shades in the palette.
        :param mode: (Optional) Specifies the mode of displaying the colorpicker ("palette" or "picker").
        :param palette: (Optional) Arrays of colors to show in the colorpicker.
        :param paletteOnly: (Optional) Shows Colorpicker only in the palette mode.
        :param pickerOnly: (Optional) Shows Colorpicker only in the picker mode.
        :param transparency: (Optional) Displays the transparency scale in the picker mode.
        :param width: (Optional) Sets the width of Colorpicker.
        """
        self.css = css
        self.customColors = customColors
        self.grayShades = grayShades
        self.mode = mode
        self.palette = palette
        self.paletteOnly = paletteOnly
        self.pickerOnly = pickerOnly
        self.transparency = transparency
        self.width = width

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ColorpickerConfig into a dictionary format that can be
        passed into the colorpicker constructor.
        """
        config_dict = {
            'css': self.css,
            'customColors': self.customColors,
            'grayShades': self.grayShades,
            'mode': self.mode,
            'palette': self.palette,
            'paletteOnly': self.paletteOnly,
            'pickerOnly': self.pickerOnly,
            'transparency': self.transparency,
            'width': self.width
        }
        # Remove None values to avoid passing undefined properties
        return {k: v for k, v in config_dict.items() if v is not None}
