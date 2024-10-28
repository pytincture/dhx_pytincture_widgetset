from typing import Union, Dict, Any, Callable

from pyodide.ffi import create_proxy


class DatepickerConfig:
    """
    Configuration class for the DatePicker control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 value: Union[str, Any] = None,
                 css: str = None,
                 disabled: bool = False,
                 editable: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 required: bool = False,
                 validation: Callable[[Any], bool] = None,
                 width: Union[str, int] = "content",
                 date: Union[str, Any] = None,
                 dateFormat: str = "%d/%m/%y",
                 disabledDates: Any = None,
                 icon: str = None,
                 mark: Any = None,
                 mode: str = "calendar",
                 placeholder: str = None,
                 thisMonthOnly: bool = False,
                 timeFormat: Union[int, str] = 24,
                 timePicker: bool = False,
                 valueFormat: str = "string",
                 weekNumbers: bool = False,
                 weekStart: str = "sunday",
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None):
        """
        Initializes the DatePickerConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param value: (Optional) The value of the datepicker.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param editable: (Optional) Allows user to enter the value manually.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param required: (Optional) Whether the control is required.
        :param validation: (Optional) The validation function.
        :param width: (Optional) The width of the control.
        :param date: (Optional) The date that will be opened when the calendar is created.
        :param dateFormat: (Optional) The format of dates in the calendar.
        :param disabledDates: (Optional) Disables some date intervals.
        :param icon: (Optional) The CSS class name of an icon.
        :param mark: (Optional) Adds a CSS class to specific days.
        :param mode: (Optional) Specifies the mode of displaying a calendar.
        :param placeholder: (Optional) A tip for the input.
        :param thisMonthOnly: (Optional) Hides dates of the previous/next months.
        :param timeFormat: (Optional) Time format of a timepicker: 12 or 24.
        :param timePicker: (Optional) Adds a timepicker into the calendar.
        :param valueFormat: (Optional) Format of the returned value: "string" or "Date".
        :param weekNumbers: (Optional) Shows the numbers of weeks.
        :param weekStart: (Optional) Starting day of the week.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message after successful validation.
        :param errorMessage: (Optional) Message after validation error.
        """
        self.type = "datepicker"
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
        self.date = date
        self.dateFormat = dateFormat
        self.disabledDates = disabledDates
        self.icon = icon
        self.mark = mark
        self.mode = mode
        self.placeholder = placeholder
        self.thisMonthOnly = thisMonthOnly
        self.timeFormat = timeFormat
        self.timePicker = timePicker
        self.valueFormat = valueFormat
        self.weekNumbers = weekNumbers
        self.weekStart = weekStart
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
        Converts the DatePickerConfig into a dictionary format.
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
            'validation': self.validation,
            'width': self.width,
            'date': self.date,
            'dateFormat': self.dateFormat,
            'disabledDates': self.disabledDates,
            'icon': self.icon,
            'mark': self.mark,
            'mode': self.mode,
            'placeholder': self.placeholder,
            'thisMonthOnly': self.thisMonthOnly,
            'timeFormat': self.timeFormat,
            'timePicker': self.timePicker,
            'valueFormat': self.valueFormat,
            'weekNumbers': self.weekNumbers,
            'weekStart': self.weekStart,
            'hiddenLabel': self.hiddenLabel,
            'label': self.label,
            'labelPosition': self.labelPosition,
            'labelWidth': self.labelWidth,
            'helpMessage': self.helpMessage,
            'preMessage': self.preMessage,
            'successMessage': self.successMessage,
            'errorMessage': self.errorMessage
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}

        # Handle functions
        if 'validation' in config_dict:
            config_dict['validation'] = create_proxy(self.validation)

        return config_dict
