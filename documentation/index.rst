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
   :target: https://github.com/pylover

ADia is a language for ASCII diagrams. Currently, only ``sequence`` diagram is
supported. But the roadmap is to implement two additional diagram types: 
``fork/join`` and ``class``.

.. code-block:: adia

   diagram: Foo
   sequence:
   foo -> bar: Hello World!

.. code-block::

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

Contents
********

.. toctree::
   :maxdepth: 2

   tutorial
   lang
   api
   faq
   howto

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
