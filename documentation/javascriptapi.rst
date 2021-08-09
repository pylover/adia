Javascript API
==============

Introduction
************

You may use the ``adia`` inside Javascript (browser) because we pass all tests 
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

Copy and paste the generated file inside your Javascript project's static
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
       return f'Error: {ex}'
   
   window.adiaDiagram = adia_diagram
   </script>

   ...

   </body>
   </html>


After the setup above you can use the function ``window.adiaDiagram(...)`` 
anywhere.


Javascript demo page
********************

Let's make and visit the provided javascript demo page: 
``webclinic/jsdemo.html``.

.. code-block:: bash

   cd path/to/adia
   make clean serve

Now browse the http://localhost:8000/jsdemo.html.
