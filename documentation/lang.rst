Language Reference
==================

``ADia`` is an indent based language such as ``Python`` and uses indentation
to specify the ``parent/children`` relationship between entities. Leading 
whitespaces at the beginning of a line is used to compute the indentation 
level of the line, which in turn is used to determine the grouping of 
statements.

Every statement of the ``ADia`` language is consist of one ``operation`` and
an optional ``text`` as follow:

.. code-block:: bash

   operation [: text]


Example:

.. testcode:: langref

   adia.print('''
       diagram: foo
       sequence:
       foo -> bar
   ''')

.. testoutput:: langref

   DIAGRAM: foo
   
   +-----+ +-----+
   | foo | | bar |
   +-----+ +-----+
      |       |
      |~~~~~~>|
      |       |
      |<------|
      |       |
   +-----+ +-----+
   | foo | | bar |
   +-----+ +-----+

Comments
--------

Every line started with `#` is comment and will be ignored by the lexer.


Diagram Header
--------------

Every ``ADia`` document should starts with the ``diagram: [TITLE]`` attribute.
There is also two optional attributes: ``version`` and ``author``.

Example:

.. testcode::

   adia.print('''
       diagram: Foo
       version: 1.0
       author: Alice

       sequence: Foo & Bar
       foo -> bar
   ''')

.. testoutput::
   :no-trim-doctest-flags:

   DIAGRAM: Foo
   author: Alice
   version: 1.0


   SEQUENCE: Foo & Bar

   +-----+ +-----+
   | foo | | bar |
   +-----+ +-----+
      |       |
      |~~~~~~>|
      |       |
      |<------|
      |       |
   +-----+ +-----+
   | foo | | bar |
   +-----+ +-----+


Diagram Section
---------------

Every ``ADia`` document may consists of zero or more sections which could be
one of ``sequence``, ``class`` and ``fork``.

.. testcode::

   adia.print('''
       diagram: Foo 
        
       sequence:  Foo & Bar
       foo -> bar

       sequence: Bar & Baz
       bar -> baz
   ''')

.. testoutput::
   :no-trim-doctest-flags:

   DIAGRAM: Foo


   SEQUENCE: Foo & Bar

   +-----+ +-----+
   | foo | | bar |
   +-----+ +-----+
      |       |
      |~~~~~~>|
      |       |
      |<------|
      |       |
   +-----+ +-----+
   | foo | | bar |
   +-----+ +-----+


   SEQUENCE: Bar & Baz

   +-----+ +-----+
   | bar | | baz |
   +-----+ +-----+
      |       |
      |~~~~~~>|
      |       |
      |<------|
      |       |
   +-----+ +-----+
   | bar | | baz |
   +-----+ +-----+

.. note::

   Currently, only the ``sequence`` diagram is implemented. It means every 
   ``ADia`` document may consists of zero or more sequence diagrams.


Sequence Diagram
----------------

A sequence diagram always starts with the ``sequence: [TITLE]`` keyword and
basically it is a collection of ``modules`` and ``items`` which described
below.

Module
^^^^^^

You may use shorter name for modules for simplicity and define comprehensive 
title with ``MODULE.title: TITLE`` statement.


.. testcode::

   adia.print('''
       diagram: foo
       sequence:
       foo.title: Mr Foo
       foo -> bar: hello!
   ''')

.. testoutput::

   DIAGRAM: foo

   +---------+     +-----+
   | Mr Foo  |     | bar |
   +---------+     +-----+
        |             |
        |~~~hello!~~~>|
        |             |
        |<------------|
        |             |
   +---------+     +-----+
   | Mr Foo  |     | bar |
   +---------+     +-----+


Note
^^^^

You can put note anywhere and at every indentation level. see below to learn
about the ``Single-Module`` and ``Multi-Module`` notes.


Single-Module Note
""""""""""""""""""

.. testcode::

   adia.print('''
       diagram: foo
       sequence:
       @foo: Over the foo->bar
       foo -> bar
         bar -> baz 
           @baz: Inside the bar->baz
         @bar: Under the bar->baz
   ''')

