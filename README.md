[![Build](https://github.com/pylover/dial/actions/workflows/build.yml/badge.svg)](https://github.com/pylover/dial/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/pylover/dial/badge.svg?branch=master)](https://coveralls.io/github/pylover/dial?branch=master)

# dial
[Dial](https://github.com/pylover/dial) is a language specially designed to 
render ASCII diagrams.

Currently, only sequence diagrams are supported, but the roadmap is to support 
two more types of diagrams: `fork` and `class`,  check out the `TODO.md` to 
figure out what I talking about.

The Dial can also run flawlessly inside the browsers using the awesome 
project: [Brython](https://github.com/brython-dev/brython). check out 
the [Web Interface](https://github.com/pylover/dial#web-interface) 
section below for more info.

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


#### Update Brython runtime

Run `make cleanall` to force download and update `brython*.js` files.

```bash
make cleanall
make www
```

## Complete example

```dial
diagram: Authentication
version: 1.0
author: pylover

sequence: Login/Logout
alice.title: Alice
bob.title: Bob
db.title: Database

# Login
@alice ~ bob: Alice tries to authenticate herself
alice -> bob: authenticate(email, password) -> token
  if: db is null
    bob -> db: initialize() -> db
  elif: db.is_connected()
    bob -> db: keepalive()
  else:
    while: not db.is_connected()
      bob -> db: connect()
  
  bob -> bob: create_token() -> token
  
@alice: |
  Alice decides to 
  store the newly 
  received Token 
  in a safe place. 
alice -> alice: store(token)

# Logout
@alice ~ bob: Alice tries to logout
alice -> bob: logout(token)
  bob -> db: delete(token)
  for: each token in db
    bob -> db: delete(token)
```

Generated diagram:

```
 DIAGRAM: Authentication                                                           
 author: pylover                                                                   
 version: 1.0                                                                      
                                                                                   
 SEQUENCE: Login/Logout                                                            
                                                                                   
 +-------+                                   +-----+                 +-----------+ 
 | Alice |                                   | Bob |                 | Database  | 
 +-------+                                   +-----+                 +-----------+ 
     |                                          |                          |       
 ---------------------------------------------------                       |       
 | Alice tries to authenticate herself             |                       |       
 ---------------------------------------------------                       |       
     |                                          |                          |       
     |~~~authenticate(email, password)~~~~~~~~~>|                          |       
     |                                          |                          |       
     |                                       ************************************* 
     |                                       * if db is null                     * 
     |                                       ************************************* 
     |                                          |                          |       
     |                                          |~~~initialize()~~~~~~~~~~>|       
     |                                          |                          |       
     |                                          |<--db---------------------|       
     |                                          |                          |       
     |                                       ************************************* 
     |                                       * elif db.is_connected()            * 
     |                                       ************************************* 
     |                                          |                          |       
     |                                          |~~~keepalive()~~~~~~~~~~~>|       
     |                                          |                          |       
     |                                          |<-------------------------|       
     |                                          |                          |       
     |                                       ************************************* 
     |                                       * else                              * 
     |                                       ************************************* 
     |                                       ************************************* 
     |                                       * while not db.is_connected()       * 
     |                                       ************************************* 
     |                                          |                          |       
     |                                          |~~~connect()~~~~~~~~~~~~~>|       
     |                                          |                          |       
     |                                          |<-------------------------|       
     |                                          |                          |       
     |                                       ************************************* 
     |                                       * end while                         * 
     |                                       ************************************* 
     |                                       ************************************* 
     |                                       * end if                            * 
     |                                       ************************************* 
     |                                          |                          |       
     |                                          |~~~create_token()~~~+     |       
     |                                          |                    |     |       
     |                                          |<--token------------+     |       
     |<--token----------------------------------|                          |       
     |                                          |                          |       
 ---------------------                          |                          |       
 | Alice decides to  |                          |                          |       
 | store the newly   |                          |                          |       
 | received Token    |                          |                          |       
 | in a safe place.  |                          |                          |       
 ---------------------                          |                          |       
     |                                          |                          |       
     |~~~store(token)~~~+                       |                          |       
     |                  |                       |                          |       
     |<-----------------+                       |                          |       
     |                                          |                          |       
 ---------------------------------------------------                       |       
 | Alice tries to logout                           |                       |       
 ---------------------------------------------------                       |       
     |                                          |                          |       
     |~~~logout(token)~~~~~~~~~~~~~~~~~~~~~~~~~>|                          |       
     |                                          |~~~delete(token)~~~~~~~~~>|       
     |                                          |                          |       
     |                                          |<-------------------------|       
     |                                          |                          |       
     |                                       ************************************* 
     |                                       * for each token in db              * 
     |                                       ************************************* 
     |                                          |                          |       
     |                                          |~~~delete(token)~~~~~~~~~>|       
     |                                          |                          |       
     |                                          |<-------------------------|       
     |                                          |                          |       
     |                                       ************************************* 
     |                                       * end for                           * 
     |                                       ************************************* 
     |                                          |                          |       
     |<-----------------------------------------|                          |       
     |                                          |                          |       
 +-------+                                   +-----+                 +-----------+ 
 | Alice |                                   | Bob |                 | Database  | 
 +-------+                                   +-----+                 +-----------+ 
                                                                                   
```
