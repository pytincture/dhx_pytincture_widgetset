from typing import Any, Callable, List, Union
import js
import json
from pyodide.ffi import create_proxy

from .calendar_config import CalendarConfig

str = None
str = None

class Calendar:
    def __init__(self, config: CalendarConfig, widget_parent: Any = None):
        """Initializes the calendar instance."""
        self.calendar = js.dhx.Calendar.new(widget_parent, js.JSON.parse(json.dumps(config.to_dict())))

    """ Calendar API Functions """

    def clear(self) -> None:
        """Clears the value set in the calendar."""
        self.calendar.clear()

    def destructor(self) -> None:
        """Removes a calendar instance and releases occupied resources."""
        self.calendar.destructor()

    def get_current_mode(self) -> str:
        """Returns the current mode of displaying the Calendar."""
        return self.calendar.getCurrentMode()

    def get_value(self, as_date_obj: bool = False) -> Union[Union[str, List[str]], Union[str, List[str]]]:
        """Returns the selected date(s)."""
        return self.calendar.getValue(as_date_obj)

    def link(self, calendar: Any) -> None:
        """Links the calendar to another calendar for selecting a date range."""
        self.calendar.link(calendar.calendar)

    def paint(self) -> None:
        """Repaints the calendar on a page."""
        self.calendar.paint()

    def set_value(self, value: Union[str, List[str], str, List[str]]) -> bool:
        """Selects a date in the calendar."""
        return self.calendar.setValue(value)

    def show_date(self, date: Union[str, str] = None, mode: str = "calendar") -> None:
        """Shows a specified date and/or opens the calendar in one of the available modes."""
        self.calendar.showDate(date, mode)

    """ Calendar Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper method to dynamically add event handlers."""
        event_proxy = create_proxy(handler)
        self.calendar.events[event_name] = event_proxy

    def before_change(self, handler: Callable[[str, str, bool], Union[bool, None]]) -> None:
        """Fires before the change of date selection."""
        self.add_event_handler('beforeChange', handler)

    def cancel_click(self, handler: Callable[[], None]) -> None:
        """Fires when the user clicks on the 'Cancel' control."""
        self.add_event_handler('cancelClick', handler)

    def change(self, handler: Callable[[str, str, bool], None]) -> None:
        """Fires on change of date selection."""
        self.add_event_handler('change', handler)

    def date_mouse_over(self, handler: Callable[[str, str], None]) -> None:
        """Fires when the mouse pointer is over a date."""
        self.add_event_handler('dateMouseOver', handler)

    def mode_change(self, handler: Callable[[str], None]) -> None:
        """Fires on change of the calendar mode."""
        self.add_event_handler('modeChange', handler)

    def month_selected(self, handler: Callable[[int], None]) -> None:
        """Fires after a month was selected in the calendar."""
        self.add_event_handler('monthSelected', handler)

    def year_selected(self, handler: Callable[[int], None]) -> None:
        """Fires after a year was selected in the calendar."""
        self.add_event_handler('yearSelected', handler)

    """ Calendar Properties """

    @property
    def css(self) -> str:
        """Optional. Adds style classes to the calendar."""
        return self.calendar.css

    @css.setter
    def css(self, value: str) -> None:
        self.calendar.css = value

    @property
    def date(self) -> Union[str, str]:
        """Optional. Defines the date that will be opened when the calendar is created."""
        return self.calendar.date

    @date.setter
    def date(self, value: Union[str, str]) -> None:
        self.calendar.date = value

    @property
    def date_format(self) -> str:
        """Optional. Defines the format of dates in the calendar."""
        return self.calendar.dateFormat

    @date_format.setter
    def date_format(self, value: str) -> None:
        self.calendar.dateFormat = value

    @property
    def disabled_dates(self) -> Callable[[str], bool]:
        """Optional. Allows disabling some date intervals."""
        return self.calendar.disabledDates

    @disabled_dates.setter
    def disabled_dates(self, value: Callable[[str], bool]) -> None:
        self.calendar.disabledDates = value

    @property
    def mark(self) -> Callable[[str], str]:
        """Optional. Adds a CSS class to specific days."""
        return self.calendar.mark

    @mark.setter
    def mark(self, value: Callable[[str], str]) -> None:
        self.calendar.mark = value

    @property
    def mode(self) -> str:
        """Optional. The mode of Calendar initialization."""
        return self.calendar.mode

    @mode.setter
    def mode(self, value: str) -> None:
        self.calendar.mode = value

    @property
    def range(self) -> bool:
        """Optional. Enables/disables the possibility to select a range of dates."""
        return self.calendar.range

    @range.setter
    def range(self, value: bool) -> None:
        self.calendar.range = value

    @property
    def this_month_only(self) -> bool:
        """Optional. Hides dates of the previous/next months relative to the currently displayed one."""
        return self.calendar.thisMonthOnly

    @this_month_only.setter
    def this_month_only(self, value: bool) -> None:
        self.calendar.thisMonthOnly = value

    @property
    def time_format(self) -> int:
        """Optional. Defines the time format for the timepicker in the calendar."""
        return self.calendar.timeFormat

    @time_format.setter
    def time_format(self, value: int) -> None:
        self.calendar.timeFormat = value

    @property
    def time_picker(self) -> bool:
        """Optional. Adds a timepicker into the calendar."""
        return self.calendar.timePicker

    @time_picker.setter
    def time_picker(self, value: bool) -> None:
        self.calendar.timePicker = value

    @property
    def value(self) -> Union[str, List[str], str, List[str]]:
        """Optional. Selects the day(s) (adds a round blue marker)."""
        return self.calendar.value

    @value.setter
    def value(self, value: Union[str, List[str], str, List[str]]) -> None:
        self.calendar.value = value

    @property
    def week_numbers(self) -> bool:
        """Optional. Defines whether to show the numbers of weeks."""
        return self.calendar.weekNumbers

    @week_numbers.setter
    def week_numbers(self, value: bool) -> None:
        self.calendar.weekNumbers = value

    @property
    def week_start(self) -> str:
        """Optional. Sets the starting day of the week."""
        return self.calendar.weekStart

    @week_start.setter
    def week_start(self, value: str) -> None:
        self.calendar.weekStart = value

    @property
    def width(self) -> Union[str, int]:
        """Optional. Sets the width of the calendar."""
        return self.calendar.width

    @width.setter
    def width(self, value: Union[str, int]) -> None:
        self.calendar.width = value
