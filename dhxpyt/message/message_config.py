from typing import Any, Dict


class MessageConfig:
    """
    Configuration class for the Message widget.
    """
    def __init__(self,
                 text: str = None,
                 icon: str = None,
                 css: str = None,
                 html: str = None,
                 node: Any = None,  # Could be an element or its id
                 position: str = "top-right",
                 expire: int = None):
        """
        Initializes the MessageConfig.

        :param text: (Optional) The text of the message box.
        :param icon: (Optional) An icon from the used icon font.
        :param css: (Optional) The style of the message box.
        :param html: (Optional) The HTML content to be displayed in the message box.
        :param node: (Optional) The container for the message box or its id.
        :param position: (Optional) The position of the message box.
        :param expire: (Optional) The time period of displaying the message box before it disappears, in milliseconds.
        """
        self.text = text
        self.icon = icon
        self.css = css
        self.html = html
        self.node = node
        self.position = position
        self.expire = expire

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the MessageConfig into a dictionary format.
        """
        config_dict = {
            'text': self.text,
            'icon': self.icon,
            'css': self.css,
            'html': self.html,
            'node': self.node,
            'position': self.position,
            'expire': self.expire
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
