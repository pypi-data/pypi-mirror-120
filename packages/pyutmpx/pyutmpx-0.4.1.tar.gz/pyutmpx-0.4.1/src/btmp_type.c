/* ****************************************************************************
 * btmp_type.c -- btmpx file iterator definition.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#if defined(PYUTMPX_HAS_BTMP) && PYUTMPX_HAS_BTMP

/* ---
 * btmp_iter object definition.
 * --- */

/* ``btmp_iter_type``: the main iterator type. */

struct btmp_iter_type {
	PyObject_HEAD

	struct utmp_node *nodes;
};

/* `new_btmp_iter()`: initialize a utmp iterator. */

static PyObject *new_btmp_iter(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct btmp_iter_type *self;

	self = (struct btmp_iter_type *)type->tp_alloc(type, 0);
	return ((PyObject *)self);
}

/* `init_btmp_iter()`: initialize the Python object. */

static int init_btmp_iter(struct btmp_iter_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	/* Load all entries now to avoid having problems with multiple
	 * iterators. */

	if (pyutmpx_get_btmp_nodes(&self->nodes))
		return (-1);

	/* Reset the thing and return. */

	return (0);
}

/* `del_btmp_iter()`: destroy the Python object. */

static void del_btmp_iter(struct btmp_iter_type *self)
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

/* `repr_btmp_iter()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_btmp_iter(struct btmp_iter_type *Py_UNUSED(self))
{
	return (Py_BuildValue("s", "pyutmpx.btmp_iter_type()"));
}

/* `next_btmp_iter()`: return next element in self. */

static PyObject *next_btmp_iter(struct btmp_iter_type *self)
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

static PyMethodDef btmp_iter_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyTypeObject btmp_iter_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.btmp_iter_type",
	.tp_doc = "btmp entries iterator",
	.tp_basicsize = sizeof(struct btmp_iter_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_btmp_iter,
	.tp_init = (initproc)init_btmp_iter,
	.tp_dealloc = (destructor)del_btmp_iter,
	.tp_iternext = (iternextfunc)next_btmp_iter,
	.tp_repr = (reprfunc)repr_btmp_iter,

	/* Members. */

	.tp_methods = btmp_iter_methods
};

/* ---
 * btmp object definition.
 * --- */

/* ``btmp_type``: the main utmp structure.
 * Doesn't define much.
 *
 * TODO: store the path in there? */

struct btmp_type {
	PyObject_HEAD
};

/* ``btmp_instance``: the single instance of this type.
 *
 * Only one btmp_type instance subsists, and it is the one instanciated
 * by default. ``type(pyutmpx.btmp)()`` will return ``pyutmpx.btmp``,
 * much like ``None``. */

static struct btmp_type *btmp_instance = NULL;

/* `new_btmp()`: create an instance of btmp_type.
 * Actually, returns the single instance if already exists. */

static PyObject *new_btmp(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct btmp_type *self;

	if (btmp_instance) {
		Py_XINCREF(btmp_instance);
		return ((PyObject *)btmp_instance);
	}

	self = (struct btmp_type *)type->tp_alloc(type, 0);
	btmp_instance = self;
	return ((PyObject *)self);
}

/* `init_btmp()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_btmp(struct btmp_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	return (0);
}

/* `del_btmp()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_btmp(struct btmp_type *self)
{
	/* If `self` exists, free it. */

	if (!self)
		return ;

	Py_TYPE(self)->tp_free((PyObject *)self);
	btmp_instance = NULL;
}

/* `repr_btmp()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_btmp(struct btmp_type *self)
{
	return (Py_BuildValue("s", "pyutmpx.btmp"));
}

/* `iter_btmp()`: return self because we are iterable. */

static PyObject *iter_btmp(struct btmp_type *self)
{
	return (PyObject_CallObject((PyObject *)&btmp_iter_type, NULL));
}

/* `get_btmp_path()`: getter to the `path` property. */

static PyObject *get_btmp_path(PyObject *self, void *cookie)
{
# ifdef PYUTMPX_BTMP_PATH
	return (Py_BuildValue("s", PYUTMPX_BTMP_PATH));
# else
	Py_RETURN_NONE;
# endif
}

/* Entry object definition. */

static PyMethodDef btmp_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyGetSetDef btmp_getset[] = {
	{
		/* .name = */ "path",
		/* .get = */ (getter)&get_btmp_path,
		/* .set = */ NULL,
		/* .doc = */ PyDoc_STR(
			"The path to the btmp database file, if available."
		),
		/* .closure = */ NULL
	},
	{NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject btmp_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.btmp_type",
	.tp_doc = PyDoc_STR(
		"btmp database handle, as an iterable object for reading\n"
		"entries from the btmp database."
	),
	.tp_basicsize = sizeof(struct btmp_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_btmp,
	.tp_init = (initproc)init_btmp,
	.tp_dealloc = (destructor)del_btmp,
	.tp_iter = (getiterfunc)iter_btmp,
	.tp_repr = (reprfunc)repr_btmp,

	/* Members. */

	.tp_methods = btmp_methods,
	.tp_getset = btmp_getset
};

/* ---
 * Module setup.
 * --- */

/* `pyutmpx_init_btmp_type()`: initialize utmp type
 * and specific utilities. */

int pyutmpx_init_btmp_type(PyObject *m)
{
	PyObject *btmp;

	/* Create the utmp iterator type. */

	if (PyType_Ready(&btmp_type) < 0
	 || PyType_Ready(&btmp_iter_type) < 0)
		goto fail;

	Py_INCREF(&btmp_type);
	Py_INCREF(&btmp_iter_type);

	/* Create an instance of the utmp type and add it
	 * to the module. */

	btmp = PyObject_CallObject((PyObject *)&btmp_type, NULL);
	if (!btmp || PyModule_AddObject(m, "btmp", btmp) < 0)
		goto fail;

	return (0);
fail:
	return (-1);
}

/* `pyutmpx_exit_btmp_type()`: deinitialize btmp type
 * and specific utilities. */

void pyutmpx_exit_btmp_type(void)
{
	Py_XDECREF(&btmp_type);
	Py_XDECREF(&btmp_iter_type);
}

#endif
