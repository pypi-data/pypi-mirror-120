Welcome to pyutmpx's documentation!
===================================

pyutmpx is a CPython 3.x module which allows you to interact with
user accounting databases, a.k.a login-related log files found
within POSIX systems, such as ``utmp``, ``wtmp`` and ``btmp``.

It was developed for the `fingerd`_ project, which needs to know the last
login date of a user, if the user is still logged in, on which line they are
connected to the system, and so on. I decided to make my own module to
manage these files.

These files and the interfaces to them vary among systems, but this module
attempts at implementing as much as possible, including the standardized
form in POSIX and the `Single Unix Specification`_.

.. toctree::
	:maxdepth: 3

	onboarding
	discuss
	api

.. _fingerd: https://forge.touhey.fr/fingerd.git/
.. _Single Unix Specification: http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/utmpx.h.html
