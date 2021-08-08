Contributing
============

First of all, fork and clone the `ADia <https://github.com/pylover/adia>`_.

.. code-block:: bash
   
   cd path/to/adia

What you have to do before sending any pull request:

* Pass All CPython tests
* Ensure the code coverage factor remains at ``100%``.
* Pass Javascript tests
* Lint
* Doctest


Setup Development Environment
#############################

Use your favorite virtual environment tool such as 
https://pypi.org/project/virtualenvwrapper/.

In order, you need ``GNU Make`` to continue.

.. code-block:: bash
   
   sudo apt install make
   make env


Running CPython tests
#####################

.. code-block:: bash

   make test

Coverage Result
***************

.. code-block:: bash

   make cover


Lint
####

.. code-block:: bash

   make lint


Documentation
#############


.. code-block:: bash

   make doc


Generated HTML documentation can be found at ``documentation/build``.

.. seealso::

   https://www.sphinx-doc.org/en/master/usage/quickstart.html

Live Documenetation
*******************

.. code-block:: bash

   make livedoc


Now browse the http://localhost:8082.


Doctest
*******

.. code-block:: bash

   make doctest

.. seealso::

   https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html

Javascript Tests
################

Run:

.. code-block:: bash
    
   make clean serve

To build and serve the client side test files.

Then browse http://0.0.0.0:8000/check.html and wait to pass/fail tests.

Update Brython runtime
**********************

Run ``make cleanall`` to force the ``webclinic`` makefile rule to download and 
update ``brython*.js`` files.

.. code-block:: bash

   make cleanall webclinic

.. seealso::

   https://brython.info/
