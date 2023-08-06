utmp/wtmp/btmp reader module for Python 3.x
===========================================

This project is a binary CPython 3.x module which allows you to interact with
the user accounting databases ``utmp``, ``wtmp``, ``btmp``, and ``lastlog``,
which keep track of the boot, login and logout events.

It was developed for the `fingerd`_ project, which needs to know the last
login date of a user, if the user is still logged in, on which line they are
connected to the system, and so on. I decided to make my own module to
manage these files.

For now, the project is only available on Linux.

For more information, you can consult the docs on `pyutmpx.touhey.pro
<https://pyutmpx.touhey.pro/>`_.

Quickstart
----------

A more thorough `onboarding guide`_ is available in the documentation;
here are some basic instructions.

Install the module by using the following command:

.. code-block:: sh

	python -m pip install pyutmpx

List all entries in the ``utmp`` file:

.. code-block:: python

	import pyutmpx

	for entry in pyutmpx.utmp:
		print(entry)

Get the last boot time:

.. code-block:: python

	import pyutmpx

	for entry in pyutmpx.utmp:
		if entry.type != pyutmpx.BOOT_TIME:
			continue
		print(f"Last boot time is {entry.time.isoformat()}")
		exit()

	print("No boot time on record.")

Get the last login time and host for a given user:

.. code-block:: python

	import pyutmpx

	uid = 1000

	for entry in pyutmpx.lastlog:
		if entry.uid != uid:
			continue

		print(f"Last login at {entry.time.isoformat()} on {entry.line} "
			f"from {entry.host}")
		exit()

	print("No last login.")

Changelog
---------

0.4.1 (September 19th, 2021)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the code:

   - Added a lot of macros to use feature tests in order to kickstart
     cross-platforming system-specific code.
   - Added compatibility for OpenBSD 6.x (tested on an OpenBSD 6.9 install).
   - Added management of the case where utmp entries found in the file
     are all-zeroes (now making pyutmpx ignoring them).
   - Rewrote the module's and attributes' description for expliciting how
     every attribute is gathered and populated.
   - Rewrote the object building logic to be more efficient and less
     cumbersome.
   - Made that system-specific functions now raise Python exceptions.
   - Fixed symbols that shouldn't have been exported (made them static).

 * In the documentation:

   - Added the ``ACCOUNTING`` and ``RUN_LEVEL`` types.
   - Added a description of the ``exit_status`` class, and
     ``wtmp`` and ``btmp`` objects.
   - Rewrote the attributes' description for expliciting how every
     property is populated.
   - Added a retroactive changelog (about time!).

 * In the build system:

   - Added the header to the dependency, in order to cause a rebuild
     on header modification.

0.4 (September 11th, 2021)
~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the code:

   - Added support for the wtmp and btmp user accounting databases.
   - Added support for the exit status (``ut->ut_exit``) with the addition
     of the ``exit_status`` class.
   - Added support for the session identifier (``ut->ut_session``) and
     remote Internet address (``ut->ut_addr_v6``).
   - Added the UTC timezone by default to all dates in all entries.
   - Isolated system-specific code into ``sys.c``.

 * In the documentation:

   - Removed the "reference" found in the README to replace it with a
     very simple quickstart piece of code.

0.3.1 (September 6th, 2021)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the code:

   - Added the forgotten ``host`` properties in those accessible in
     ``utmp_entry`` instances.

0.3 (September 6th, 2021)
~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the code:

   - Added a lastlog database reader.

 * In the documentation:

   - Added a first version of the documentation with three sections inspired
     from the Divio documentation framework: onboarding (tutorial),
     discussion topics and API (technical reference).
   - Created the <https://pyutmpx.touhey.pro/>_ website.

 * In the build system:

   - Removed the ``setup.cfg`` file in favor of having everything in the
     ``setup.py`` file.

0.2.2 (September 11th, 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the code:

   - Made utmp entry type public again; let users be adults.
   - Fixed bad reference counting on utmp entries.
   - Removed tests; system-specific stuff like this is hard to test.

 * In the documentation:

   - Added a small reference in the README file.

0.2.1 (September 11th, 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the code:

   - Put the headers with the rest of the source files.
   - Started making the code modular.
   - Made utmp entry type private, as it should only be returned by
     pyutmpx iterators.

 * In the documentation:

   - Fixed some reference issues in the README, identified using checkdocs.

0.2 (September 11th, 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the code:

   - Added some very basic tests.

 * In the documentation:

   - Rewrote the README from markdown to reStructuredText.

 * In the build system:

   - Separated the setup script into setup data (``setup.cfg``) and
     the script itself (``setup.py``).

0.1.3 (February 8th, 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the build system:

   - Fixed some packaging issues.

0.1.2 (February 7th, 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the code:

   - Renamed the main header from ``main.h`` to ``pyutmpx.h`` and
     added a few casts.

0.1.1 (February 7th, 2018)
~~~~~~~~~~~~~~~~~~~~~~~~~~

 * In the build system:

   - Fixed some packaging issues (headers not in package, does not build).

0.1 (February 7th, 2018)
~~~~~~~~~~~~~~~~~~~~~~~~

Initial release as an independent project from fingerd.

.. _fingerd: https://forge.touhey.fr/fingerd.git/
.. _Single Unix Specification: http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/utmpx.h.html
.. _onboarding guide: https://pyutmpx.touhey.pro/onboarding.html
