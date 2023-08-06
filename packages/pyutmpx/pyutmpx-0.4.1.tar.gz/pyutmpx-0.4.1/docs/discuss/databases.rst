Databases accessible through pyutmpx
====================================

pyutmpx allows accessing a number of databases within the system:

 * ``utmp`` is a minimal list of events that allows a user to understand
   the current system status.
 * ``wtmp`` is a full list of events, and acts like a historical ``utmp``.
 * ``btmp`` is a list of failed login attempts.
 * ``lastlog`` is a list of last logins.

These files are available through formats varying between systems, even
within systems where one file can be available with the POSIX compliant
format and the historic format. pyutmpx makes use of the C APIs to abstract
these difficulties away from your code.

Descriptions for these files can be found on the following pages:

 * `utmp`_, from Wikipedia.
 * `utmpx.h`_, from the Single Unix Specification.
 * `lastlog(5)`_, from the FreeBSD 5.0 manpages.

.. _utmp: https://en.wikipedia.org/wiki/Utmp
.. _utmpx.h: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/utmpx.h.html
.. _`lastlog(5)`: https://www.freebsd.org/cgi/man.cgi?query=lastlog&sektion=5&manpath=FreeBSD+5.0-RELEASE
