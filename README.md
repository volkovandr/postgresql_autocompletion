# PostgreSQL autocompletion
Enables autocompletion when writing SQL queries.

# Overview

# Features

# Installation
cd to the folder where Sublime packages are installed and clone this repository there

# Configuration

# Usage

# Testing
You don't need Sublime to run the tests. There are mocking modules
* sublime_moker
* sublime_plugin_mocker

The plugin tries to load the real Sublime modules and if that fails it will load the
mockers.

To run the tests execute this from the root folder of the project:
```
python -m unittest discover -v -s unit_test -p *_test.py
```

