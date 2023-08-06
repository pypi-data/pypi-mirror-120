Installing pyutmpx
==================

In order to run and tweak pyutmpx, you must first install it; this section
will cover the need.

Dependencies
------------

pyutmpx is a binary module for CPython 3.x, and only depends on standard
libraries which it checks.

Installing pyutmpx using pip
----------------------------

To install pyutmpx, you can use pip with the following command:

.. code-block:: sh

	python -m pip install pyutmpx

Some notes on this command:

 * On most Linux distributions, you can directly call ``pip`` (or ``pip3``
   on those where Python 2.x is still the default); I personnally prefer
   to call it through Python as a module.
 * On Linux and other UNIX-like distributions where Python 2.x is still the
   default, when Python 3.x is installed, you must usually call it using
   ``python3`` instead of ``python``.
 * On Microsoft Windows, the Python executable, when added to the PATH,
   goes by the name ``py`` instead of ``python``.
