from typing import List, Union, Dict, Any


def process_item(item):
    if isinstance(item, dict):
        if 'cols' in item:
            item['cols'] = [process_item(col) for col in item['cols']]
        if 'rows' in item:
            item['rows'] = [process_item(row) for row in item['rows']]
    elif hasattr(item, 'to_dict'):
        return item.to_dict()
    return item

class FormConfig:
    """
    Configuration class for Form.
    """
    def __init__(self,
                 align: str = "start",
                 cols: List[Dict[str, Any]] = None,
                 css: str = None,
                 disabled: bool = False,
                 height: Union[str, int] = "content",
                 hidden: bool = False,
                 padding: Union[str, int] = None,
                 rows: List[Dict[str, Any]] = None,
                 title: str = None,
                 width: Union[str, int] = "content"):
        """
        :param align: (Optional) Sets the alignment of controls inside the control group.
        :param cols: (Optional) Arranges controls inside the control group horizontally.
        :param css: (Optional) The name of a CSS class(es) applied to the control group.
        :param disabled: (Optional) Makes a form disabled.
        :param height: (Optional) Sets the height of the control group.
        :param hidden: (Optional) Defines whether a form is hidden.
        :param padding: (Optional) Sets padding for content inside the control group.
        :param rows: (Optional) Arranges controls inside the control group vertically.
        :param title: (Optional) Specifies the title of the control group.
        :param width: (Optional) Sets the width of the control group.
        """
        self.align = align
        self.cols = cols if cols else []
        self.css = css
        self.disabled = disabled
        self.height = height
        self.hidden = hidden
        self.padding = padding
        self.rows = rows if rows else []
        self.title = title
        self.width = width

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the FormConfig into a dictionary format that can be
        passed into the form constructor.
        """
        config_dict = {
            'align': self.align,
            'cols': self.cols,
            'css': self.css,
            'disabled': self.disabled,
            'height': self.height,
            'hidden': self.hidden,
            'padding': self.padding,
            'rows': self.rows,
            'title': self.title,
            'width': self.width
        }

        if 'cols' in config_dict:
            config_dict['cols'] = [process_item(col) for col in config_dict['cols']]
        if 'rows' in config_dict:
            config_dict['rows'] = [process_item(row) for row in config_dict['rows']]

            
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}

