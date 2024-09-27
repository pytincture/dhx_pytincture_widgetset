from typing import Any, Callable, Dict, Optional, Union


class TimepickerConfig:
    """
    Configuration class for the TimePicker widget.
    """

    def __init__(self,
                 value: Union[Dict[str, int], str, int, list, object] = None,
                 controls: bool = False,
                 css: str = None,
                 timeFormat: int = 24,
                 valueFormat: str = None):
        """
        Initializes the TimePickerConfig.

        :param value: (Optional) The time value to be set on initialization of the timepicker.
        :param controls: (Optional) Defines whether a timepicker is equipped with the Close and Save buttons. Default is False.
        :param css: (Optional) Adds style classes to TimePicker.
        :param timeFormat: (Optional) Defines what clock format is activated: the 12-hour or 24-hour one. Default is 24.
        :param valueFormat: (Optional) Defines the format of the value to be applied when working with TimePicker events.
        """
        self.value = value
        self.controls = controls
        self.css = css
        self.timeFormat = timeFormat
        self.valueFormat = valueFormat

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the TimePickerConfig into a dictionary format.
        """
        config_dict = {
            'value': self.value,
            'controls': self.controls,
            'css': self.css,
            'timeFormat': self.timeFormat,
            'valueFormat': self.valueFormat,
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}
        return config_dict
