from typing import Any, Callable, Dict, Optional, Union



class SliderConfig:
    """
    Configuration class for the Slider widget.
    """

    def __init__(self,
                 min: float,
                 max: float,
                 step: float = 1,
                 value: Union[float, str, list] = None,
                 css: str = None,
                 helpMessage: str = None,
                 hiddenLabel: bool = None,
                 inverse: bool = None,
                 label: str = None,
                 labelPosition: str = None,
                 labelWidth: Union[str, int] = None,
                 majorTick: float = None,
                 mode: str = "horizontal",
                 range: bool = None,
                 tick: float = None,
                 tickTemplate: Callable[[float], str] = None,
                 tooltip: bool = True):
        """
        Initializes the SliderConfig.

        :param min: (Required) The minimal value of slider.
        :param max: (Required) The maximal value of slider.
        :param step: (Optional) The step the slider thumb will be moved with. Default is 1.
        :param value: (Optional) The value the thumb will be set at on initialization of the slider.
        :param css: (Optional) Adds style classes for the component.
        :param helpMessage: (Optional) Adds an icon with a question mark next to Slider.
        :param hiddenLabel: (Optional) Adds a hidden label for a Slider that will be used while sending a form to the server.
        :param inverse: (Optional) Enables/disables the inverse slider mode.
        :param label: (Optional) Specifies the label of a slider.
        :param labelPosition: (Optional) Defines the position of a label of a slider ("left" | "top").
        :param labelWidth: (Optional) Sets the width of a label.
        :param majorTick: (Optional) Sets interval of rendering numeric values on the slider scale.
        :param mode: (Optional) The direction of the Slider scale ("vertical" | "horizontal"). Default is "horizontal".
        :param range: (Optional) Enables/disables the possibility to select a range of values on the slider.
        :param tick: (Optional) Sets the interval of steps for rendering the slider scale.
        :param tickTemplate: (Optional) Sets a template for rendering values on the scale.
        :param tooltip: (Optional) Enables a tooltip on hovering over the slider thumb. Default is True.
        """
        self.min = min
        self.max = max
        self.step = step
        self.value = value
        self.css = css
        self.helpMessage = helpMessage
        self.hiddenLabel = hiddenLabel
        self.inverse = inverse
        self.label = label
        self.labelPosition = labelPosition
        self.labelWidth = labelWidth
        self.majorTick = majorTick
        self.mode = mode
        self.range = range
        self.tick = tick
        self.tickTemplate = tickTemplate
        self.tooltip = tooltip

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the SliderConfig into a dictionary format.
        """
        config_dict = {
            'min': self.min,
            'max': self.max,
            'step': self.step,
            'value': self.value,
            'css': self.css,
            'helpMessage': self.helpMessage,
            'hiddenLabel': self.hiddenLabel,
            'inverse': self.inverse,
            'label': self.label,
            'labelPosition': self.labelPosition,
            'labelWidth': self.labelWidth,
            'majorTick': self.majorTick,
            'mode': self.mode,
            'range': self.range,
            'tick': self.tick,
            'tooltip': self.tooltip,
        }
        # Handle the tickTemplate function
        if self.tickTemplate:
            # Since tickTemplate is a function, we can't serialize it to JSON
            # We'll store it separately and handle it in the Slider class
            config_dict['tickTemplate'] = self.tickTemplate

        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}
        return config_dict