.. testoutput::

   DIAGRAM: foo

   +-----+              +-----+               +-----+
   | foo |              | bar |               | baz |
   +-----+              +-----+               +-----+
      |                    |                     |
   ---------------------   |                     |
   | Over the foo->bar |   |                     |
   ---------------------   |                     |
      |                    |                     |
      |~~~~~~~~~~~~~~~~~~~>|                     |
      |                    |~~~~~~~~~~~~~~~~~~~~>|
      |                    |                     |
      |                    |                  -----------------------
      |                    |                  | Inside the bar->baz |
      |                    |                  -----------------------
      |                    |                     |
      |                    |<--------------------|
      |                    |                     |
      |                 ----------------------   |
      |                 | Under the bar->baz |   |
      |                 ----------------------   |
      |                    |                     |
      |<-------------------|                     |
      |                    |                     |
   +-----+              +-----+               +-----+
   | foo |              | bar |               | baz |
   +-----+              +-----+               +-----+


Multi-Module Note
"""""""""""""""""

A ``Multi-Module Note`` may cover two or more modules.

.. testcode::

   adia.print('''
       diagram: foo
       sequence:
       @foo ~ bar: Lorem Ipsum
       foo -> bar
         bar -> baz 
           @foo ~ baz: Lorem Ipsum 
   ''')

.. testoutput::

   DIAGRAM: foo

   +-----+ +-----+ +-----+
   | foo | | bar | | baz |
   +-----+ +-----+ +-----+
      |       |       |
   ---------------    |
   | Lorem Ipsum |    |
   ---------------    |
      |       |       |
      |~~~~~~>|       |
      |       |~~~~~~>|
      |       |       |
   -----------------------
   | Lorem Ipsum         |
   -----------------------
      |       |       |
      |       |<------|
      |<------|       |
      |       |       |
   +-----+ +-----+ +-----+
   | foo | | bar | | baz |
   +-----+ +-----+ +-----+


Call
^^^^

A call is consists of ``CALLER -> CALLEE[: [FUNCTION] [-> RETURN]]``.

``CALLER`` and ``CALLEE`` are modules which described above.

``FUNCTION`` and ``RETURN`` can be any ``ASCII`` character.

.. testcode::

   adia.print('''
       diagram: foo
       sequence:

       @foo ~ bar: Without function name
       foo -> bar
        
       @foo ~ bar: With function name
       foo -> bar: init(options)

       @foo ~ bar: With function name & return value
       foo -> bar: init(options) -> err

       @foo ~ bar: Only return value
       foo -> bar: -> err
   ''')

.. testoutput::

   DIAGRAM: foo

   +-----+                       +-----+
   | foo |                       | bar |
   +-----+                       +-----+
      |                             |
   -------------------------------------
   | Without function name             |
   -------------------------------------
      |                             |
      |~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|
      |                             |
      |<----------------------------|
      |                             |
   -------------------------------------
   | With function name                |
   -------------------------------------
      |                             |
      |~~~init(options)~~~~~~~~~~~~>|
      |                             |
      |<----------------------------|
      |                             |
   -------------------------------------
   | With function name & return value |
   -------------------------------------
      |                             |
      |~~~init(options)~~~~~~~~~~~~>|
      |                             |
      |<--err-----------------------|
      |                             |
   -------------------------------------
   | Only return value                 |
   -------------------------------------
      |                             |
      |~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|
      |                             |
      |<--err-----------------------|
      |                             |
   +-----+                       +-----+
   | foo |                       | bar |
   +-----+                       +-----+


Self Call
"""""""""

.. testcode::

   adia.print('''
       diagram: foo
       sequence:
       foo -> foo
       foo -> foo: self_test() -> Result
   ''')

.. testoutput::

   DIAGRAM: foo

   +-----+
   | foo |
   +-----+
      |
      |~~~~~~+
      |      |
      |<-----+
      |
      |~~~self_test()~~~+
      |                 |
      |<--Result--------+
      |
   +-----+
   | foo |
   +-----+


