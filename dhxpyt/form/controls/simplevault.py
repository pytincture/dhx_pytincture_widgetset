"""
SimpleVault control implementation for the Form widget
"""

from typing import Any, Callable, Dict, Union, List
import json
from pyodide.ffi import create_proxy
import js

from .simplevault_config import SimpleVaultConfig


class SimpleVault:
    def __init__(self, config: SimpleVaultConfig = None, widget_parent: Any = None):
        """Initializes the SimpleVault control."""
        if config is None:
            config = SimpleVaultConfig()
        config_dict = config.to_dict()
        self.simplevault = js.dhx.FormControl.new(widget_parent, js.JSON.parse(json.dumps(config_dict)))

    """ SimpleVault API Functions """

    def blur(self) -> None:
        """Removes focus from the SimpleVault control."""
        self.simplevault.blur()

    def clear(self) -> None:
        """Clears the value of the SimpleVault control."""
        self.simplevault.clear()

    def clear_validate(self) -> None:
        """Clears validation of the SimpleVault control."""
        self.simplevault.clearValidate()

    def destructor(self) -> None:
        """Removes the SimpleVault instance and releases the occupied resources."""
        self.simplevault.destructor()

    def disable(self) -> None:
        """Disables the SimpleVault control."""
        self.simplevault.disable()

    def enable(self) -> None:
        """Enables the SimpleVault control."""
        self.simplevault.enable()

    def focus(self) -> None:
        """Sets focus to the SimpleVault control."""
        self.simplevault.focus()

    def get_properties(self) -> Dict[str, Any]:
        """Returns the configuration attributes of the control."""
        return self.simplevault.getProperties().to_py()

    def get_value(self) -> List[Dict[str, Any]]:
        """Returns the current value of the SimpleVault control."""
        value = self.simplevault.getValue()
        return [item.to_py() for item in value]

    def hide(self) -> None:
        """Hides the SimpleVault control."""
        self.simplevault.hide()

    def is_disabled(self) -> bool:
        """Checks whether the SimpleVault control is disabled."""
        return self.simplevault.isDisabled()

    def is_visible(self) -> bool:
        """Checks whether the SimpleVault control is visible on the page."""
        return self.simplevault.isVisible()

    def select_file(self) -> None:
        """Opens the dialog for selecting new files for adding to the SimpleVault."""
        self.simplevault.selectFile()

    def send(self, params: Dict[str, Any] = None) -> None:
        """Sends a POST request for file upload to a server-side URL."""
        self.simplevault.send(params)

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """Allows changing configuration attributes of the control dynamically."""
        self.simplevault.setProperties(js.JSON.parse(json.dumps(properties)))

    def set_value(self, value: List[Dict[str, Any]]) -> None:
        """Sets the value for the SimpleVault control."""
        self.simplevault.setValue(js.JSON.parse(json.dumps(value)))

    def show(self) -> None:
        """Shows the SimpleVault control on the page."""
        self.simplevault.show()

    def validate(self, silent: bool = False, validate_value: List[Dict[str, Any]] = None) -> bool:
        """Validates the SimpleVault control."""
        return self.simplevault.validate(silent, validate_value)

    """ SimpleVault Events """

    def add_event_handler(self, event_name: str, handler: Callable) -> None:
        """Helper to add event handlers dynamically."""
        event_proxy = create_proxy(handler)
        self.simplevault.events.on(event_name, event_proxy)

    def on_after_add(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after a file is added to the data collection."""
        self.add_event_handler('afterAdd', handler)

    def on_after_change_properties(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after configuration attributes have been changed dynamically."""
        self.add_event_handler('afterChangeProperties', handler)

    def on_after_hide(self, handler: Callable[[List[Dict[str, Any]], bool], None]) -> None:
        """Fires after the control is hidden."""
        self.add_event_handler('afterHide', handler)

    def on_after_remove(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Fires after a file is removed from the data collection."""
        self.add_event_handler('afterRemove', handler)

    def on_after_show(self, handler: Callable[[List[Dict[str, Any]]], None]) -> None:
        """Fires after the control is shown."""
        self.add_event_handler('afterShow', handler)

    def on_after_validate(self, handler: Callable[[List[Dict[str, Any]], bool], None]) -> None:
        """Fires after the control value is validated."""
        self.add_event_handler('afterValidate', handler)

    def on_before_add(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before a file is added to the data collection."""
        def event_handler(file):
            result = handler(file.to_py())
            if result is False:
                return js.Boolean(False)
        self.simplevault.events.on('beforeAdd', create_proxy(event_handler))

    def on_before_change(self, handler: Callable[[List[Dict[str, Any]], Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before changing the value of the control."""
        def event_handler(value, file=None):
            value_py = [item.to_py() for item in value]
            file_py = file.to_py() if file else None
            result = handler(value_py, file_py)
            if result is False:
                return js.Boolean(False)
        self.simplevault.events.on('beforeChange', create_proxy(event_handler))

    def on_before_change_properties(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before configuration attributes are changed dynamically."""
        def event_handler(properties):
            result = handler(properties.to_py())
            if result is False:
                return js.Boolean(False)
        self.simplevault.events.on('beforeChangeProperties', create_proxy(event_handler))

    def on_before_hide(self, handler: Callable[[List[Dict[str, Any]], bool], Union[bool, None]]) -> None:
        """Fires before the control is hidden."""
        def event_handler(value, init):
            value_py = [item.to_py() for item in value]
            result = handler(value_py, init)
            if result is False:
                return js.Boolean(False)
        self.simplevault.events.on('beforeHide', create_proxy(event_handler))

    def on_before_remove(self, handler: Callable[[Dict[str, Any]], Union[bool, None]]) -> None:
        """Fires before a file is removed from the data collection."""
        def event_handler(file):
            result = handler(file.to_py())
            if result is False:
                return js.Boolean(False)
        self.simplevault.events.on('beforeRemove', create_proxy(event_handler))

    def on_before_show(self, handler: Callable[[List[Dict[str, Any]]], Union[bool, None]]) -> None:
        """Fires before the control is shown."""
        def event_handler(value):
            value_py = [item.to_py() for item in value]
            result = handler(value_py)
            if result is False:
                return js.Boolean(False)
        self.simplevault.events.on('beforeShow', create_proxy(event_handler))

    def on_before_upload_file(self, handler: Callable[[Dict[str, Any], List[Dict[str, Any]]], Union[bool, None]]) -> None:
        """Fires before file upload begins."""
        def event_handler(file, value):
            file_py = file.to_py()
            value_py = [item.to_py() for item in value]
            result = handler(file_py, value_py)
            if result is False:
                return js.Boolean(False)
        self.simplevault.events.on('beforeUploadFile', create_proxy(event_handler))

    def on_before_validate(self, handler: Callable[[List[Dict[str, Any]]], Union[bool, None]]) -> None:
        """Fires before the control value is validated."""
        def event_handler(value):
            value_py = [item.to_py() for item in value]
            result = handler(value_py)
            if result is False:
                return js.Boolean(False)
        self.simplevault.events.on('beforeValidate', create_proxy(event_handler))

    def on_change(self, handler: Callable[[List[Dict[str, Any]]], None]) -> None:
        """Fires on changing the value of the control."""
        self.add_event_handler('change', handler)

    def on_upload_begin(self, handler: Callable[[List[Dict[str, Any]], List[Dict[str, Any]]], None]) -> None:
        """Fires when file upload begins."""
        self.add_event_handler('uploadBegin', handler)

    def on_upload_complete(self, handler: Callable[[List[Dict[str, Any]], List[Dict[str, Any]]], None]) -> None:
        """Fires when upload is completed."""
        self.add_event_handler('uploadComplete', handler)

    def on_upload_fail(self, handler: Callable[[Dict[str, Any], List[Dict[str, Any]]], None]) -> None:
        """Fires if the file upload failed."""
        self.add_event_handler('uploadFail', handler)

    def on_upload_file(self, handler: Callable[[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]], None]) -> None:
        """Fires when a file has been uploaded."""
        self.add_event_handler('uploadFile', handler)

    def on_upload_progress(self, handler: Callable[[int, List[Dict[str, Any]]], None]) -> None:
        """Fires on each percent of files uploading."""
        self.add_event_handler('uploadProgress', handler)
