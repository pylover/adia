Javascript API
==============

Introduction
************

The ADia can also run flawlessly inside the browsers's web worker environment
because we pass all tests with both ``CPython`` and 
`Brython <https://brython.info/>`_ environments before each commit.

This page aims to demonstrate how to use the ``adia`` inside your javascript 
project.

For the first you have to grab the file: "adia-\ |version|\ .tar.gz" from the
https://pylover.github.io/adia/about page or generate it using:

.. code-block:: bash

   cd path/to/adia
   make jsdist


The ``build/jsdist/adia-<ver>.tar.gz`` is what you need now.

Archive contains:

.. code-block::

   adia.bundle.js
   adia.js
   adia.stdlib.js
   adia_worker.py
   adia/
     __init__.py
     canvas.py
     constants.py
     container.py
     diagram.py
     exceptions.py
     interpreter.py
     lazyattr.py
     mutablestring.py
     renderer.py
     renderingplans.py
     sequence.py
     tokenizer.py
     token.py

Extract the ``adia-<ver>.tar.gz`` file into Javascript project's static
directory, where you can fetch it's content by URL. then modify your HTML file
as the below:


.. code-block:: html

   <html>
   <head>
   ...   

   <!-- One-By-One  -->
   <script type="text/javascript" src="brython.js"></script>
   <script type="text/javascript" src="adia.stdlib.js"></script>
   <script type="text/javascript" src="adia.js"></script>

   <!-- OR Bundle -->
   <script type="text/javascript" src="adia.bundle.js"></script>
   ... 
   </head>
   <body onload="brython()">

     <!-- Page DOM -->
     <textarea cols="100" rows="8" id="error"></textarea>
     <label id="status"></label>
     <br />
     <textarea cols="55" rows="40" id="source"></textarea>
     <textarea cols="120" rows="40" id="target"></textarea>

     <!-- Brython Setup -->
     <script type="text/python">
     # Coding style: PEP8

     from browser import window, bind, worker
     
     
     adiaworker = worker.Worker('adiaWorker')
     
     
     @bind(adiaworker, 'message')
     def onmessage(e):
       window.__adia__.callback(e.data)
     
     
     window.__adia__ = {
       'send': adiaworker.send,
       'callback': None
     }
     </script>

     <!-- Usage -->
     <script>
     let sourceArea = document.getElementById('source');
     let targetArea = document.getElementById('target');
     let errorArea = document.getElementById('error');
     let statusArea = document.getElementById('status');
     
     /* Create ADia instance */
     const aDia = new ADia({
       delay: 10,  // ms
       input: sourceArea,
       clean: () => {
         errorArea.value = '';
         targetArea.value = '';
       },
       success: dia => targetArea.value = dia,
       error: msg => errorArea.value = msg,
       status: state => statusArea.innerText = state
     });
     </script>

   ...

   </body>
   </html>


The ``ADia`` class will listen for changes of source element and inform you
by provided callbacks.


Let's make and visit the pure javascript echo system of the ``ADia`` inside 
the ``webclinic`` directory: 

.. code-block:: bash

   cd path/to/adia
   make clean webclinic_serve

Now browse the http://localhost:8000/index.html.


adia-live Source Code
*********************

The `ADia Live Demo <https://pylover.github.io/adia>`_ source code 
which exists at https://github.com/pylover/adia-live is a good example of how
to use the Javascript API. 


