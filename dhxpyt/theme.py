import json
from typing import Any, Dict, Optional, Union

import js


def _apply_css_vars(css_vars: Optional[Dict[str, Dict[str, Any]]]) -> None:
    """
    Apply scoped CSS custom properties via the frontend helper if available.
    The mapping should be {"selector": {"--var": "value", ...}, ...}.
    """
    if not css_vars:
        return

    try:
        helper = getattr(js.customdhx, "applyCssVars", None)
    except Exception:
        helper = None

    if helper:
        helper(js.JSON.parse(json.dumps(css_vars)))


def apply_theme(theme: Union[str, Dict[str, Any], None], css_vars: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
    """
    Apply a global DHTMLX theme and optional scoped CSS variable overrides.

    - theme: string name or dict payload accepted by dhx.setTheme; pass None to only set CSS vars
    - css_vars: mapping of selectors to {css_var: value} for fine-grained overrides
    """
    if theme is not None:
        if isinstance(theme, dict):
            js.dhx.setTheme(js.JSON.parse(json.dumps(theme)))
        elif isinstance(theme, str):
            js.dhx.setTheme(theme)
        else:
            raise TypeError(f"Unsupported theme type: {type(theme)!r}")

    _apply_css_vars(css_vars)


def set_theme(theme: Union[str, Dict[str, Any], None], css_vars: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
    """Alias for apply_theme."""
    apply_theme(theme, css_vars)
