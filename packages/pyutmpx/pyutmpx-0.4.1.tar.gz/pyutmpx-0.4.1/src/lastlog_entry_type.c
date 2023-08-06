/* ****************************************************************************
 * lastlog_entry_type.c -- lastlog entry definition and utilities.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <string.h>
#include <limits.h>

/* ---
 * Entry object definition.
 * --- */

/* ``entry_type``: the type of the entry. */

struct entry_type {
	PyObject_HEAD

	PyObject *uid;
    PyObject *line;
    PyObject *host;
    PyObject *time;
};

/* `new_entry()`: create the Python object. */

static PyObject *new_entry(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct entry_type *self;

	self = (struct entry_type *)type->tp_alloc(type, 0);

	if (self) {
        self->uid = NULL;
        self->line = NULL;
        self->host = NULL;
        self->time = NULL;
	}

	return ((PyObject *)self);
}

/* `init_entry()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_entry(struct entry_type *self,
	PyObject *args, PyObject *kw)
{
	char *keywords[] = {"uid", "line", "host", "time", NULL};

	/* Main parsing and default arguments. */

	if (!PyArg_ParseTupleAndKeywords(args, kw, "|$OOOO", keywords,
		&self->uid, &self->line, &self->host, &self->time))
		return (-1);

	/* Check the arguments.
	 * TODO: check their types too! (here?) */

	if (!self->uid)
		self->uid = Py_None;
	if (!self->line)
		self->line = Py_None;
	if (!self->host)
		self->host = Py_None;
	if (!self->time)
		self->time = Py_None;

	Py_INCREF(self->uid);
	Py_INCREF(self->line);
	Py_INCREF(self->host);
	Py_INCREF(self->time);

	return 0;
}

/* `del_entry()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_entry(struct entry_type *self)
{
	if (!self)
		return;

	Py_XDECREF(self->uid);
	Py_XDECREF(self->line);
	Py_XDECREF(self->host);
	Py_XDECREF(self->time);

	Py_TYPE(self)->tp_free((PyObject*)self);
}

/* ``repr_entry()``: actual C implementation of the ``__repr__`` function
 * for the utmp entry. */

static PyObject *repr_entry(struct entry_type *self)
{
	char buf[1024], *s = buf;
	size_t len = 1024;
	int haslast = 0;

#define prop(PROP, NAME) \
	if ((NAME) != Py_None) { \
		if (haslast) \
			pyutmpx_put_str(&s, &len, ", "); \
		pyutmpx_put_str(&s, &len, PROP " = "); \
		pyutmpx_put_repr(&s, &len, NAME); \
		haslast = 1; \
	}

	pyutmpx_put_str(&s, &len, "pyutmpx.lastlog_entry(");

	prop("uid",  self->uid)
	prop("host", self->host)
	prop("line", self->line)
	prop("time", self->time)

	pyutmpx_put_str(&s, &len, ")");

	return (Py_BuildValue("s", buf));
}

/* Entry object definition. */

static PyMethodDef entry_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyMemberDef entry_members[] = {
	{
		/* .name = */ "uid",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, uid),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The user identifier (uid) of the login process.\n"
			"\n"
			"This field is populated using the offset of the entry in\n"
			"the file."
		)
	},
	{
		/* .name = */ "host",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, host),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The host from which last login has occurred, as a string.\n"
			"\n"
			"This field is populated using the ``ll->ll_host`` field."
		)
	},
	{
		/* .name = */ "line",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, line),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The line on which last login has occurred, as a string.\n"
			"\n"
			"This field is populated using the ``ll->ll_line`` field."
		)
	},
	{
		/* .name = */ "time",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, time),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The time at which last login has occurred for this user,\n"
			"as a datetime with the UTC timezone.\n"
			"\n"
			"This field is populated using the ``ll->ll_time`` field."
		)
	},

	{NULL}
};

PyTypeObject pyutmpx_lastlog_entry_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.lastlog_entry",
	.tp_doc = PyDoc_STR(
		"lastlog entry representation, as described by the\n"
		"``struct lastlog`` type defined in ``<utmp.h>``."
	),
	.tp_basicsize = sizeof(struct entry_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_entry,
	.tp_init = (initproc)init_entry,
	.tp_dealloc = (destructor)del_entry,
	.tp_repr = (reprfunc)repr_entry,

	/* Members. */

	.tp_methods = entry_methods,
	.tp_members = entry_members
};

/* ---
 * Module setup.
 * --- */

/* `pyutmpx_init_utmp_entry_type()`: initialize utmp entry type
 * and specific utilities. */

int pyutmpx_init_lastlog_entry_type(PyObject *m)
{
	/* Create the utmp entry type to the module. */

	if (PyType_Ready(&pyutmpx_lastlog_entry_type) < 0)
		return -1;

	Py_INCREF((PyObject *)&pyutmpx_lastlog_entry_type);
	if (PyModule_AddObject(m, "lastlog_entry",
		(PyObject *)&pyutmpx_lastlog_entry_type) < 0) {
		Py_DECREF(&pyutmpx_lastlog_entry_type);
		return -1;
	}

	/* Prepare types. */

	return 0;
}

/* `pyutmpx_exit_lastlog_entry_type()`: deinitialize utmp entry type
 * and specific utilities. */

void pyutmpx_exit_lastlog_entry_type(void)
{
	/* Nothing to do here. */
}
