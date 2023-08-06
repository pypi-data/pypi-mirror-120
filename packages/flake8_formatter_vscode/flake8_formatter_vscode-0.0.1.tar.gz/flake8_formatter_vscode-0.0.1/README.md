# flake8-formatter-vscode

[![pypi][pypi-badge]](https://pypi.org/project/flake8-formatter-vscode/)
[![black][black-badge]](https://github.com/psf/black)

[pypi-badge]: https://badgen.net/pypi/v/flake8-formatter-vscode
[black-badge]: https://badgen.net/badge/code%20style/black/black/

## Installation

Install from `pip` with:

`pip install flake8-formatter-vscode` or `pip install --user flake8-formatter-vscode`

## Usage

To activate this formatter one will need to run:

flake8 --format=vscode your_module.py

Or set the configuration option inside `setup.cfg` or `.flake8` or `~/.config/flake8` file:

[flake8]
format = vscode
