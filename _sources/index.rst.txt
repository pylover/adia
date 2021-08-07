.. ADia documentation master file, created by
   sphinx-quickstart on Tue Jan 21 16:31:18 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

v\ |version| documentation!
===========================

.. image:: http://img.shields.io/pypi/v/easycli.svg?style=for-the-badge&logo=python&logoColor=white&logoWidth=20
   :alt: PyPI
   :target: https://pypi.python.org/pypi/adia

.. image:: https://img.shields.io/github/workflow/status/pylover/adia/Build?style=for-the-badge&logo=github&logoWidth=20
   :alt: GitHub Workflow Status 
   :target: https://github.com/pylover/adia/actions

.. image:: https://img.shields.io/coveralls/github/pylover/adia?style=for-the-badge&logo=coveralls&logoWidth=20
   :alt: Coveralls
   :target: https://coveralls.io/github/pylover/adia?branch=master

.. image:: https://img.shields.io/badge/CPython-%3E%3D3.6-blue?style=for-the-badge&logo=python&logoColor=white&logoWidth=20
   :alt: CPython >= 3.6
   :target: https://python.org

.. image:: https://img.shields.io/badge/Brython-%3E%3D3.9.5-blue?style=for-the-badge&logo=python&logoColor=white&logoWidth=20
   :alt: Brython >= 3.9.5
   :target: https://brython.info

.. image:: https://img.shields.io/github/forks/pylover/adia?style=for-the-badge&logo=github&logoWidth=20
   :alt: GitHub forks
   :target: https://github.com/pylover/adia


About
#####

ADia is a language for ASCII diagrams. Currently, only ``sequence`` diagram is
supported. But the roadmap is to implement two additional diagram types: 
``fork/join`` and ``class``.

.. Uncomment after adding the javascript section.
   ADia can also run flawlessly inside the browsers using the awesome project: 
   `Brython <https://brython.info>`_. check out the Web Interface section below 
   for more info.

.. testcode:: quickstart

   adia.print('''
     diagram: Foo
     sequence:
     foo -> bar: Hello World!
   ''')

.. testoutput:: quickstart

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
   

.. seealso::

   :func:`adia.diagram`, :func:`adia.print` and :class:`adia.Diagram`.


Command Line Interface
######################


.. code-block:: bash

   $ adia << EOF
   diagram: Foo
   sequence:
   foo -> bar: Hello
   EOF

Or feed one or more filename(s):

.. code-block:: bash

   $ adia file1.adia file2.adia fileN.adia > foo.txt

Issue ``adia --help`` for more info.


Contents
########

.. toctree::
   :maxdepth: 2

   install
   lang
   pythonapi
   javascriptapi
   contributing

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
