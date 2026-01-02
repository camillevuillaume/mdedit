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
First of all, create a Python virtual environment to install dependencies.
```
python3 -m venv .venv
```
If necessary, activate the venv:
```
source ".venv/bin/activate"
```
And then, if necessary install the requirements and the app.
```
pip install .
```
Now you can run the program with the command `mdedit`.

## Testing

Unit tests can be execute with `pytest`.
