/* ****************************************************************************
 * utmp_type.c -- utmpx file iterator definition.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#if defined(PYUTMPX_HAS_UTMP) && PYUTMPX_HAS_UTMP

/* ---
 * utmp_iter object definition.
 * --- */

/* ``utmp_iter_type``: the main iterator type. */

struct utmp_iter_type {
	PyObject_HEAD

	struct utmp_node *nodes;
};

/* `new_utmp_iter()`: initialize a utmp iterator. */

static PyObject *new_utmp_iter(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct utmp_iter_type *self;

	self = (struct utmp_iter_type *)type->tp_alloc(type, 0);
	return ((PyObject *)self);
}

/* `init_utmp_iter()`: initialize the Python object. */

static int init_utmp_iter(struct utmp_iter_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	/* Load all entries now to avoid having problems with multiple
	 * iterators. */

	if (pyutmpx_get_utmp_nodes(&self->nodes))
		return (-1);

	/* Reset the thing and return. */

	return (0);
}

/* `del_utmp_iter()`: destroy the Python object. */

static void del_utmp_iter(struct utmp_iter_type *self)
{
	if (!self)
		return ;

	while (self->nodes) {
		struct utmp_node *node = self->nodes;

		self->nodes = self->nodes->next;
		free(node);
	}

	Py_TYPE(self)->tp_free((PyObject *)self);
}

/* `repr_utmp_iter()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_utmp_iter(struct utmp_iter_type *Py_UNUSED(self))
{
	return (Py_BuildValue("s", "pyutmpx.utmp_iter_type()"));
}

/* `next_utmp_iter()`: return next element in self. */

static PyObject *next_utmp_iter(struct utmp_iter_type *self)
{
	struct utmp_node *node;
	PyObject *entry = NULL;

	node = self->nodes;
	if (!node) {
		PyErr_SetNone(PyExc_StopIteration);
		return (NULL);
	}

	entry = pyutmpx_build_utmp_entry(node);
	if (!entry)
		return (NULL);

	self->nodes = node->next;
	free(node);

	return (entry);
}

/* Entry object definition. */

static PyMethodDef utmp_iter_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyTypeObject utmp_iter_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.utmp_iter_type",
	.tp_doc = "utmp entries iterator",
	.tp_basicsize = sizeof(struct utmp_iter_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_utmp_iter,
	.tp_init = (initproc)init_utmp_iter,
	.tp_dealloc = (destructor)del_utmp_iter,
	.tp_iternext = (iternextfunc)next_utmp_iter,
	.tp_repr = (reprfunc)repr_utmp_iter,

	/* Members. */

	.tp_methods = utmp_iter_methods
};

/* ---
 * utmp object definition.
 * --- */

/* ``utmp_type``: the main utmp structure.
 * Doesn't define much.
 *
 * TODO: store the path in there? */

struct utmp_type {
	PyObject_HEAD
};

/* ``utmp_instance``: the single instance of this type.
 *
 * Only one utmp_type instance subsists, and it is the one instanciated
 * by default. ``type(pyutmpx.utmp)()`` will return ``pyutmpx.utmp``,
 * much like ``None``. */

static struct utmp_type *utmp_instance = NULL;

/* `new_utmp()`: create an instance of utmp_type.
 * Actually, returns the single instance if already exists. */

static PyObject *new_utmp(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct utmp_type *self;

	if (utmp_instance) {
		Py_XINCREF(utmp_instance);
		return ((PyObject *)utmp_instance);
	}

	self = (struct utmp_type *)type->tp_alloc(type, 0);
	utmp_instance = self;
	return ((PyObject *)self);
}

/* `init_utmp()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_utmp(struct utmp_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	return (0);
}

/* `del_utmp()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_utmp(struct utmp_type *self)
{
	/* If `self` exists, free it. */

	if (!self)
		return ;

	Py_TYPE(self)->tp_free((PyObject *)self);
	utmp_instance = NULL;
}

/* `repr_utmp()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_utmp(struct utmp_type *self)
{
	return (Py_BuildValue("s", "pyutmpx.utmp"));
}

/* `iter_utmp()`: return self because we are iterable. */

static PyObject *iter_utmp(struct utmp_type *self)
{
	return (PyObject_CallObject((PyObject *)&utmp_iter_type, NULL));
}

/* `get_utmp_path()`: getter to the `path` property. */

static PyObject *get_utmp_path(PyObject *self, void *cookie)
{
# ifdef PYUTMPX_UTMP_PATH
	return (Py_BuildValue("s", PYUTMPX_UTMP_PATH));
# else
	Py_RETURN_NONE;
# endif
}

/* Entry object definition. */

static PyMethodDef utmp_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyGetSetDef utmp_getset[] = {
	{
		/* .name = */ "path",
		/* .get = */ (getter)&get_utmp_path,
		/* .set = */ NULL,
		/* .doc = */ PyDoc_STR(
			"The path to the utmp database file, if available."
		),
		/* .closure = */ NULL
	},
	{NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject utmp_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.utmp_type",
	.tp_doc = PyDoc_STR(
		"utmp database handle, as an iterable object for reading\n"
		"entries from the utmp database."
	),
	.tp_basicsize = sizeof(struct utmp_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_utmp,
	.tp_init = (initproc)init_utmp,
	.tp_dealloc = (destructor)del_utmp,
	.tp_iter = (getiterfunc)iter_utmp,
	.tp_repr = (reprfunc)repr_utmp,

	/* Members. */

	.tp_methods = utmp_methods,
	.tp_getset = utmp_getset
};

/* ---
 * Module setup.
 * --- */

/* `pyutmpx_init_utmp_type()`: initialize utmp type
 * and specific utilities. */

int pyutmpx_init_utmp_type(PyObject *m)
{
	PyObject *utmp;

	/* Create the utmp iterator type. */

	if (PyType_Ready(&utmp_type) < 0
	 || PyType_Ready(&utmp_iter_type) < 0)
		goto fail;

	Py_INCREF(&utmp_type);
	Py_INCREF(&utmp_iter_type);

	/* Create an instance of the utmp type and add it
	 * to the module. */

	utmp = PyObject_CallObject((PyObject *)&utmp_type, NULL);
	if (!utmp || PyModule_AddObject(m, "utmp", utmp) < 0)
		goto fail;

	return (0);
fail:
	return (-1);
}

/* `pyutmpx_exit_utmp_type()`: deinitialize utmp type
 * and specific utilities. */

void pyutmpx_exit_utmp_type(void)
{
	Py_XDECREF(&utmp_type);
	Py_XDECREF(&utmp_iter_type);
}

#endif
