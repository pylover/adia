Language Reference
==================

``ADia`` is an indent based language such as ``Python`` and uses indentation
to specify the ``parent/children`` relationship between entities.

Every statement of the ``ADia`` language is consist of one ``operation`` and
an optional ``text`` as follow:

.. code-block:: bash

   operation [: text]


Example:

.. testsetup::

   from adia import renders

.. doctest::

   >>> print(renders('''
   ... diagram: foo
   ... sequence:
   ... foo -> bar
   ... '''))

Diagram Header
**************

Every ``ADia`` document should starts with the ``digram: [TITLE]`` attribute.
There is other optional attributes: ``version`` and ``author``.

Example:

.. code-block:: adia

   diagram: Foo
   version: 1.0
   author: Alice

Output

.. code-block:: adia

   DIAGRAM: Foo 
   author: Alice
   version: 1.0 


Diagram Section
***************

Every ``ADia`` document may consists of zero or more sections which could be
one of ``sequence``, ``class`` and ``fork``.

.. note::

   Currently, only ``sequence`` diagram is implemented. It means every 
   ``ADia`` document may consists of zero or more sequence diagrams.

.. code-block:: adia

   diagram: Foo 
    
   sequence: foo bar
   foo -> bar

   sequence: bar baz
   bar -> baz

Sequence Diagram
****************

A sequence diagram is always starts with the ``sequence: [TITLE]`` keyword and
basically it is a collection of ``modules`` and ``items`` which described
below.

Module
^^^^^^

You may use shorter name for modules for simplicity and define comprehensive 
titile with ``MODULE.title: TITLE`` statement.


.. ::

   comments
   moduleattr
   call
   callstask
   selfcall
   condition
   loop
   note
   
