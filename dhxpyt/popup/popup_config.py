from typing import Any, Dict



class PopupConfig:
    """
    Configuration class for the Popup widget.
    """
    def __init__(self,
                 css: str = None):
        """
        Initializes the PopupConfig.

        :param css: (Optional) Adds style classes for the component.
        """
        self.css = css

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the PopupConfig into a dictionary format.
        """
        config_dict = {
            'css': self.css
        }
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}


class PopupShowConfig:
    """
    Configuration class for the 'show' method of the Popup widget.
    """
    def __init__(self,
                 centering: bool = True,
                 auto: bool = False,
                 mode: str = "bottom",
                 indent: int = 0):
        """
        Initializes the PopupShowConfig.

        :param centering: (Optional) Whether to center the popup relative to the element.
        :param auto: (Optional) Enables autopositioning of the popup.
        :param mode: (Optional) The position relative to the element to show the popup at.
        :param indent: (Optional) The offset of the popup relative to the element.
        """
        self.centering = centering
        self.auto = auto
        self.mode = mode
        self.indent = indent

    def to_dict(self) -> Dict[str, Any]:
        config_dict = {
            'centering': self.centering,
            'auto': self.auto,
            'mode': self.mode,
            'indent': self.indent,
        }
        return config_dict
