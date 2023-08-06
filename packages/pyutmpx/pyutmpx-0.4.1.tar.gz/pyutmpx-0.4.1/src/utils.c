/* ****************************************************************************
 * utils.c -- general utilities.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <datetime.h>

/* ---
 * Buffer utilities.
 * --- */

/* ``pyutmpx_put_str()``: at the end of ``*ps`` of size ``*pn``, copies the
 * ``s`` string up to ``*pn`` bytes at a maximum, then updates ``*ps`` to the
 * end of the copy and ``*pn`` to the number of left bytes after copy. */

void pyutmpx_put_str(char **ps, size_t *pn, char const *s)
{
	size_t len;

	strncpy(*ps, s, *pn);
	len = strlen(*ps);
	*ps += len;
	*pn -= len;
}

/* ``pyutmpx_put_repr()``: at the end of ``*ps`` of size ``*pn``, copies the
 * string representation of the object ``o`` to ``*pn`` bytes at a maximum,
 * then updates ``*ps`` to the end of the copy and ``*pn`` to the number of
 * left bytes after copy. */

void pyutmpx_put_repr(char **ps, size_t *pn, PyObject *o)
{
	PyObject *repr, *repr_utf8;
	char const *r;
	int has_failed = 1;

	/* Get the representation. */

	repr = PyObject_Repr(o);
	if (!repr)
		goto fail;

	/* Encode the representation as UTF-8 */

	repr_utf8 = PyUnicode_AsEncodedString(repr, "utf-8", "~E~");
	Py_DECREF(repr);
	if (!repr_utf8)
		goto fail;

	/* Get a C string from the Python encoded string. */

	r = PyBytes_AS_STRING(repr_utf8);
	Py_DECREF(repr_utf8);

	/* Get a default string if has failed. */

	has_failed = 0;
fail:
	if (has_failed)
		r = "(unknown)";

	/* Copy into the final buffer. */

	pyutmpx_put_str(ps, pn, r);
}

/* `pyutmpx_get_len()`: get the length of the ``s`` string, up to ``n``
 * bytes at a maximum. */

Py_ssize_t pyutmpx_get_len(char const *s, Py_ssize_t n)
{
	Py_ssize_t len;

	if (!s)
		len = 0;
	else if (n <= 0) {
		size_t slen = strlen(s);

		if (slen > INT_MAX)
			len = INT_MAX;
		else
			len = (Py_ssize_t)slen;
	} else {
		char const *ptr = memchr(s, '\0', (size_t)n);

		if (!ptr)
			len = n;
		else
			len = (Py_ssize_t)(ptr - s);
	}

	return (len);
}

/* ---
 * Building objects.
 * --- */

/* `pyutmpx_build_datetime()`: utility to build a datetime from a timeval,
 * with a reference already present. */

PyObject *pyutmpx_build_datetime(struct timeval const *tv)
{
	PyObject *datetime = NULL;

	/* Create the datetime. */

	{
		PyObject *epoch = NULL, *delta = NULL;

		epoch = PyDateTime_FromDateAndTime(1970, 1, 1, 0, 0, 0, 0);
		delta = PyDelta_FromDSU(0, tv->tv_sec, tv->tv_usec);

		if (epoch && delta)
			datetime = PyNumber_Add(epoch, delta);

		Py_XDECREF(epoch);
		Py_XDECREF(delta);

		if (!datetime)
			return NULL;
	}

	/* Set the timezone. */

	{
		PyObject *replace_method = NULL;
		PyObject *args = NULL, *kwargs = NULL;
		PyObject *new_datetime = NULL;

		replace_method = PyObject_GetAttrString(datetime, "replace");
		args = Py_BuildValue("()");
		kwargs = Py_BuildValue("{s:O}", "tzinfo", PyDateTime_TimeZone_UTC);

		if (replace_method && args && kwargs)
			new_datetime = PyObject_Call(replace_method, args, kwargs);

		Py_XDECREF(replace_method);
		Py_XDECREF(args);
		Py_XDECREF(kwargs);

		Py_DECREF(datetime);
		if (!new_datetime)
			return NULL;

		datetime = new_datetime;
	}

	/* We're done! */

	return (datetime);
}

/* `pyutmpx_build_utmp_entry()`: build a utmp_entry object. */

