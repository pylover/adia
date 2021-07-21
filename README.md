[![Build](https://github.com/dobisel/dial/actions/workflows/build.yml/badge.svg)](https://github.com/dobisel/dial/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/dobisel/dial/badge.svg?branch=master)](https://coveralls.io/github/dobisel/dial?branch=master)

# dial
ASCII diagram language.

```dial
diagram: Foo

sequence:
foo -> bar: Hello World!
```

Output: 

```
 DIAGRAM: Foo                             

 +-----+             +-----+
 | foo |             | bar |
 +-----+             +-----+
    |                   |
    |~~~Hello World!~~~>|
    |                   |
    |<------------------|
    |                   |
 +-----+             +-----+
 | foo |             | bar |
 +-----+             +-----+
```

## Quickstart

```python
from dial import Diagram

diagram = Diagram('''
  diagram: Foo
  
  sequence:
  foo -> bar: Hello World!
''')

print(diagram.renders())
```

## Setup development environment

Use your favorite virtual environment tool such as 
https://pypi.org/project/virtualenvwrapper/.

Then:

```bash
make env
```

### Running tests

#### CPython Tests

```bash
make test
```

#### CPython Coverage

```bash
make cover
```

#### Brython Tests

```bash
make clean serve
```

Then open the browser and point http://localhost:8000/check.html to run tests.

### Web interface

The `dial` package should be compatible with the `Brython` too. So, you can 
use it on every browser which supports ECMA6.

To build and check the demo, run:

```bash
make clean
make www
make serve
```

Or just one line to do all the above commands in order:

```bash
make clean serve
```

then open http://localhost:8000 in your favorite browser to use `dial` wihtout
the `CPython`.

Isn't that nice?
