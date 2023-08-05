# Hello World

This is an example project demonstrating how to publish a python module to PyPI

## Installation

Run the following to install:

```python
pip install mygpio
```

## Usage

```python
from mygpio import set_on

# Switch on pin 5
set_on(5)

```
## Developing Hello World

To install helloworld, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```