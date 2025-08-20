"""A Python interface for the DHX Calendar JavaScript widget.

This module provides the `Calendar` class to create and manage a calendar widget,
with support for date selection, event handling, and configuration of display properties.
It relies on Pyodide to interface with the JavaScript-based DHX Calendar library.

"""

from typing import Any, Callable, List, Union
import js
import json
from pyodide.ffi import create_proxy

from .calendar_config import CalendarConfig

class Calendar:
    """A Python wrapper for the DHX Calendar JavaScript widget.

    This class provides an interface to create and manipulate a calendar widget,
    allowing users to select dates, configure display modes, and handle events.
    It integrates with a JavaScript-based calendar via Pyodide.

    Args:
        config (CalendarConfig): Configuration object for the calendar.
        widget_parent (Any, optional): The parent DOM element for the calendar. Defaults to None.

    Example:
        ```
        from calendar_config import CalendarConfig
        config = CalendarConfig(date_format="%Y-%m-%d")
        cal = Calendar(config)
        cal.set_value("2025-08-12")
        print(cal.get_value())
        '2025-08-12'
        ```
    """
    def __init__(self, config: CalendarConfig, widget_parent: Any = None):
        """Initializes the calendar instance."""
        self.calendar = js.dhx.Calendar.new(widget_parent, js.JSON.parse(json.dumps(config.to_dict())))

    """ Calendar API Functions """

    def clear(self) -> None:
        """Clears the value set in the calendar.

        Resets the selected date(s) to an empty state.
        """
        self.calendar.clear()

    def destructor(self) -> None:
        """Removes a calendar instance and releases occupied resources.

        Call this method to clean up the calendar widget when it is no longer needed.
        """
        self.calendar.destructor()

    def get_current_mode(self) -> str:
        """Returns the current mode of displaying the Calendar.

        Returns:
            str: The current mode (e.g., 'calendar', 'month', 'year').
        """
        return self.calendar.getCurrentMode()

    def get_value(self, as_date_obj: bool = False) -> Union[str, List[str]]:
        """Returns the selected date(s) in the calendar.

        Args:
            as_date_obj (bool, optional): If True, returns the date(s) as JavaScript Date object(s).
                                         If False, returns date(s) as string(s) in the configured format.
                                         Defaults to False.

        Returns:
            Union[str, List[str]]: A single date string or a list of date strings (e.g., '2025-08-12').
                                 If `as_date_obj` is True, returns JavaScript Date object(s).

        Example:
            >>> cal.set_value("2025-08-12")
            >>> cal.get_value()
            '2025-08-12'
            >>> cal.get_value(as_date_obj=True)
            <JavaScript Date object>
        """
        return self.calendar.getValue(as_date_obj)

    def link(self, calendar: Any) -> None:
        """Links the calendar to another calendar for selecting a date range.

        Args:
            calendar (Calendar): Another Calendar instance to link with for range selection.
        """
        self.calendar.link(calendar.calendar)

    def paint(self) -> None:
        """Repaints the calendar on a page.

        Call this method to refresh the calendar's display after changes.
        """
        self.calendar.paint()

    def set_value(self, value: Union[str, List[str]]) -> bool:
        """Selects a date or dates in the calendar.

        Args:
            value (Union[str, List[str]]): A single date string (e.g., '2025-08-12') or a list of date strings.

        Returns:
            bool: True if the value was set successfully, False otherwise.

        Example:
            >>> cal.set_value(["2025-08-12", "2025-08-15"])
            True
        """
        return self.calendar.setValue(value)

    def show_date(self, date: Union[str, None] = None, mode: str = "calendar") -> None:
        """Shows a specified date and/or opens the calendar in one of the available modes.

        Args:
            date (Union[str, None], optional): The date to show (e.g., '2025-08-12'). If None, shows the current date.
            mode (str, optional): The display mode ('calendar', 'month', or 'year'). Defaults to 'calendar'.
        """
        self.calendar.showDate(date, mode)

    """ Calendar Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper method to dynamically add event handlers.

        Args:
            event_name (str): The name of the event (e.g., 'beforeChange', 'change').
            handler (Callable): The callback function to handle the event.
        """
        event_proxy = create_proxy(handler)
        self.calendar.events[event_name] = event_proxy

    def before_change(self, handler: Callable[[str, str, bool], Union[bool, None]]) -> None:
        """Fires before the change of date selection.

        Args:
            handler (Callable[[str, str, bool], Union[bool, None]]): A callback function that receives:
                - old_date (str): The previously selected date.
                - new_date (str): The newly selected date.
                - click (bool): Whether the change was triggered by a user click.
                The handler can return False to cancel the change, or None to allow it.

        Example:
            >>> def on_before_change(old_date, new_date, click):
            ...     print(f"Changing from {old_date} to {new_date}")
            ...     return True
            >>> cal.before_change(on_before_change)
        """
        self.add_event_handler('beforeChange', handler)

    def cancel_click(self, handler: Callable[[], None]) -> None:
        """Fires when the user clicks on the 'Cancel' control.

        Args:
            handler (Callable[[], None]): A callback function to handle the cancel click event.
        """
        self.add_event_handler('cancelClick', handler)

    def change(self, handler: Callable[[str, str, bool], None]) -> None:
        """Fires on change of date selection.

        Args:
            handler (Callable[[str, str, bool], None]): A callback function that receives:
                - old_date (str): The previously selected date.
                - new_date (str): The newly selected date.
                - click (bool): Whether the change was triggered by a user click.

        Example:
            >>> def on_change(old_date, new_date, click):
            ...     print(f"Date changed to {new_date}")
            >>> cal.change(on_change)
        """
        self.add_event_handler('change', handler)

    def date_mouse_over(self, handler: Callable[[str, str], None]) -> None:
        """Fires when the mouse pointer is over a date.

        Args:
            handler (Callable[[str, str], None]): A callback function that receives:
                - date (str): The date under the mouse pointer.
                - formatted_date (str): The formatted date string.
        """
        self.add_event_handler('dateMouseOver', handler)

    def mode_change(self, handler: Callable[[str], None]) -> None:
        """Fires on change of the calendar mode.

        Args:
            handler (Callable[[str], None]): A callback function that receives:
                - mode (str): The new mode ('calendar', 'month', or 'year').
        """
        self.add_event_handler('modeChange', handler)

    def month_selected(self, handler: Callable[[int], None]) -> None:
        """Fires after a month was selected in the calendar.

        Args:
            handler (Callable[[int], None]): A callback function that receives:
                - month (int): The selected month (0-11).
        """
        self.add_event_handler('monthSelected', handler)

    def year_selected(self, handler: Callable[[int], None]) -> None:
        """Fires after a year was selected in the calendar.

        Args:
            handler (Callable[[int], None]): A callback function that receives:
                - year (int): The selected year.
        """
        self.add_event_handler('yearSelected', handler)

    """ Calendar Properties """

    @property
    def css(self) -> str:
        """Adds style classes to the calendar.

        Returns:
            str: The CSS class(es) applied to the calendar.
        """
        return self.calendar.css

    @css.setter
    def css(self, value: str) -> None:
        self.calendar.css = value

    @property
    def date(self) -> str:
        """Defines the date that will be opened when the calendar is created.

        Returns:
            str: The initial date string (e.g., '2025-08-12').
        """
        return self.calendar.date

    @date.setter
    def date(self, value: str) -> None:
        self.calendar.date = value

    @property
    def date_format(self) -> str:
        """Defines the format of dates in the calendar.

        The format string follows the DHX Calendar specification (e.g., '%Y-%m-%d' for 'YYYY-MM-DD').

        Returns:
            str: The current date format string.
        """
        return self.calendar.dateFormat

    @date_format.setter
    def date_format(self, value: str) -> None:
        self.calendar.dateFormat = value

    @property
    def disabled_dates(self) -> Callable[[str], bool]:
        """Allows disabling some date intervals.

        Returns:
            Callable[[str], bool]: A function that takes a date string and returns True if the date should be disabled.
        """
        return self.calendar.disabledDates

    @disabled_dates.setter
    def disabled_dates(self, value: Callable[[str], bool]) -> None:
        self.calendar.disabledDates = value

    @property
    def mark(self) -> Callable[[str], str]:
        """Adds a CSS class to specific days.

        Returns:
            Callable[[str], str]: A function that takes a date string and returns a CSS class to apply.
        """
        return self.calendar.mark

    @mark.setter
    def mark(self, value: Callable[[str], str]) -> None:
        self.calendar.mark = value

    @property
    def mode(self) -> str:
        """The mode of Calendar initialization.

        Returns:
            str: The current mode ('calendar', 'month', or 'year').
        """
        return self.calendar.mode

    @mode.setter
    def mode(self, value: str) -> None:
        self.calendar.mode = value

    @property
    def range(self) -> bool:
        """Enables/disables the possibility to select a range of dates.

        Returns:
            bool: True if range selection is enabled, False otherwise.
        """
        return self.calendar.range

    @range.setter
    def range(self, value: bool) -> None:
        self.calendar.range = value

    @property
    def this_month_only(self) -> bool:
        """Hides dates of the previous/next months relative to the currently displayed one.

        Returns:
            bool: True if only the current month's dates are shown, False otherwise.
        """
        return self.calendar.thisMonthOnly

    @this_month_only.setter
    def this_month_only(self, value: bool) -> None:
        self.calendar.thisMonthOnly = value

    @property
    def time_format(self) -> int:
        """Defines the time format for the timepicker in the calendar.

        Returns:
            int: The time format (e.g., 12 for 12-hour, 24 for 24-hour).
        """
        return self.calendar.timeFormat

    @time_format.setter
    def time_format(self, value: int) -> None:
        self.calendar.timeFormat = value

    @property
    def time_picker(self) -> bool:
        """Adds a timepicker into the calendar.

        Returns:
            bool: True if the timepicker is enabled, False otherwise.
        """
        return self.calendar.timePicker

    @time_picker.setter
    def time_picker(self, value: bool) -> None:
        self.calendar.timePicker = value

    @property
    def value(self) -> Union[str, List[str]]:
        """Selects the day(s) (adds a round blue marker).

        Returns:
            Union[str, List[str]]: The selected date(s) as a string or list of strings.
        """
        return self.calendar.value

    @value.setter
    def value(self, value: Union[str, List[str]]) -> None:
        self.calendar.value = value

    @property
    def week_numbers(self) -> bool:
        """Defines whether to show the numbers of weeks.

        Returns:
            bool: True if week numbers are shown, False otherwise.
        """
        return self.calendar.weekNumbers

    @week_numbers.setter
    def week_numbers(self, value: bool) -> None:
        self.calendar.weekNumbers = value

    @property
    def week_start(self) -> str:
        """Sets the starting day of the week.

        Returns:
            str: The starting day (e.g., 'sunday', 'monday').
        """
        return self.calendar.weekStart

    @week_start.setter
    def week_start(self, value: str) -> None:
        self.calendar.weekStart = value

    @property
    def width(self) -> Union[str, int]:
        """Sets the width of the calendar.

        Returns:
            Union[str, int]: The width of the calendar (e.g., '300px' or 300).
        """
        return self.calendar.width

    @width.setter
    def width(self, value: Union[str, int]) -> None:
        self.calendar.width = value