"""
pyTincture Avatar control implementation
"""

from typing import Any, Callable, Dict, List, Union
import json
from pyodide.ffi import create_proxy
import js

from .avatar_config import AvatarConfig


class Avatar:
    def __init__(self, config: AvatarConfig = None, widget_parent: Any = None):
        """Initializes the Avatar control."""
        if config is None:
            config = AvatarConfig()
        config_dict = config.to_dict()
        self.avatar = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ Avatar API Functions """

    def blur(self) -> None:
        """Removes focus from the control."""
        self.avatar.blur()

    def clear(self) -> None:
        """Clears the value of the Avatar control."""
        self.avatar.clear()

    def clear_validate(self) -> None:
        """Clears validation of the Avatar control."""
        self.avatar.clearValidate()

    def destructor(self) -> None:
        """Removes the Avatar instance and releases the occupied resources."""
        self.avatar.destructor()

    def disable(self) -> None:
        """Disables the Avatar control."""
        self.avatar.disable()

    def enable(self) -> None:
        """Enables the Avatar control."""
        self.avatar.enable()

    def focus(self) -> None:
        """Sets focus to the control."""
        self.avatar.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns an object with the available configuration attributes of the control."""
        return self.avatar.getProperties().to_py()

    def get_value(self) -> Dict[str, Any]:
        """Returns the current value of the Avatar control."""
        return self.avatar.getValue().to_py()

    def hide(self) -> None:
        """Hides the Avatar control."""
        self.avatar.hide()

    def is_disabled(self) -> bool:
        """Checks whether the Avatar control is disabled."""
        return self.avatar.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the Avatar control is visible on the page."""
        return self.avatar.isVisible()

    def select_file(self) -> None:
        """Opens the dialog for selecting an image."""
        self.avatar.selectFile()

    def send(self, params: Dict[str, Any] = None) -> None:
        """Sends a POST request for a file upload to a server-side URL."""
        self.avatar.send(js.JSON.parse(json.dumps(params or {})))

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing available configuration attributes of the control dynamically."""
        self.avatar.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: Dict[str, Any]) -> None:
        """Sets the value for the Avatar control."""
        self.avatar.setValue(js.JSON.parse(json.dumps(value)))

    def show(self) -> None:
        """Shows the Avatar control on the page."""
        self.avatar.show()

    def validate(self, silent: bool = False, validate_value: Dict[str, Any] = None) -> bool:
        """Validates the Avatar control."""
        return self.avatar.validate(silent, js.JSON.parse(json.dumps(validate_value or {})))

    """ Avatar Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.avatar.events.on(event_name, event_proxy)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[Dict[str, Any], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_show(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[Dict[str, Any], bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_change(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.avatar.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.avatar.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[Dict[str, Any], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            result = handler(value.to_py(), init)
            if result is False:
                return js.Boolean(False)
        self.avatar.events.on('beforeHide', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.avatar.events.on('beforeShow', create_proxy(event_handler))

    def on_before_upload_file(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before file upload begins."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.avatar.events.on('beforeUploadFile', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            result = handler(value.to_py())
            if result is False:
                return js.Boolean(False)
        self.avatar.events.on('beforeValidate', create_proxy(event_handler))

    def on_blur(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires when the control has lost focus."""
        self.add_event_handler('blur', handler)

    def on_change(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_focus(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires when the control has received focus."""
        self.add_event_handler('focus', handler)

    def on_keydown(self, handler: Callable[[Any], None]) -> None:
        """Fires when any key is pressed and the control is in focus."""
        self.add_event_handler('keydown', handler)

    def on_upload_begin(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires when file upload begins."""
        self.add_event_handler('uploadBegin', handler)

    def on_upload_complete(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires when upload is completed."""
        self.add_event_handler('uploadComplete', handler)

    def on_upload_fail(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires if the file upload failed."""
        self.add_event_handler('uploadFail', handler)

    def on_upload_file(self, handler: Callable[[Dict[str, Any], Dict[str, Any]], None]) -> None:
        """Fires when a file has been uploaded."""
        self.add_event_handler('uploadFile', handler)

    def on_upload_progress(self, handler: Callable[[int, Dict[str, Any]], None]) -> None:
        """Fires on each percent of a file uploading."""
        self.add_event_handler('uploadProgress', handler)