Callstack
"""""""""

Use one indentation level to put one or more item inside another.

Consider these ``Python`` modules: ``foo.py`` and ``bar.py``.


``foo.py``

.. code-block:: python

   import bar


   bat.init()

``bar.py``

.. code-block:: python

   import baz
   import qux

   def prepare():
       ...

   def init():
     prepare()
     baz.init()
     qux.init()

``ADia`` representation of the codes above would be something like this:

.. testcode::

   adia.print('''
       diagram: foo
       sequence:
       foo -> bar: init()
         bar -> bar: prepare()
         bar -> baz: init()
         bar -> qux: init()
   ''')

.. testoutput::

   DIAGRAM: foo

   +-----+       +-----+            +-----+ +-----+
   | foo |       | bar |            | baz | | qux |
   +-----+       +-----+            +-----+ +-----+
      |             |                  |       |
      |~~~init()~~~>|                  |       |
      |             |~~~prepare()~~~+  |       |
      |             |               |  |       |
      |             |<--------------+  |       |
      |             |                  |       |
      |             |~~~init()~~~~~~~~>|       |
      |             |                  |       |
      |             |<-----------------|       |
      |             |                  |       |
      |             |~~~init()~~~~~~~~~~~~~~~~>|
      |             |                  |       |
      |             |<-------------------------|
      |<------------|                  |       |
      |             |                  |       |
   +-----+       +-----+            +-----+ +-----+
   | foo |       | bar |            | baz | | qux |
   +-----+       +-----+            +-----+ +-----+


Condition
---------

.. testcode::

   adia.print('''
       diagram: foo
       sequence:
       foo -> bar: init(force, full)
         if: force
           bar -> baz: force_init()
         elif: full
           bar -> baz: full_init()
         else:
           bar -> baz: init()
   ''')

.. testoutput::

   DIAGRAM: foo

   +-----+                  +-----+             +-----+
   | foo |                  | bar |             | baz |
   +-----+                  +-----+             +-----+
      |                        |                   |
      |~~~init(force, full)~~~>|                   |
      |                        |                   |
      |                     ***************************
      |                     * if force                *
      |                     ***************************
      |                        |                   |
      |                        |~~~force_init()~~~>|
      |                        |                   |
      |                        |<------------------|
      |                        |                   |
      |                     ***************************
      |                     * elif full               *
      |                     ***************************
      |                        |                   |
      |                        |~~~full_init()~~~~>|
      |                        |                   |
      |                        |<------------------|
      |                        |                   |
      |                     ***************************
      |                     * else                    *
      |                     ***************************
      |                        |                   |
      |                        |~~~init()~~~~~~~~~>|
      |                        |                   |
      |                        |<------------------|
      |                        |                   |
      |                     ***************************
      |                     * end if                  *
      |                     ***************************
      |                        |                   |
      |<-----------------------|                   |
      |                        |                   |
   +-----+                  +-----+             +-----+
   | foo |                  | bar |             | baz |
   +-----+                  +-----+             +-----+


Loop
^^^^

For Loop
""""""""
.. testcode::

   adia.print('''
       diagram: foo
       sequence:
       foo -> bar: init(forks)
         for: i in range(forks)
           bar -> baz: fork(i)
   ''')

.. testoutput::

   DIAGRAM: foo

   +-----+            +-----+           +-----+
   | foo |            | bar |           | baz |
   +-----+            +-----+           +-----+
      |                  |                 |
      |~~~init(forks)~~~>|                 |
      |                  |                 |
      |               *************************
      |               * for i in range(forks) *
      |               *************************
      |                  |                 |
      |                  |~~~fork(i)~~~~~~>|
      |                  |                 |
      |                  |<----------------|
      |                  |                 |
      |               *************************
      |               * end for               *
      |               *************************
      |                  |                 |
      |<-----------------|                 |
      |                  |                 |
   +-----+            +-----+           +-----+
   | foo |            | bar |           | baz |
   +-----+            +-----+           +-----+

While Loop
""""""""""

.. testcode::

   adia.print('''
       diagram: foo
       sequence:
       while: True
         foo -> bar: accept() -> socket
   ''')

.. testoutput::

   DIAGRAM: foo

   +-----+         +-----+
   | foo |         | bar |
   +-----+         +-----+
      |               |
   ***********************
   * while True          *
   ***********************
      |               |
      |~~~accept()~~~>|
      |               |
      |<--socket------|
      |               |
   ***********************
   * end while           *
   ***********************
      |               |
   +-----+         +-----+
   | foo |         | bar |
   +-----+         +-----+
