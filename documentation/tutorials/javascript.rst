Javascript
==========

Introduction
************

You may use the ``adia`` inside Javascript (browser) because we pass all tests 
with both ``CPython`` and ``Brython`` environments before each commit.

This page aims to demonstrate how to use the ``adia`` inside your javascript 
project.

For the first you have to generate ``adia.bundle.js`` using:

.. code-block:: bash

   cd path/to/adia
   make www


``www/build/adia.bundle.js`` is what you need now.

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
   from adia import renders, BadSyntax
   
   def adia_renders(source):
     try:
       return renders(source)
     except BadSyntax as ex:
       return f'Error: {ex}'
   
   window.adiaRenders = adia_renders
   </script>

   ...

   </body>
   </html>


After the setup above you can use the function ``window.adiaRenders(...)`` 
anywhere.


Javascript demo page
********************

Let's make and visit the provided javascript demo page: ``www/jsdemo.html``.

.. code-block:: bash

   cd path/to/adia
   make clean serve

Now browse the http://localhost:8000/jsdemo.html.
