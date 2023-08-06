/* ****************************************************************************
 * lastlog_type.c -- lastlog file iterator definition.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#if defined(PYUTMPX_HAS_LASTLOG) && PYUTMPX_HAS_LASTLOG

/* ---
 * lastlog_iter object definition.
 * --- */

/* ``lastlog_iter_type``: the main iterator type. */

struct lastlog_iter_type {
	PyObject_HEAD

	struct lastlog_node *nodes;
};

/* `new_lastlog_iter()`: initialize a lastlog iterator. */

static PyObject *new_lastlog_iter(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct lastlog_iter_type *self;

	self = (struct lastlog_iter_type *)type->tp_alloc(type, 0);
	return ((PyObject *)self);
}

/* `init_lastlog_iter()`: initialize the Python object. */

static int init_lastlog_iter(struct lastlog_iter_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	/* Load all entries now to avoid having problems with multiple
	 * iterators. */

	pyutmpx_get_lastlog_nodes(&self->nodes);

	/* Reset the thing and return. */

	return (0);
}

/* `del_lastlog_iter()`: destroy the Python object. */

static void del_lastlog_iter(struct lastlog_iter_type *self)
{
	if (!self)
		return ;

	while (self->nodes) {
		struct lastlog_node *node = self->nodes;

		self->nodes = self->nodes->next;
		free(node);
	}

	Py_TYPE(self)->tp_free((PyObject *)self);
}

/* `repr_lastlog_iter()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_lastlog_iter(struct lastlog_iter_type *Py_UNUSED(self))
{
	return (Py_BuildValue("s", "pyutmpx.lastlog_iter_type()"));
}

/* `next_lastlog_iter()`: return next element in self. */

static PyObject *next_lastlog_iter(struct lastlog_iter_type *self)
{
	struct lastlog_node *node;
	PyObject *entry = NULL;

	if (!self->nodes) {
		PyErr_SetNone(PyExc_StopIteration);
		return (NULL);
	}

	/* Consume the node! */

	node = self->nodes;

	entry = pyutmpx_build_lastlog_entry(node);
	if (!entry)
		return (NULL);

	self->nodes = node->next;
	free(node);

	return (entry);
}

/* Entry object definition. */

static PyMethodDef lastlog_iter_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyTypeObject lastlog_iter_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.lastlog_iter_type",
	.tp_doc = "lastlog entries iterator",
	.tp_basicsize = sizeof(struct lastlog_iter_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_lastlog_iter,
	.tp_init = (initproc)init_lastlog_iter,
	.tp_dealloc = (destructor)del_lastlog_iter,
	.tp_iternext = (iternextfunc)next_lastlog_iter,
	.tp_repr = (reprfunc)repr_lastlog_iter,

	/* Members. */

	.tp_methods = lastlog_iter_methods
};

/* ---
 * lastlog object definition.
 * --- */

/* ``lastlog_type``: the main lastlog structure.
 * Doesn't define much. */

struct lastlog_type {
	PyObject_HEAD
};

/* ``lastlog_instance``: the single instance of this type.
 *
 * Only one lastlog_type instance subsists, and it is the one instanciated
 * by default. ``type(pyutmpx.lastlog)()`` will return ``pyutmpx.lastlog``,
 * much like ``None``. */

static struct lastlog_type *lastlog_instance = NULL;

/* `new_lastlog()`: create an instance of lastlog_type.
 * Actually, returns the single instance if already exists. */

static PyObject *new_lastlog(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct lastlog_type *self;

	if (lastlog_instance) {
		Py_XINCREF(lastlog_instance);
		return ((PyObject *)lastlog_instance);
	}

	self = (struct lastlog_type *)type->tp_alloc(type, 0);
	lastlog_instance = self;
	return ((PyObject *)self);
}

/* `init_lastlog()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_lastlog(struct lastlog_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	return (0);
}

/* `del_lastlog()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_lastlog(struct lastlog_type *self)
{
	/* If `self` exists, free it. */

	if (!self)
		return ;

	Py_TYPE(self)->tp_free((PyObject *)self);
	lastlog_instance = NULL;
}

/* `repr_lastlog()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_lastlog(struct lastlog_type *self)
{
	return (Py_BuildValue("s", "pyutmpx.lastlog"));
}

/* `iter_lastlog()`: return self because we are iterable. */

static PyObject *iter_lastlog(struct lastlog_type *self)
{
	return (PyObject_CallObject((PyObject *)&lastlog_iter_type, NULL));
}

/* `get_lastlog_path()`: getter to the `path` property. */

static PyObject *get_lastlog_path(PyObject *self, void *Py_UNUSED(cookie))
{
# ifdef PYUTMPX_LASTLOG_PATH
	return (Py_BuildValue("s", PYUTMPX_LASTLOG_PATH));
# else
	Py_RETURN_NONE;
# endif
}

/* Entry object definition. */

static PyMethodDef lastlog_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyGetSetDef lastlog_getset[] = {
	{
		/* .name = */ "path",
		/* .get = */ (getter)&get_lastlog_path,
		/* .set = */ NULL,
		/* .doc = */ PyDoc_STR(
			"The path to the lastlog database file, if available."
		),
		/* .closure = */ NULL
	},
	{NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject lastlog_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.lastlog_type",
	.tp_doc = PyDoc_STR(
		"lastlog database handle, as an iterable object for reading\n"
		"entries from the lastlog database."
	),
	.tp_basicsize = sizeof(struct lastlog_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_lastlog,
	.tp_init = (initproc)init_lastlog,
	.tp_dealloc = (destructor)del_lastlog,
	.tp_iter = (getiterfunc)iter_lastlog,
	.tp_repr = (reprfunc)repr_lastlog,

	/* Members. */

	.tp_methods = lastlog_methods,
	.tp_getset = lastlog_getset
};

/* ---
 * Module setup.
 * --- */

/* `pyutmpx_init_lastlog_type()`: initialize lastlog type
 * and specific utilities. */

int pyutmpx_init_lastlog_type(PyObject *m)
{
	PyObject *lastlog;

	/* Create the lastlog iterator type. */

	if (PyType_Ready(&lastlog_type) < 0
	 || PyType_Ready(&lastlog_iter_type) < 0)
		goto fail;

	Py_INCREF(&lastlog_type);
	Py_INCREF(&lastlog_iter_type);

	/* Create an instance of the lastlog type and add it
	 * to the module. */

	lastlog = PyObject_CallObject((PyObject *)&lastlog_type, NULL);
	if (!lastlog || PyModule_AddObject(m, "lastlog", lastlog) < 0)
		goto fail;

	return (0);
fail:
	return (-1);
}

/* `pyutmpx_exit_lastlog_type()`: deinitialize lastlog type
 * and specific utilities. */

void pyutmpx_exit_lastlog_type(void)
{
	Py_XDECREF(&lastlog_type);
	Py_XDECREF(&lastlog_iter_type);
}

#endif
