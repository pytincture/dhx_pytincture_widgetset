"""
# DHX PyTincture WASM Based Widgetset
"""

__widgetset__ = "dhxpyt"
__version__ = "0.9.13"
__version_tuple__ = tuple(map(int, __version__.split('.')))
__description__ = "Python wrapper for DHTMLX widgets"

# Optional WebGPU bridge helpers (Pyodide environments only)
try:  # pragma: no cover - availability depends on runtime
    from .gpu import enable_webgpu, webgpu_status  # noqa: F401
except Exception:
    # In non-Pyodide or headless environments, the helpers are unavailable.
    pass
