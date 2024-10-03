from typing import List, Union, Dict, Any, Callable

class ControlConfig:
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

class CalendarConfig(ControlConfig):
    """Configuration class for Calendar."""
    def __init__(self,
                 date: Union[str, Any] = None,
                 date_format: str = "%d/%m/%y",
                 disabled_dates: Callable[[Any], bool] = None,
                 mark: Callable[[Any], str] = None,
                 mode: str = "calendar",
                 range: bool = False,
                 this_month_only: bool = False,
                 time_format: int = 24,
                 time_picker: bool = False,
                 value: Union[str, Any, List[Union[str, Any]]] = None,
                 week_numbers: bool = False,
                 week_start: str = "sunday",
                 css: str = None,
                 width: Union[int, str] = "250px"):
        self.date = date
        self.date_format = date_format
        self.disabled_dates = disabled_dates
        self.mark = mark
        self.mode = mode
        self.range = range
        self.this_month_only = this_month_only
        self.time_format = time_format
        self.time_picker = time_picker
        self.value = value
        self.week_numbers = week_numbers
        self.week_start = week_start
        self.css = css
        self.width = width