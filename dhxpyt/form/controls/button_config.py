from typing import Union, Dict, Any
from pyodide.ffi import create_proxy


class ButtonConfig:
    """
    Configuration class for the Button control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 text: str = None,
                 submit: bool = False,
                 url: str = None,
                 css: str = None,
                 disabled: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = "5px",
                 width: Union[str, int] = "content",
                 circle: bool = False,
                 color: str = "primary",
                 full: bool = False,
                 icon: str = None,
                 loading: bool = False,
                 size: str = "medium",
                 view: str = "flat"):
        """
        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param text: (Optional) The text label of the button.
        :param submit: (Optional) Enables the button to send form data to a server.
        :param url: (Optional) The URL the post request with form data will be sent to.
        :param css: (Optional) Adds style classes to the control.
        :param disabled: (Optional) Whether the control is disabled.
        :param height: (Optional) The height of the control.
        :param hidden: (Optional) Whether the control is hidden.
        :param padding: (Optional) Sets padding between the cell and border.
        :param width: (Optional) The width of the control.
        :param circle: (Optional) Makes the corners of the button round.
        :param color: (Optional) Defines the color scheme of the button.
        :param full: (Optional) Extends the button to the full width of the form.
        :param icon: (Optional) The CSS class of an icon of the button.
        :param loading: (Optional) Adds a spinner into the button.
        :param size: (Optional) Defines the size of the button.
        :param view: (Optional) Defines the look of the button.
        """
        self.type = "button"
        self.name = name
        self.id = id
        self.text = text
        self.submit = submit
        self.url = url
        self.css = css
        self.disabled = disabled
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.width = width
        self.circle = circle
        self.color = color
        self.full = full
        self.icon = icon
        self.loading = loading
        self.size = size
        self.view = view

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ButtonConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'text': self.text,
            'submit': self.submit,
            'url': self.url,
            'css': self.css,
            'disabled': self.disabled,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'width': self.width,
            'circle': self.circle,
            'color': self.color,
            'full': self.full,
            'icon': self.icon,
            'loading': self.loading,
            'size': self.size,
            'view': self.view
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
