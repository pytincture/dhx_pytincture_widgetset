from typing import Union, Dict, Any, Callable

from pyodide.ffi import create_proxy


class ColorpickerConfig:
    """
    Configuration class for the ColorPicker control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 value: str = None,
                 css: str = None,
                 disabled: bool = False,
                 editable: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 required: bool = False,
                 validation: Callable[[Any], bool] = None,
                 width: Union[str, int] = "content",
                 customColors: bool = False,
                 grayShades: bool = True,
                 icon: str = None,
                 mode: str = "palette",
                 palette: Any = None,
                 paletteOnly: bool = False,
                 pickerOnly: bool = False,
                 placeholder: str = None,
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None):
        """
        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param value: (Optional) The value of the colorpicker.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param editable: (Optional) Allows user to enter the value manually.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param required: (Optional) Whether the control is required.
        :param validation: (Optional) The validation function.
        :param width: (Optional) The width of the control.
        :param customColors: (Optional) Shows a section with custom colors.
        :param grayShades: (Optional) Displays gray shades in the palette.
        :param icon: (Optional) The CSS class name of an icon.
        :param mode: (Optional) The mode of the control ("palette", "picker").
        :param palette: (Optional) Arrays of colors to be shown in the colorpicker.
        :param paletteOnly: (Optional) Shows only the palette mode.
        :param pickerOnly: (Optional) Shows only the picker mode.
        :param placeholder: (Optional) A tip for the input.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message after successful validation.
        :param errorMessage: (Optional) Message after validation error.
        """
        self.type = "colorpicker"
        self.name = name
        self.id = id
        self.value = value
        self.css = css
        self.disabled = disabled
        self.editable = editable
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.required = required
        self.validation = validation
        self.width = width
        self.customColors = customColors
        self.grayShades = grayShades
        self.icon = icon
        self.mode = mode
        self.palette = palette
        self.paletteOnly = paletteOnly
        self.pickerOnly = pickerOnly
        self.placeholder = placeholder
        self.hiddenLabel = hiddenLabel
        self.label = label
        self.labelPosition = labelPosition
        self.labelWidth = labelWidth
        self.helpMessage = helpMessage
        self.preMessage = preMessage
        self.successMessage = successMessage
        self.errorMessage = errorMessage

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ColorPickerConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'value': self.value,
            'css': self.css,
            'disabled': self.disabled,
            'editable': self.editable,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'required': self.required,
            'width': self.width,
            'customColors': self.customColors,
            'grayShades': self.grayShades,
            'icon': self.icon,
            'mode': self.mode,
            'palette': self.palette,
            'paletteOnly': self.paletteOnly,
            'pickerOnly': self.pickerOnly,
            'placeholder': self.placeholder,
            'hiddenLabel': self.hiddenLabel,
            'label': self.label,
            'labelPosition': self.labelPosition,
            'labelWidth': self.labelWidth,
            'helpMessage': self.helpMessage,
            'preMessage': self.preMessage,
            'successMessage': self.successMessage,
            'errorMessage': self.errorMessage,
            'validation': self.validation
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}

        # Handle functions
        if 'validation' in config_dict:
            config_dict['validation'] = create_proxy(self.validation)

        return config_dict
