# myosutils Library

This is an example project demonstrating how to publish a python module to PyPI

## Installation

Run the following to install:

```python
pip install myosutils
```

## Usage

```python
from myosutils import raw_mode

with raw_mode(sys.stdin):
	...

```
## Developing Hello World

To install helloworld, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```