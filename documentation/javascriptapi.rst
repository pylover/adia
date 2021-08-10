Javascript API
==============

Introduction
************

The ADia can also run flawlessly inside the browsers because we pass all tests 
with both ``CPython`` and `Brython <https://brython.info/>`_ environments 
before each commit.

This page aims to demonstrate how to use the ``adia`` inside your javascript 
project.

For the first you have to grab the ``adia.bundle.js`` from 
https://pylover.github.io/adia/about or generate ``adia.bundle.js`` using:

.. code-block:: bash

   cd path/to/adia
   make webclinic


``webclinic/build/adia.bundle.js`` is what you need now.

Copy and paste the ``adia.bundle.js`` inside your Javascript project's static
directory, where you can fetch it by a URL. then load it using:

.. code-block:: html

   <html>
   <head>
   ...
   <script type="text/javascript" src="adia.bundle.js"></script>
   </head>
   <body onload="brython()">
   <script type="text/python">
   from browser import window
   import adia
   
   def adia_diagram(source):
     try:
       return adia.diagram(source)
     except adia.BadSyntax as ex:
       return f'Syntax Error: {ex}'
     except adia.BadAttribute as ex:
       return f'Attribute Error: {ex}'

   window.adiaDiagram = adia_diagram
   </script>

   ...

   </body>
   </html>


After the setup above you can use the function ``window.adiaDiagram(...)`` 
anywhere.


adia-live Source Code
*********************

The `ADia Live Demo <https://pylover.github.io/adia>`_ source code 
which exists at https://github.com/pylover/adia-live is a good example of how
to use the Javascript API. 

Web Clinic
**********

.. note::

   This section may be useful for the contibutors.

Let's make and visit the pure javascript echo system of the ``ADia`` inside 
the ``webclinic`` directory: 

``webclinic/jsdemo.html``.

.. code-block:: bash

   cd path/to/adia
   make clean webclinic_serve

Now browse the http://localhost:8000/jsdemo.html.


