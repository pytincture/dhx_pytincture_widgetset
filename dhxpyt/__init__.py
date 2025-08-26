"""
# DHX PyTincture WASM Based Widgetset

<img src="tincture.jpeg" alt="DHX PyTincture Widgetset Logo" width="400" style="display: block; margin: 0 auto;">

## Overview

The DHX PyTincture Widgetset is a Python library that integrates DHTMLX JavaScript UI components with the pyTincture framework using Pyodide. It enables building interactive, browser-based user interfaces directly in Python, supporting cross-platform GUI development with rich widgets like grids, charts, and forms.

## Features

- Direct integration with DHTMLX UI components
- Pyodide-powered Python execution in the browser
- Cross-platform compatibility
- Customizable and reusable widgets
- Event handling for interactive experiences

Detailed class and API documentation is available in the sidebar.

## Installation

### Prerequisites
- Python 3.13+
- Pyodide

### Steps
1. Clone the repository:  
   ```bash
   git clone https://github.com/pytincture/dhx_pytincture_widgetset.git
   cd dhx_pytincture_widgetset;```

## QuickStart

## Windows
#### Install UV / pytincture / dhxpyt on Powershell
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
$env:Path += ";$env:USERPROFILE\.cargo\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::User)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
New-Item -ItemType Directory -Name dhxpyt_quickstart; Set-Location dhxpyt_quickstart
uv venv --python 3.13; .\.venv\Scripts\Activate.ps1
uv pip install dhxpyt pyodide-py js pytincture itsdangerous
Invoke-WebRequest -Uri https://pytincture.com/quickstart.py -OutFile quickstart.py
$env:PYTHONUTF8 = "1"
uv run quickstart.py
```

## Linux / MacOS
#### Install UV / pytincture / dhxpyt on Bash
```
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
uv --version
mkdir dhxpyt_quickstart;cd dhxpyt_quickstart
uv venv --python 3.13 && source .venv/bin/activate
uv pip install dhxpyt pyodide-py js pytincture itsdangerous
curl -O https://pytincture.com/quickstart.py
uv run quickstart.py
```

Open in Browser:
http://localhost:8070/quickstart


### Example Code
```python
import sys
from dhxpyt.layout import MainWindow, Layout, LayoutConfig, CellConfig
from dhxpyt.toolbar import ButtonConfig, ToolbarConfig
from dhxpyt.sidebar import NavItemConfig, SidebarConfig
from dhxpyt.grid import GridConfig, GridColumnConfig
from pyodide.ffi import create_proxy

# Sample data for the grid
SAMPLE_DATA = [
    {"id": 1, "name": "Item 1", "value": 100},
    {"id": 2, "name": "Item 2", "value": 200},
    {"id": 3, "name": "Item 3", "value": 300}
]

class QuickstartMain(Layout):
    layout_config = LayoutConfig(
        type="line",
        cols=[
            CellConfig(id="sidebar", width="auto"),
            CellConfig(id="content")
        ]
    )

    def load_ui(self):
        # Sidebar configuration
        sidebar_items = [
            NavItemConfig(id="hamburger", icon="mdi mdi-menu"),
            NavItemConfig(id="items", value="Items", icon="mdi mdi-view-list")
        ]
        sidebar_config = SidebarConfig(data=sidebar_items, collapsed=False)
        self.sidebar = self.add_sidebar(id="sidebar", sidebar_config=sidebar_config)
        self.sidebar.on_click(create_proxy(self.handle_sidebar_click))

        # Content layout with toolbar and grid
        content_layout_config = LayoutConfig(
            type="line",
            rows=[
                CellConfig(id="toolbar", height="auto"),
                CellConfig(id="grid")
            ]
        )
        self.content_layout = self.add_layout("content", content_layout_config)

        # Toolbar configuration
        toolbar_config = ToolbarConfig(data=[
            ButtonConfig(id="add", value="Add Item", icon="mdi mdi-plus"),
            ButtonConfig(id="refresh", value="Refresh", icon="mdi mdi-refresh")
        ])
        self.toolbar = self.content_layout.add_toolbar(id="toolbar", toolbar_config=toolbar_config)

        # Grid configuration
        grid_columns = [
            GridColumnConfig(id="id", width=100, header=[{"text": "ID"}]),
            GridColumnConfig(id="name", width=200, header=[{"text": "Name"}]),
            GridColumnConfig(id="value", width=150, header=[{"text": "Value"}])
        ]
        grid_config = GridConfig(columns=grid_columns, data=SAMPLE_DATA)
        self.grid = self.content_layout.add_grid(id="grid", grid_config=grid_config)

    def handle_sidebar_click(self, id, event):
        if id == "hamburger":
            self.sidebar.toggle()

class QuickstartApp(MainWindow):
    def load_ui(self):
        self.set_theme("dark")
        self.main_layout = QuickstartMain(parent=self)
        self.attach("mainwindow", self.main_layout.layout)

if __name__ == "__main__" and sys.platform != "emscripten":
    from pytincture import launch_service
    launch_service()

```
"""

__widgetset__ = "dhxpyt"
__version__ = "0.8.5"
__version_tuple__ = tuple(map(int, __version__.split('.')))
__description__ = "Python wrapper for DHTMLX widgets"
