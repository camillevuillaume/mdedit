# MDedit

Simple Markdown file editor using Python PyWebView and EasyMDE.
Local file handling is supported.

## Features

- Typical markdown edit features, including preview via EasyMDE
- Open / save files locally
- Date picker using a custom `\date` command

## Installation

The following packages are needed:
- python3
- pip3
- npm
Although it should be possible to install requirements via pip, I had no luck with GTK or QT (Pyside6) in a python virtual environment.
As a consequence, you will also need to install PyWebview, and create a Python virtual environment in the project folder as follows:
```
python3 -m venv --system-site-packages .venv
```
If necessary, activate the venv:
```
source ".venv/bin/activate"
```
This will install requirements on both python and npm side.
Now you can run the program with the command `mdedit`.

## Testing

Unit tests can be execute with `pytest`.
