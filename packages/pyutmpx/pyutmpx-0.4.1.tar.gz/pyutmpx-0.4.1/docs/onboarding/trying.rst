Trying pyutmpx out in an interactive shell
==========================================

Once installed, you can directly try pyutmpx out in an interactive shell.
For example, you can try reading the first entry from the ``utmp`` file:

::

	>>> import pyutmpx
	>>> for entry in pyutmpx.utmp:
	...     print(entry)
	...     break
	...
	pyutmpx.utmp_entry(type = BOOT_TIME, time = datetime.datetime(2021, 9, 5, 9, 24, 52), user = 'reboot', line = '~', pid = 0)
