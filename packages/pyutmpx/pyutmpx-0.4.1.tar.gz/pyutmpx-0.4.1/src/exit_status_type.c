/* ****************************************************************************
 * exit_status_type.c -- exit status structure.
 * Copyright (C) 2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
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

	PyObject *termination; /* e_termination */
	PyObject *exit; /* e_exit */
};

/* `new_entry()`: create the Python object. */

static PyObject *new_entry(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct entry_type *self;

	self = (struct entry_type *)type->tp_alloc(type, 0);

	if (self) {
		self->termination = NULL;
		self->exit = NULL;
	}

	return ((PyObject *)self);
}

/* `init_entry()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_entry(struct entry_type *self,
	PyObject *args, PyObject *kw)
{
	char *keywords[] = {"termination", "exit", NULL};

	/* Main parsing and default arguments. */

	if (!PyArg_ParseTupleAndKeywords(args, kw, "|$OO", keywords,
		&self->termination, &self->exit))
		return (-1);

	/* Check the arguments.
	 * TODO: check their types too! (here?) */

	if (!self->termination)
		self->termination = Py_None;
	if (!self->exit)
		self->exit = Py_None;

	Py_INCREF(self->termination);
	Py_INCREF(self->exit);

	return 0;
}

/* `del_entry()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_entry(struct entry_type *self)
{
	if (!self)
		return;

	Py_XDECREF(self->termination);
	Py_XDECREF(self->exit);

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

	pyutmpx_put_str(&s, &len, "pyutmpx.exit_status(");

	prop("termination", self->termination)
	prop("exit",        self->exit)

	pyutmpx_put_str(&s, &len, ")");

	return (Py_BuildValue("s", buf));
}

/* Entry object definition. */

static PyMethodDef entry_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyMemberDef entry_members[] = {
	{
		/* .name = */ "termination",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, termination),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The process termination status, i.e. whether it has exited\n"
			"normally using exit(2) or if it has been terminated\n"
			"using a signal.\n"
			"\n"
			"This field is populated using the ``e->e_termination`` field.\n"
			"Refer to <utmp.h> and wait(2) for more information."
		)
	},
	{
		/* .name = */ "exit",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, exit),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The process exit status, i.e. the code returned by the\n"
			"process in the case it has called exit(2).\n"
			"\n"
			"This field is populated using the ``e->e_exit`` field.\n"
			"Refer to <utmp.h> and wait(2) for more information."
		)
	},

	{NULL}
};

PyTypeObject pyutmpx_exit_status_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.exit_status",
	.tp_doc = PyDoc_STR(
		"Exit status representation for dead process entries in utmp\n"
		"and related databases, as described by the\n"
		"``struct exit_status`` type defined in ``<utmp.h>``."
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

/* `pyutmpx_init_exit_status_type()`: initialize exit status type
 * and specific utilities. */

int pyutmpx_init_exit_status_type(PyObject *m)
{
	/* Create the utmp entry type to the module. */

	if (PyType_Ready(&pyutmpx_exit_status_type) < 0)
		return -1;

	Py_INCREF((PyObject *)&pyutmpx_exit_status_type);
	if (PyModule_AddObject(m, "exit_status",
		(PyObject *)&pyutmpx_exit_status_type) < 0) {
		Py_DECREF(&pyutmpx_exit_status_type);
		return -1;
	}

	/* Prepare types. */

	return 0;
}

/* `pyutmpx_exit_exit_status_type()`: deinitialize exit status type
 * and specific utilities. */

void pyutmpx_exit_exit_status_type(void)
{
	/* Nothing to do here. */
}
