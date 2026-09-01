# DHX PyTincture Widgetset

## Overview
The **DHX PyTincture Widgetset** is a Python-based library that integrates the [DHTMLX JavaScript UI components](https://dhtmlx.com/) with the [pyTincture framework](https://github.com/schapman1974/pyTincture). Leveraging Pyodide, this widgetset enables developers to create rich, interactive web-based user interfaces using Python. It simplifies the process of building cross-platform GUI applications by combining DHTMLX's powerful UI components with pyTincture's seamless Pyodide integration.

## Features
- **DHTMLX Integration**: Utilize DHTMLX's extensive suite of UI components (e.g., grids, charts, forms, and schedulers) within Python applications.
- **Pyodide-Powered**: Run Python code in the browser with Pyodide, enabling dynamic frontend development without leaving the Python ecosystem.
- **Cross-Platform**: Build applications that work across various platforms where Pyodide is supported.
- **Customizable Widgets**: Easily create and manage reusable UI components tailored to your application's needs.
- **Event-Driven**: Support for event handling to create responsive and interactive user experiences.
- **AI Chat Widget**: Stream Markdown-rendered assistant responses, surface artifacts in a live preview pane, and react to dark/light theme changes without leaving Python.

## Browser content safety

Widget data is text by default. `htmlEnable=True`, CardPanel `contentHtml` / `iconHtml`,
and HTML-returning CardPanel templates are explicit rich-content paths; their output is
sanitized to a small formatting allowlist before it reaches the DOM. Grid, Listbox, and
Combobox `htmlEnable` now default to `False`. Applications that previously relied on
event attributes, scripts, inline styles, SVG, images, or other active markup inside
those values must replace that markup with trusted application code and DOM event
handlers.

Chat assistant Markdown never accepts raw HTML. HTML artifacts run only inside an
opaque-origin sandbox with network, forms, popups, workers, and parent DOM access
blocked. SVG artifacts are passive images, and Python artifacts are displayed as code
rather than executed. This may change applications that previously depended on active
SVG, in-page network calls, same-origin access, or automatic execution of model-supplied
Python.

Chat histories are bounded to 100 messages per chat and 20 chats by default.
Content persistence is off unless an existing explicit `storage_key` is used
or `persistence="local"` / `"session"` is selected. Persisted history omits
tool payloads, metadata, artifacts, and preview-console output and is capped at
2 MiB by default. Set `persistence=False` to remove earlier history under an
explicit storage key. Artifact preview logs are source/capability bound and
bounded, and they are excluded from send/model event payloads unless
`include_artifact_console_in_send=True` is deliberately configured; included
logs are marked untrusted.

## Installation
### Prerequisites
- Python 3.13+

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
