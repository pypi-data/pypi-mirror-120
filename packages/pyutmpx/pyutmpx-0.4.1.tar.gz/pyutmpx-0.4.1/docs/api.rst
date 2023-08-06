API Reference
=============

.. py:module:: pyutmpx

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

utmp entry types
----------------

.. py:data:: EMPTY: int = 0

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	an invalid or empty event.

.. py:data:: BOOT_TIME: int = 1

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a host boot event.

.. py:data:: OLD_TIME: int = 2

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a time yield event before system time change.

.. py:data:: NEW_TIME: int = 3

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a time yield event after system time change.

.. py:data:: USER_PROCESS: int = 4

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a user process.

.. py:data:: INIT_PROCESS: int = 5

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a process spawned by the init process.

.. py:data:: LOGIN_PROCESS: int = 6

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a process which is the session leader of a user.

.. py:data:: DEAD_PROCESS: int = 7

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a session leader who has exited.

.. py:data:: RUN_LEVEL: int = 8

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a system run-level change.

.. py:data:: ACCOUNTING: int = 9

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	an other accounting event.

Entry formats
-------------

.. py:class:: exit_status

	Exit status representation for dead process entries in utmp
	and related databases, as described by the
	``struct exit_status`` type defined in ``<utmp.h>``.

	.. py:attribute:: termination: int

		The process termination status, i.e. whether it has exited
		normally using exit(2) or if it has been terminated
		using a signal.

		This field is populated using the ``e->e_termination`` field.
		Refer to ``<utmp.h>`` and wait(2) for more information.

	.. py:attribute:: exit: int

		The process exit status, i.e. the code returned by the
		process in the case it has called exit(2).

		This field is populated using the ``e->e_exit`` field.
		Refer to ``<utmp.h>`` and wait(2) for more information.

.. py:class:: utmp_entry

	utmp entry representation, as described by either the
	``struct utmp`` type defined in ``<utmp.h>`` or the ``struct utmpx``
	type defined in ``<utmpx.h>``.

	.. py:attribute:: id: str

		The unspecified initialization process identifier.

		This field is populated using the ``ut->ut_id`` field,
		when available.

	.. py:attribute:: type: int

		The type of the entry, amongst the following constants:

		:py:data:`pyutmpx.EMPTY`
			No valid user accounting information.

		:py:data:`pyutmpx.BOOT_TIME`
			Identifies time of system boot.

		:py:data:`pyutmpx.OLD_TIME`
			Identifies time when system clock changed.

		:py:data:`pyutmpx.NEW_TIME`
			Identifies time after system clock changed.

		:py:data:`pyutmpx.USER_PROCESS`
			Identifies a process.

		:py:data:`pyutmpx.INIT_PROCESS`
			Identifies a process spawned by the init process.

		:py:data:`pyutmpx.LOGIN_PROCESS`
			Identifies a session leader of a logged-in user.

		:py:data:`pyutmpx.DEAD_PROCESS`
			Identifies a session leader who has exited.

		:py:data:`pyutmpx.RUN_LEVEL`
			Identifies a change in system run-level; refer to init(1)
			for more information.

		:py:data:`pyutmpx.ACCOUNTING`
			No information available.

		This field is populated using the ``ut->ut_type`` field,
		when available.

	.. py:attribute:: user: str

		The login name of the user involved in the event.

		This field is populated using the ``ut->ut_user`` or
		``ut->ut_name`` fields.

	.. py:attribute:: host: str

		The host from which the event has occurred.

		The name of the remote host from which the event has occurred
		in the case of remote logins, or the kernel version for other
		system-related events.

		This field is populated using the ``ut->ut_host`` field,
		when available.

	.. py:attribute:: line: str

		The line or device on which the event has occurred.

		This field is populated using the ``ut->ut_line`` field.

	.. py:attribute:: time: datetime.datetime

		The time at which the entry was added to the database, as
		a datetime using the UTC timezone.

		This field is populated using the ``ut->ut_tv``,
		``ut->ut_time`` or ``ut->ut_xtime`` fields, when available.

	.. py:attribute:: pid: int

		The process identifier (pid), for process or session leader
		related events.

		This field is populated using the ``ut->ut_pid`` field,
		when available.

	.. py:attribute:: sid: int

		The session identifier (sid) of the process, used for
		windowing.

		This field is populated using the ``ut->ut_session`` field,
		when available. Refer to getsid(2) for more information.

	.. py:attribute:: exit: exit_status

		The exit status of the process or session leader on
		dead process events, as a :py:class:`pyutmpx.exit_status`
		instance.

		This field is populated using the ``ut->ut_exit`` field,
		when available.

	.. py:attribute:: addr: str

		The IPv4 or IPv6 address of the host in case of remote logins,
		as a string.

		This field is populated using the ``ut->ut_addr_v6`` or
		``ut->ut_addr`` fields, when available.

.. py:class:: lastlog_entry

	lastlog entry representation, as described by the
	``struct lastlog`` type defined in ``<utmp.h>``.

	.. py:attribute:: uid: int

		The user identifier (uid) of the login process.

		This field is populated using the offset of the entry in
		the file.

	.. py:attribute:: host: str

		The host from which last login has occurred, as a string.

		This field is populated using the ``ll->ll_host`` field.

	.. py:attribute:: line: str

		The line on which last login has occurred, as a string.

		This field is populated using the ``ll->ll_line`` field.

	.. py:attribute:: time: datetime.datetime

		The time at which last login has occurred for this user,
		as a datetime with the UTC timezone.

		This field is populated using the ``ll->ll_time`` field.

Classes abstracting the databases
---------------------------------

.. py:class:: utmp

	An iterable read-only view of the utmp database, yielding
	:py:class:`utmp_entry` instances.

.. py:class:: wtmp

	An iterable read-only view of the wtmp (historical utmp) database
	when available, yielding :py:class:`utmp_entry` instances.

.. py:class:: btmp

	An iterable read-only view of the btmp (bad logins) database
	when available, yielding :py:class:`utmp_entry` instances.

.. py:class:: lastlog

	An iterable read-only view of the lastlog database, yielding
	:py:class:`lastlog_entry` instances.
