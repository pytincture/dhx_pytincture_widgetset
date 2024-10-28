from typing import Union, List, Dict, Any, Callable



class SliderConfig:
    """
    Configuration class for the Slider control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 value: Union[float, List[float]] = None,
                 css: str = None,
                 disabled: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 width: Union[str, int] = "content",
                 inverse: bool = False,
                 majorTick: Union[int, float] = None,
                 max: Union[int, float] = 100,
                 min: Union[int, float] = 0,
                 mode: str = "horizontal",
                 range: bool = False,
                 step: Union[int, float] = 1,
                 tick: Union[int, float] = None,
                 tickTemplate: Callable[[Any], str] = None,
                 tooltip: bool = True,
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None):
        """
        Initializes the SliderConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param value: (Optional) The initial value(s) of the slider.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param width: (Optional) The width of the control.
        :param inverse: (Optional) Enables the inverse slider mode.
        :param majorTick: (Optional) Interval of rendering numeric values on the scale.
        :param max: (Optional) The maximal value of the slider.
        :param min: (Optional) The minimal value of the slider.
        :param mode: (Optional) Direction of the Slider scale.
        :param range: (Optional) Enables selecting a range of values.
        :param step: (Optional) The step the slider thumb will be moved with.
        :param tick: (Optional) Interval of steps for rendering the scale.
        :param tickTemplate: (Optional) Template for rendering values on the scale.
        :param tooltip: (Optional) Enables prompt messages with ticks values.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        """
        self.type = "slider"
        self.name = name
        self.id = id
        self.value = value
        self.css = css
        self.disabled = disabled
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.width = width
        self.inverse = inverse
        self.majorTick = majorTick
        self.max = max
        self.min = min
        self.mode = mode
        self.range = range
        self.step = step
        self.tick = tick
        self.tickTemplate = tickTemplate
        self.tooltip = tooltip
        self.hiddenLabel = hiddenLabel
        self.label = label
        self.labelPosition = labelPosition
        self.labelWidth = labelWidth
        self.helpMessage = helpMessage

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the SliderConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'value': self.value,
            'css': self.css,
            'disabled': self.disabled,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'width': self.width,
            'inverse': self.inverse,
            'majorTick': self.majorTick,
            'max': self.max,
            'min': self.min,
            'mode': self.mode,
            'range': self.range,
            'step': self.step,
            'tick': self.tick,
            'tickTemplate': self.tickTemplate,
            'tooltip': self.tooltip,
            'hiddenLabel': self.hiddenLabel,
            'label': self.label,
            'labelPosition': self.labelPosition,
            'labelWidth': self.labelWidth,
            'helpMessage': self.helpMessage
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}

        # Handle tickTemplate function
        if 'tickTemplate' in config_dict and callable(config_dict['tickTemplate']):
            config_dict['tickTemplate'] = create_proxy(self.tickTemplate)

        return config_dict