PyObject *pyutmpx_build_utmp_entry(struct utmp_node const *node)
{
	PyObject *entry = NULL;
	PyObject *estatus = NULL;

	/* Get the exit status. */

	{
		PyObject *args = NULL, *kwargs = NULL;
		PyObject *exit_code = NULL, *termination_code = NULL;

		if (!node->exit)
			estatus = Py_None;
		else {
			args = Py_BuildValue("()");
			if (!args)
				return (NULL);

			/* Get exit code object. */

			if (node->exit->status_code)
				exit_code = Py_BuildValue("i", *node->exit->status_code);
			else
				exit_code = Py_BuildValue("");

			/* Get thetermination code object. */

			if (node->exit->termination_code)
				termination_code = Py_BuildValue("i",
					*node->exit->termination_code);
			else
				termination_code = Py_BuildValue("");

			/* Allocate the kwargs. */

			if (exit_code && termination_code)
				kwargs = Py_BuildValue("{s:O,s:O}",
					"exit", exit_code,
					"termination", termination_code);

			Py_XDECREF(exit_code);
			Py_XDECREF(termination_code);

			/* Get the estatus. */

			if (args && kwargs)
				estatus = PyObject_Call((PyObject *)&pyutmpx_exit_status_type,
					args, kwargs);

			Py_XDECREF(args);
			Py_XDECREF(kwargs);
		}

		if (!estatus)
			return (NULL);
	}

	/* Get the entry object! */

	{
		PyObject *date_object = NULL;
		PyObject *type_object = NULL;
		PyObject *pid_object = NULL;
		PyObject *sid_object = NULL;
		PyObject *args = NULL, *kwargs = NULL;

		/* Get the date object. */

		if (node->time)
			date_object = pyutmpx_build_datetime(node->time);
		else
			date_object = Py_None;

		/* Get the type object. */

		if (node->type)
			type_object = Py_BuildValue("i", *node->type);
		else
			type_object = Py_BuildValue("");

		/* Get the pid object. */

		if (node->pid)
			pid_object = Py_BuildValue("k", *node->pid);
		else
			pid_object = Py_BuildValue("");

		/* Get the sid object. */

		if (node->sid)
			sid_object = Py_BuildValue("k", *node->sid);
		else
			sid_object = Py_BuildValue("");

		/* Build the arguments.
		 * ``estatus`` is guaranteed to exist at this point. */

		args = Py_BuildValue("()");
		if (type_object && pid_object && sid_object && date_object)
			kwargs = Py_BuildValue(
				"{s:O,s:O,s:s#,s:s#,s:s#,s:s#,s:O,s:O,s:O,s:s#}",
				"type", type_object,
				"pid", pid_object,
				"line", node->line, node->line_size,
				"id", node->id, node->id_size,
				"user", node->user, node->user_size,
				"host", node->host, node->host_size,
				"exit", estatus,
				"sid", sid_object,
				"time", date_object,
				"addr", node->addr, node->addr_size);

		Py_XDECREF(sid_object);
		Py_XDECREF(pid_object);
		Py_XDECREF(type_object);
		Py_XDECREF(date_object);
		Py_XDECREF(estatus);

		if (args && kwargs)
			entry = PyObject_Call((PyObject *)&pyutmpx_utmp_entry_type,
				args, kwargs);

		Py_XDECREF(args);
		Py_XDECREF(kwargs);
	}

	return entry;
}

/* `pyutmpx_build_lastlog_entry()`: build a lastlog_entry object. */

PyObject *pyutmpx_build_lastlog_entry(struct lastlog_node const *node)
{
	PyObject *entry = NULL;
	PyObject *date_object = NULL;
	PyObject *args = NULL, *kwargs = NULL;

	date_object = pyutmpx_build_datetime(&node->date);

	args = Py_BuildValue("()");
	if (date_object)
		kwargs = Py_BuildValue("{s:k,s:s#,s:s#,s:O}",
			"uid", node->uid,
			"host", node->host, node->host_size,
			"line", node->line, node->line_size,
			"time", date_object);

	Py_XDECREF(date_object);

	if (args && kwargs)
		entry = PyObject_Call((PyObject *)&pyutmpx_lastlog_entry_type,
			args, kwargs);

	Py_XDECREF(args);
	Py_XDECREF(kwargs);

	return (entry);
}

/* ---
 * Setup.
 * --- */

int pyutmpx_init_utils(PyObject *module)
{
	/* Import the datetime module. */

	PyDateTime_IMPORT;

	return 0;
}

void pyutmpx_exit_utils(void)
{
	/* Nothing to do here. */
}
