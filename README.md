# DHX PyTincture Widgetset

## Overview
The **DHX PyTincture Widgetset** is a Python-based library that integrates the [DHTMLX JavaScript UI components](https://dhtmlx.com/) with the [pyTincture framework](https://github.com/schapman1974/pyTincture). Leveraging Pyodide, this widgetset enables developers to create rich, interactive web-based user interfaces using Python. It simplifies the process of building cross-platform GUI applications by combining DHTMLX's powerful UI components with pyTincture's seamless Pyodide integration.

## Features
- **DHTMLX Integration**: Utilize DHTMLX's extensive suite of UI components (e.g., grids, charts, forms, and schedulers) within Python applications.
- **Pyodide-Powered**: Run Python code in the browser with Pyodide, enabling dynamic frontend development without leaving the Python ecosystem.
- **Cross-Platform**: Build applications that work across various platforms where Pyodide is supported.
- **Customizable Widgets**: Easily create and manage reusable UI components tailored to your application's needs.
- **Event-Driven**: Support for event handling to create responsive and interactive user experiences.

## Installation
### Prerequisites
- Python 3.8+
- Pyodide (configured for browser-based Python execution)
- Node.js (for local development and dependency management, optional)

### API Documenataion
https://pytincture.com/dhxpyt.html

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pytincture/dhx_pytincture_widgetset.git
   cd dhx_pytincture_widgetset
Install Dependencies: Install the required Python packages and Pyodide dependencies:
bash

pip install -r requirements.txt

or from pypi

pip install dhxpyt


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
