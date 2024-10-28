from typing import Union, Dict, Any, Callable
from pyodide.ffi import create_proxy


class AvatarConfig:
    """
    Configuration class for the Avatar control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 target: str = None,
                 value: Dict[str, Any] = None,
                 hidden: bool = False,
                 disabled: bool = False,
                 readOnly: bool = False,
                 removeIcon: bool = True,
                 circle: bool = False,
                 icon: str = None,
                 placeholder: str = None,
                 preview: str = None,
                 alt: str = None,
                 size: Union[str, int] = "medium",
                 css: str = None,
                 width: Union[str, int] = "content",
                 height: Union[str, int] = "content",
                 padding: Union[str, int] = "5px",
                 label: str = None,
                 labelWidth: Union[str, int] = None,
                 labelPosition: str = "top",
                 hiddenLabel: bool = False,
                 helpMessage: str = None,
                 required: bool = False,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None,
                 validation: Callable[[Any], bool] = None,
                 accept: str = "image/*",
                 fieldName: str = "file",
                 autosend: bool = False,
                 params: Dict[str, Any] = None,
                 headerParams: Dict[str, Any] = None,
                 updateFromResponse: bool = True):
        """
        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param target: (Optional) The URL to the server-side script for file upload.
        :param value: (Optional) The initial value of the Avatar control.
        :param hidden: (Optional) Whether the control is hidden.
        :param disabled: (Optional) Whether the control is disabled.
        :param readOnly: (Optional) Sets the readonly mode for the control.
        :param removeIcon: (Optional) Enables the possibility to clear the control via UI.
        :param circle: (Optional) Sets the mode of displaying the control with rounded corners.
        :param icon: (Optional) The CSS class of an icon when there is no image uploaded.
        :param placeholder: (Optional) The text visible when there is no image uploaded.
        :param preview: (Optional) Specifies the absolute path to the preview image.
        :param alt: (Optional) Sets the 'alt' attribute of the <img> tag.
        :param size: (Optional) The size of the control.
        :param css: (Optional) Adds style classes to the control.
        :param width: (Optional) The width of the control.
        :param height: (Optional) The height of the control.
        :param padding: (Optional) Sets padding between the cell and border.
        :param label: (Optional) Specifies a label for the control.
        :param labelWidth: (Optional) Sets the label width of the control.
        :param labelPosition: (Optional) Defines the position of the label.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param required: (Optional) Defines whether the control is required.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message shown after successful validation.
        :param errorMessage: (Optional) Message shown after validation error.
        :param validation: (Optional) The validation function.
        :param accept: (Optional) Specifies the type/extension of the selected file.
        :param fieldName: (Optional) Sets the file field name in the form data.
        :param autosend: (Optional) Enables/disables automatic sending of an added file.
        :param params: (Optional) Extra parameters for sending an XMLHttpRequest.
        :param headerParams: (Optional) Additional parameters for Request Headers.
        :param updateFromResponse: (Optional) Updates file attributes with server response data.
        """
        self.type = "avatar"
        self.name = name
        self.id = id
        self.target = target
        self.value = value
        self.hidden = hidden
        self.disabled = disabled
        self.readOnly = readOnly
        self.removeIcon = removeIcon
        self.circle = circle
        self.icon = icon
        self.placeholder = placeholder
        self.preview = preview
        self.alt = alt
        self.size = size
        self.css = css
        self.width = width
        self.height = height
        self.padding = padding
        self.label = label
        self.labelWidth = labelWidth
        self.labelPosition = labelPosition
        self.hiddenLabel = hiddenLabel
        self.helpMessage = helpMessage
        self.required = required
        self.preMessage = preMessage
        self.successMessage = successMessage
        self.errorMessage = errorMessage
        self.validation = validation
        self.accept = accept
        self.fieldName = fieldName
        self.autosend = autosend
        self.params = params
        self.headerParams = headerParams
        self.updateFromResponse = updateFromResponse

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the AvatarConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'target': self.target,
            'value': self.value,
            'hidden': self.hidden,
            'disabled': self.disabled,
            'readOnly': self.readOnly,
            'removeIcon': self.removeIcon,
            'circle': self.circle,
            'icon': self.icon,
            'placeholder': self.placeholder,
            'preview': self.preview,
            'alt': self.alt,
            'size': self.size,
            'css': self.css,
            'width': self.width,
            'height': self.height,
            'padding': self.padding,
            'label': self.label,
            'labelWidth': self.labelWidth,
            'labelPosition': self.labelPosition,
            'hiddenLabel': self.hiddenLabel,
            'helpMessage': self.helpMessage,
            'required': self.required,
            'preMessage': self.preMessage,
            'successMessage': self.successMessage,
            'errorMessage': self.errorMessage,
            'validation': self.validation,
            'accept': self.accept,
            'fieldName': self.fieldName,
            'autosend': self.autosend,
            'params': self.params,
            'headerParams': self.headerParams,
            'updateFromResponse': self.updateFromResponse
        }
        # Remove None values
        config_dict = {k: v for k, v in config_dict.items() if v is not None}

        # Handle functions
        if 'validation' in config_dict:
            config_dict['validation'] = create_proxy(self.validation)

        return config_dict
