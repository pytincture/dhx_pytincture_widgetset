"""
# DHX PyTincture Widgetset

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
"""

__widgetset__ = "dhxpyt"
__version__ = "0.8.1"
__version_tuple__ = tuple(map(int, __version__.split('.')))
__description__ = "Python wrapper for DHTMLX widgets"
