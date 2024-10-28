from typing import Union, Dict, Any, Callable, List

from pyodide.ffi import create_proxy


class SimpleVaultConfig:
    """
    Configuration class for the SimpleVault control.
    """
    def __init__(self,
                 name: str = None,
                 id: str = None,
                 target: str = None,
                 value: List[Dict[str, Any]] = None,
                 css: str = None,
                 height: Union[str, int] = "content",
                 width: Union[str, int] = "content",
                 padding: Union[str, int] = "5px",
                 hidden: bool = False,
                 disabled: bool = False,
                 fieldName: str = "file",
                 params: Dict[str, Any] = None,
                 headerParams: Dict[str, Any] = None,
                 singleRequest: bool = False,
                 updateFromResponse: bool = True,
                 autosend: bool = False,
                 accept: str = None,
                 validation: Callable[[Any], bool] = None,
                 required: bool = False,
                 hiddenLabel: bool = False,
                 label: str = None,
                 labelPosition: str = "top",
                 labelWidth: Union[str, int] = None,
                 helpMessage: str = None,
                 preMessage: str = None,
                 successMessage: str = None,
                 errorMessage: str = None):
        """
        Initializes the SimpleVaultConfig.

        :param name: (Optional) The name of the control.
        :param id: (Optional) The id of the control.
        :param target: (Optional) URL to the server-side script that will process file upload.
        :param value: (Optional) The default list of loaded files.
        :param css: (Optional) Adds style classes to the control.
        :param height: (Optional) The height of the control.
        :param width: (Optional) The width of the control.
        :param padding: (Optional) Sets padding between the cell and border.
        :param hidden: (Optional) Whether the control is hidden.
        :param disabled: (Optional) Whether the control is disabled.
        :param fieldName: (Optional) Name of the file field in the form data.
        :param params: (Optional) Extra parameters for sending XMLHttpRequest.
        :param headerParams: (Optional) Additional parameters for Request Headers.
        :param singleRequest: (Optional) Whether files are sent in one request.
        :param updateFromResponse: (Optional) Updates file attributes from server response.
        :param autosend: (Optional) Enables automatic sending of an added file.
        :param accept: (Optional) Specifies the type/extension displayed in the dialog.
        :param validation: (Optional) The validation function.
        :param required: (Optional) Whether the control is required.
        :param hiddenLabel: (Optional) Makes the label invisible.
        :param label: (Optional) Specifies a label for the control.
        :param labelPosition: (Optional) Position of the label.
        :param labelWidth: (Optional) Width of the label.
        :param helpMessage: (Optional) Adds a help message to the control.
        :param preMessage: (Optional) Instructions for interacting with the control.
        :param successMessage: (Optional) Message after successful validation.
        :param errorMessage: (Optional) Message after validation error.
        """
        self.type = "simpleVault"
        self.name = name
        self.id = id
        self.target = target
        self.value = value
        self.css = css
        self.height = height
        self.width = width
        self.padding = padding
        self.hidden = hidden
        self.disabled = disabled
        self.fieldName = fieldName
        self.params = params
        self.headerParams = headerParams
        self.singleRequest = singleRequest
        self.updateFromResponse = updateFromResponse
        self.autosend = autosend
        self.accept = accept
        self.validation = validation
        self.required = required
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
        Converts the SimpleVaultConfig into a dictionary format.
        """
        config_dict = {
            'type': self.type,
            'name': self.name,
            'id': self.id,
            'target': self.target,
            'value': self.value,
            'css': self.css,
            'height': self.height,
            'width': self.width,
            'padding': self.padding,
            'hidden': self.hidden,
            'disabled': self.disabled,
            'fieldName': self.fieldName,
            'params': self.params,
            'headerParams': self.headerParams,
            'singleRequest': self.singleRequest,
            'updateFromResponse': self.updateFromResponse,
            'autosend': self.autosend,
            'accept': self.accept,
            'validation': self.validation,
            'required': self.required,
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

        # Handle validation function
        if 'validation' in config_dict and callable(config_dict['validation']):
            config_dict['validation'] = create_proxy(self.validation)

        return config_dict
