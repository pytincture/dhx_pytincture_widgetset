"""
pyTincture Form widget implementation
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .form_config import FormConfig


class Form:
    def __init__(self, config: FormConfig = None, widget_parent: Any = None):
        """Initializes the Form instance."""
        if config is None:
            config = FormConfig()
        config_dict = config.to_dict()
        self.form = js.dhx.Form.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Form API Functions """

    def blur(self, name: str = None) -> None:
        """Removes focus from a control of the Form."""
        self.form.blur(name)

    def clear(self, method: str = None) -> None:
        """Clears the form."""
        self.form.clear(method)

    def destructor(self) -> None:
        """Removes the Form instance and releases occupied resources."""
        self.form.destructor()

    def disable(self) -> None:
        """Disables the Form."""
        self.form.disable()

    def enable(self) -> None:
        """Enables the Form."""
        self.form.enable()

    def for_each(self, callback: Callable[[Any, int, List[Any]], Any]) -> None:
        """Iterates over all controls of the Form."""
        proxy_callback = create_proxy(callback)
        self.form.forEach(proxy_callback)

    def get_item(self, name: str) -> Any:
        """Gives access to the object of a Form control."""
        return self.form.getItem(name)

    def get_properties(self, name: str = None) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
        """Returns objects with available configuration attributes of Form controls."""
        return self.form.getProperties(name)

    def get_value(self, as_form_data: bool = False) -> Dict[str, Any]:
        """Gets current values/states of controls."""
        return self.form.getValue(as_form_data)

    def hide(self) -> None:
        """Hides the Form."""
        self.form.hide()

    def is_disabled(self, name: str = None) -> bool:
        """Checks whether the Form or a control is disabled."""
        return self.form.isDisabled(name)

    def is_visible(self, name: str = None) -> bool:
        """Checks whether the Form or a control is visible."""
        return self.form.isVisible(name)

    def paint(self) -> None:
        """Repaints the Form on the page."""
        self.form.paint()

    def send(self, url: str, method: str = "POST", as_form_data: bool = False) -> Any:
        """Sends the Form to the server."""
        return self.form.send(url, method, as_form_data)

    def set_focus(self, name: str) -> None:
        """Sets focus to a Form control by its name or id."""
        self.form.setFocus(name)

    def set_properties(self, arg: Union[str, Dict[str, Dict[str, Any]]], properties: Dict[str, Any] = None) -> None:
        """Allows changing available configuration attributes of Form controls dynamically."""
        if isinstance(arg, str):
            self.form.setProperties(arg, js.JSON.parse(json.dumps(properties)))
        elif isinstance(arg, dict):
            props = {k: js.JSON.parse(json.dumps(v)) for k, v in arg.items()}
            self.form.setProperties(props)
        else:
            raise TypeError("Argument must be a string or a dictionary")

    def set_value(self, obj: Dict[str, Any]) -> None:
        """Sets values/states for controls."""
        self.form.setValue(js.JSON.parse(json.dumps(obj)))

    def show(self) -> None:
        """Shows the Form on the page."""
        self.form.show()

    def validate(self, silent: bool = False) -> bool:
        """Validates form fields."""
        return self.form.validate(silent)

    """ Form Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.form.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[str, Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes of a Form control have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[str, Any, str], None]) -> None:
        """Fires after a Form control or its element is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_send(self, handler: Callable[[], None]) -> None:
        """Fires after a form is sent to the server."""
        self.add_event_handler('afterSend', handler)

    def on_after_show(self, handler: Callable[[str, Any, str], None]) -> None:
        """Fires after a Form control or its element is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[str, Any, bool], None]) -> None:
        """Fires after validation of form fields is finished."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change(self, handler: Callable[[str, Any], Union[bool, None]]) -> None:
        """Fires before changing the value of a control."""
        def event_handler(name, value):
            result = handler(name, value)
            if result is False:
                return js.Boolean(False)
        self.form.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[str, Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes of a Form control are changed dynamically."""
        def event_handler(name, properties):
            result = handler(name, properties)
            if result is False:
                return js.Boolean(False)
        self.form.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Union[str, int], Any, str], Union[bool, None]]) -> None:
        """Fires before a Form control or its element is hidden."""
        def event_handler(name, value=None, id=None):
            result = handler(name, value, id)
            if result is False:
                return js.Boolean(False)
        self.form.events.on('beforeHide', create_proxy(event_handler))

    def on_before_send(self, handler: Callable[[], Union[bool, None]]) -> None:
        """Fires before a form is sent to the server."""
        def event_handler():
            result = handler()
            if result is False:
                return js.Boolean(False)
        self.form.events.on('beforeSend', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[str, Any, str], Union[bool, None]]) -> None:
        """Fires before a Form control or its element is shown."""
        def event_handler(name, value=None, id=None):
            result = handler(name, value, id)
            if result is False:
                return js.Boolean(False)
        self.form.events.on('beforeShow', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[str, Any], Union[bool, None]]) -> None:
        """Fires before validation of form fields has started."""
        def event_handler(name, value):
            result = handler(name, value)
            if result is False:
                return js.Boolean(False)
        self.form.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[str, Any, str], None]) -> None:
        """Fires when a control of Form has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[str, Any], None]) -> None:
        """Fires on changing the value of a control."""
        self.add_event_handler('change', handler)

    def on_click(self, handler: Callable[[str, Any], Any]) -> None:
        """Fires after a click on a button in a form."""
        self.add_event_handler('click', handler)

    def on_focus(self, handler: Callable[[str, Any, str], None]) -> None:
        """Fires when a control of Form has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any, str, str], None]) -> None:
        """Fires when any key is pressed."""
        self.add_event_handler('keydown', handler)

    """ Form Properties """

    @property
    def align(self) -> str:
        """Gets or sets the alignment of controls inside the control group."""
        return self.form.config.align

    @align.setter
    def align(self, value: str) -> None:
        self.form.config.align = value

    @property
    def cols(self) -> List[Dict[str, Any]]:
        """Gets or sets the columns of controls inside the control group."""
        return self.form.config.cols

    @cols.setter
    def cols(self, value: List[Dict[str, Any]]) -> None:
        self.form.config.cols = value

    @property
    def css(self) -> str:
        """Gets or sets the CSS classes applied to the control group."""
        return self.form.config.css

    @css.setter
    def css(self, value: str) -> None:
        self.form.config.css = value

    @property
    def disabled(self) -> bool:
        """Gets or sets whether the Form is disabled."""
        return self.form.config.disabled

    @disabled.setter
    def disabled(self, value: bool) -> None:
        self.form.config.disabled = value

    @property
    def height(self) -> Union[str, int]:
        """Gets or sets the height of the control group."""
        return self.form.config.height

    @height.setter
    def height(self, value: Union[str, int, str]) -> None:
        self.form.config.height = value

    @property
    def hidden(self) -> bool:
        """Gets or sets whether the Form is hidden."""
        return self.form.config.hidden

    @hidden.setter
    def hidden(self, value: bool) -> None:
        self.form.config.hidden = value

    @property
    def padding(self) -> Union[str, int]:
        """Gets or sets the padding for content inside the control group."""
        return self.form.config.padding

    @padding.setter
    def padding(self, value: Union[str, int]) -> None:
        self.form.config.padding = value

    @property
    def rows(self) -> List[Dict[str, Any]]:
        """Gets or sets the rows of controls inside the control group."""
        return self.form.config.rows

    @rows.setter
    def rows(self, value: List[Dict[str, Any]]) -> None:
        self.form.config.rows = value

    @property
    def title(self) -> str:
        """Gets or sets the title of the control group."""
        return self.form.config.title

    @title.setter
    def title(self, value: str) -> None:
        self.form.config.title = value

    @property
    def width(self) -> Union[str, int]:
        """Gets or sets the width of the control group."""
        return self.form.config.width

    @width.setter
    def width(self, value: Union[str, int, str]) -> None:
        self.form.config.width = value

