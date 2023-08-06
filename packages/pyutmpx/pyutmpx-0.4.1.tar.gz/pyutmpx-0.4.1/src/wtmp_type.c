/* ****************************************************************************
 * wtmp_type.c -- wtmpx file iterator definition.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#if defined(PYUTMPX_HAS_WTMP) && PYUTMPX_HAS_WTMP

/* ---
 * wtmp_iter object definition.
 * --- */

/* ``wtmp_iter_type``: the main iterator type. */

struct wtmp_iter_type {
	PyObject_HEAD

	struct utmp_node *nodes;
};

/* `new_wtmp_iter()`: initialize a utmp iterator. */

static PyObject *new_wtmp_iter(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct wtmp_iter_type *self;

	self = (struct wtmp_iter_type *)type->tp_alloc(type, 0);
	return ((PyObject *)self);
}

/* `init_wtmp_iter()`: initialize the Python object. */

static int init_wtmp_iter(struct wtmp_iter_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	/* Load all entries now to avoid having problems with multiple
	 * iterators. */

	if (pyutmpx_get_wtmp_nodes(&self->nodes))
		return (-1);

	/* Reset the thing and return. */

	return (0);
}

/* `del_wtmp_iter()`: destroy the Python object. */

static void del_wtmp_iter(struct wtmp_iter_type *self)
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

/* `repr_wtmp_iter()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_wtmp_iter(struct wtmp_iter_type *Py_UNUSED(self))
{
	return (Py_BuildValue("s", "pyutmpx.wtmp_iter_type()"));
}

/* `next_wtmp_iter()`: return next element in self. */

static PyObject *next_wtmp_iter(struct wtmp_iter_type *self)
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

static PyMethodDef wtmp_iter_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyTypeObject wtmp_iter_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.wtmp_iter_type",
	.tp_doc = "wtmp entries iterator",
	.tp_basicsize = sizeof(struct wtmp_iter_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_wtmp_iter,
	.tp_init = (initproc)init_wtmp_iter,
	.tp_dealloc = (destructor)del_wtmp_iter,
	.tp_iternext = (iternextfunc)next_wtmp_iter,
	.tp_repr = (reprfunc)repr_wtmp_iter,

	/* Members. */

	.tp_methods = wtmp_iter_methods
};

/* ---
 * wtmp object definition.
 * --- */

/* ``wtmp_type``: the main utmp structure.
 * Doesn't define much.
 *
 * TODO: store the path in there? */

struct wtmp_type {
	PyObject_HEAD
};

/* ``wtmp_instance``: the single instance of this type.
 *
 * Only one wtmp_type instance subsists, and it is the one instanciated
 * by default. ``type(pyutmpx.wtmp)()`` will return ``pyutmpx.wtmp``,
 * much like ``None``. */

static struct wtmp_type *wtmp_instance = NULL;

/* `new_wtmp()`: create an instance of wtmp_type.
 * Actually, returns the single instance if already exists. */

static PyObject *new_wtmp(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct wtmp_type *self;

	if (wtmp_instance) {
		Py_XINCREF(wtmp_instance);
		return ((PyObject *)wtmp_instance);
	}

	self = (struct wtmp_type *)type->tp_alloc(type, 0);
	wtmp_instance = self;
	return ((PyObject *)self);
}

/* `init_wtmp()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_wtmp(struct wtmp_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	return (0);
}

/* `del_wtmp()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_wtmp(struct wtmp_type *self)
{
	/* If `self` exists, free it. */

	if (!self)
		return ;

	Py_TYPE(self)->tp_free((PyObject *)self);
	wtmp_instance = NULL;
}

/* `repr_wtmp()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_wtmp(struct wtmp_type *self)
{
	return (Py_BuildValue("s", "pyutmpx.wtmp"));
}

/* `iter_wtmp()`: return self because we are iterable. */

static PyObject *iter_wtmp(struct wtmp_type *self)
{
	return (PyObject_CallObject((PyObject *)&wtmp_iter_type, NULL));
}

/* `get_wtmp_path()`: getter to the `path` property. */

static PyObject *get_wtmp_path(PyObject *self, void *cookie)
{
# ifdef PYUTMPX_WTMP_PATH
	return (Py_BuildValue("s", PYUTMPX_WTMP_PATH));
# else
	Py_RETURN_NONE;
# endif
}

/* Entry object definition. */

static PyMethodDef wtmp_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyGetSetDef wtmp_getset[] = {
	{
		/* .name = */ "path",
		/* .get = */ (getter)&get_wtmp_path,
		/* .set = */ NULL,
		/* .doc = */ PyDoc_STR(
			"The path to the wtmp database file, if available."
		),
		/* .closure = */ NULL
	},
	{NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject wtmp_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.wtmp_type",
	.tp_doc = PyDoc_STR(
		"wtmp database handle, as an iterable object for reading\n"
		"entries from the wtmp database."
	),
	.tp_basicsize = sizeof(struct wtmp_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_wtmp,
	.tp_init = (initproc)init_wtmp,
	.tp_dealloc = (destructor)del_wtmp,
	.tp_iter = (getiterfunc)iter_wtmp,
	.tp_repr = (reprfunc)repr_wtmp,

	/* Members. */

	.tp_methods = wtmp_methods,
	.tp_getset = wtmp_getset
};

/* ---
 * Module setup.
 * --- */

/* `pyutmpx_init_wtmp_type()`: initialize utmp type
 * and specific utilities. */

int pyutmpx_init_wtmp_type(PyObject *m)
{
	PyObject *wtmp;

	/* Create the utmp iterator type. */

	if (PyType_Ready(&wtmp_type) < 0
	 || PyType_Ready(&wtmp_iter_type) < 0)
		goto fail;

	Py_INCREF(&wtmp_type);
	Py_INCREF(&wtmp_iter_type);

	/* Create an instance of the utmp type and add it
	 * to the module. */

	wtmp = PyObject_CallObject((PyObject *)&wtmp_type, NULL);
	if (!wtmp || PyModule_AddObject(m, "wtmp", wtmp) < 0)
		goto fail;

	return (0);
fail:
	return (-1);
}

/* `pyutmpx_exit_wtmp_type()`: deinitialize wtmp type
 * and specific utilities. */

void pyutmpx_exit_wtmp_type(void)
{
	Py_XDECREF(&wtmp_type);
	Py_XDECREF(&wtmp_iter_type);
}

#endif
