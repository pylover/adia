
[![PyPI](http://img.shields.io/pypi/v/adia.svg)](https://pypi.python.org/pypi/adia)
[![Build](https://github.com/pylover/adia/actions/workflows/build.yml/badge.svg)](https://github.com/pylover/adia/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/pylover/adia/badge.svg?branch=master)](https://coveralls.io/github/pylover/adia?branch=master)
[![Python](https://img.shields.io/badge/Python-%3E%3D3.6-blue)](https://python.org)
[![Documentation](https://img.shields.io/badge/Documentation-almost%20done-blue)](https://pylover.github.io/adia/)


# ADia
```adia
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

[ADia](https://github.com/pylover/adia) is a language specially designed to 
render ASCII diagrams.

Currently, only sequence diagrams are supported, but the roadmap is to support 
two more types of diagrams: `fork` and `class`,  check out the `TODO.md` to 
figure out what I talking about.

The ADia can also run flawlessly inside the browsers using the awesome 
project: [Brython](https://github.com/brython-dev/brython). 

See the [documentation](https://pylover.github.io/adia/) for more info.
