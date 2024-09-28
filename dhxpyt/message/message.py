"""
Message widget implementation
"""

from typing import Any
import json
from pyodide.ffi import create_proxy
import js

from .message_config import MessageConfig


class Message:
    def __init__(self, config: MessageConfig = None):
        """
        Initializes and displays the Message widget.

        :param config: (Optional) The MessageConfig object containing the message configuration.
        """
        if config is None:
            config = MessageConfig()
        config_dict = config.to_dict()
        # Display the message and store the returned message instance
        self.message = js.dhx.message(None, js.JSON.parse(json.dumps(config_dict)))

    def close(self) -> None:
        """Closes the message box."""
        self.message.close()
