/* ****************************************************************************
 * utmp_entry_type.c -- utmp and wtmp entry definition and utilities.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <string.h>
#include <limits.h>

/* Constants representing entry types. */

static PyObject *empty;
static PyObject *boot_time;
static PyObject *old_time;
static PyObject *new_time;
static PyObject *user_process;
static PyObject *init_process;
static PyObject *login_process;
static PyObject *dead_process;
static PyObject *run_level;
static PyObject *accounting;

/* ---
 * Entry object definition.
 * --- */

/* ``entry_type``: the type of the entry. */

struct entry_type {
	PyObject_HEAD

	PyObject *type; /* ut_type */
	PyObject *pid; /* ut_pid */
	PyObject *line; /* ut_line */
	PyObject *id; /* ut_id */
	PyObject *user; /* ut_user */
	PyObject *host; /* ut_host */
	PyObject *exit; /* ut_exit */
	PyObject *sid; /* ut_session */
	PyObject *time; /* ut_tv */
	PyObject *addr; /* ut_addr_v6 */
};

/* `new_entry()`: create the Python object. */

static PyObject *new_entry(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct entry_type *self;

	self = (struct entry_type *)type->tp_alloc(type, 0);

	if (self) {
		self->type = NULL;
		self->pid = NULL;
		self->line = NULL;
		self->id = NULL;
		self->user = NULL;
		self->host = NULL;
		self->exit = NULL;
		self->sid = NULL;
		self->time = NULL;
		self->addr = NULL;
	}

	return ((PyObject *)self);
}

/* `init_entry()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_entry(struct entry_type *self,
	PyObject *args, PyObject *kw)
{
	char *keywords[] = {"type", "pid", "line", "id", "user", "host",
		"exit", "sid", "time", "addr", NULL};

	/* Main parsing and default arguments. */

	if (!PyArg_ParseTupleAndKeywords(args, kw, "|$OOOOOOOOOO", keywords,
		&self->type, &self->pid, &self->line, &self->id, &self->user,
		&self->host, &self->exit, &self->sid, &self->time,  &self->addr))
		return (-1);

	/* Check the arguments.
	 * TODO: check their types too! (here?) */

	if (!self->type)
		self->type = Py_None;
	if (!self->pid)
		self->pid = Py_None;
	if (!self->line)
		self->line = Py_None;
	if (!self->id)
		self->id = Py_None;
	if (!self->user)
		self->user = Py_None;
	if (!self->host)
		self->host = Py_None;
	if (!self->exit)
		self->exit = Py_None;
	if (!self->sid)
		self->sid = Py_None;
	if (!self->time)
		self->time = Py_None;
	if (!self->addr)
		self->addr = Py_None;

	Py_INCREF(self->type);
	Py_INCREF(self->pid);
	Py_INCREF(self->line);
	Py_INCREF(self->id);
	Py_INCREF(self->user);
	Py_INCREF(self->host);
	Py_INCREF(self->exit);
	Py_INCREF(self->sid);
	Py_INCREF(self->time);
	Py_INCREF(self->addr);

	return 0;
}

/* `del_entry()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_entry(struct entry_type *self)
{
	if (!self)
		return;

	Py_XDECREF(self->type);
	Py_XDECREF(self->pid);
	Py_XDECREF(self->line);
	Py_XDECREF(self->id);
	Py_XDECREF(self->user);
	Py_XDECREF(self->host);
	Py_XDECREF(self->exit);
	Py_XDECREF(self->sid);
	Py_XDECREF(self->time);
	Py_XDECREF(self->addr);

	Py_TYPE(self)->tp_free((PyObject*)self);
}

/* ``repr_entry()``: actual C implementation of the ``__repr__`` function
 * for the utmp entry. */

static PyObject *repr_entry(struct entry_type *self)
{
	char buf[1024], *s = buf, *type_name;
	size_t len = 1024;
	int type, haslast = 0;

#define prop(PROP, NAME) \
	if ((NAME) != Py_None) { \
		if (haslast) \
			pyutmpx_put_str(&s, &len, ", "); \
		pyutmpx_put_str(&s, &len, PROP " = "); \
		if (!(NAME)) \
			pyutmpx_put_str(&s, &len, "(NULL)"); \
		else \
			pyutmpx_put_repr(&s, &len, NAME); \
		haslast = 1; \
	}

	pyutmpx_put_str(&s, &len, "pyutmpx.utmp_entry(");

	if (PyObject_IsTrue(self->type)) {
		if (PyArg_Parse(self->type, "i", &type) < 0)
			type = 0;

		switch (type) {
		case PYUTMPX_EMPTY:
			type_name = "pyutmpx.EMPTY";
			break;
		case PYUTMPX_BOOT_TIME:
			type_name = "pyutmpx.BOOT_TIME";
			break;
		case PYUTMPX_OLD_TIME:
			type_name = "pyutmpx.OLD_TIME";
			break;
		case PYUTMPX_NEW_TIME:
			type_name = "pyutmpx.NEW_TIME";
			break;
		case PYUTMPX_USER_PROCESS:
			type_name = "pyutmpx.USER_PROCESS";
			break;
		case PYUTMPX_INIT_PROCESS:
			type_name = "pyutmpx.INIT_PROCESS";
			break;
		case PYUTMPX_LOGIN_PROCESS:
			type_name = "pyutmpx.LOGIN_PROCESS";
			break;
		case PYUTMPX_DEAD_PROCESS:
			type_name = "pyutmpx.DEAD_PROCESS";
			break;
		case PYUTMPX_RUN_LEVEL:
			type_name = "pyutmpx.RUN_LEVEL";
			break;
		case PYUTMPX_ACCOUNTING:
			type_name = "pyutmpx.ACCOUNTING";
			break;
		default:
			type_name = "(unknown)";
		}

		pyutmpx_put_str(&s, &len, "type = ");
		pyutmpx_put_str(&s, &len, type_name);
		haslast = 1;
	}

	prop("pid",  self->pid)
	prop("line", self->line)
	prop("id",   self->id)
	prop("user", self->user)
	prop("host", self->host)
	prop("exit", self->exit)
	prop("sid",  self->sid)
	prop("time", self->time)
	prop("addr", self->addr)

	pyutmpx_put_str(&s, &len, ")");

	return (Py_BuildValue("s", buf));
}

/* Entry object definition. */

static PyMethodDef entry_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyMemberDef entry_members[] = {
	{
		/* .name = */ "type",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, type),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The type of the entry, amongst the following constants:\n"
			"\n"

			":py:data:`pyutmpx.EMPTY`\n"
			"\tNo valid user accounting information.\n"
			"\n"

			":py:data:`pyutmpx.BOOT_TIME`\n"
			"\tIdentifies time of system boot.\n"
			"\n"

			":py:data:`pyutmpx.OLD_TIME`\n"
			"\tIdentifies time when system clock changed.\n"
			"\n"

			":py:data:`pyutmpx.NEW_TIME`\n"
			"\tIdentifies time after system clock changed.\n"
			"\n"

			":py:data:`pyutmpx.USER_PROCESS`\n"
			"\tIdentifies a process.\n"
			"\n"

			":py:data:`pyutmpx.INIT_PROCESS`\n"
			"\tIdentifies a process spawned by the init process.\n"
			"\n"

			":py:data:`pyutmpx.LOGIN_PROCESS`\n"
			"\tIdentifies a session leader of a logged-in user.\n"
			"\n"

			":py:data:`pyutmpx.DEAD_PROCESS`\n"
			"\tIdentifies a session leader who has exited.\n"
			"\n"

			":py:data:`pyutmpx.RUN_LEVEL`\n"
			"\tIdentifies a change in system run-level; refer to init(1)\n"
			"\tfor more information.\n"
			"\n"

			":py:data:`pyutmpx.ACCOUNTING`\n"
			"\tNo information available.\n"
			"\n"

			"This field is populated using the ``ut->ut_type`` field,\n"
			"when available."
		)
	},
	{
		/* .name = */ "pid",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, pid),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The process identifier (pid), for process or session leader\n"
			"related events.\n"
			"\n"
			"This field is populated using the ``ut->ut_pid`` field,\n"
			"when available."
		)
	},
	{
		/* .name = */ "line",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, line),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The line or device on which the event has occurred.\n"
			"\n"
			"This field is populated using the ``ut->ut_line`` field."
		)
	},
	{
		/* .name = */ "id",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, id),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The unspecified initialization process identifier.\n"
			"\n"
			"This field is populated using the ``ut->ut_id`` field,\n"
			"when available."
		)
	},
	{
		/* .name = */ "user",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, user),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The login name of the user involved in the event.\n"
			"\n"
			"This field is populated using the ``ut->ut_user`` or\n"
			"``ut->ut_name`` fields."
		)
	},
	{
		/* .name = */ "host",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, host),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The name of the remote host from which the event has occurred\n"
			"in the case of remote logins, or the kernel version for other\n"
			"system-related events.\n"
			"\n"
			"This field is populated using the ``ut->ut_host`` field,\n"
			"when available."
		)
	},
	{
		/* .name = */ "exit",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, exit),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The exit status of the process or session leader on\n"
			"dead process events, as a :py:class:`pyutmpx.exit_status`\n"
			"instance.\n"
			"\n"
			"This field is populated using the ``ut->ut_exit`` field,\n"
			"when available."
		)
	},
	{
		/* .name = */ "sid",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, sid),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The session identifier (sid) of the process, used for\n"
			"windowing.\n"
			"\n"
			"This field is populated using the ``ut->ut_session`` field,\n"
			"when available. Refer to getsid(2) for more information."
		)
	},
	{
		/* .name = */ "time",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, time),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The time at which the entry was added to the database, as\n"
			"a datetime using the UTC timezone.\n"
			"\n"
			"This field is populated using the ``ut->ut_tv``,\n"
			"``ut->ut_time`` or ``ut->ut_xtime`` fields, when available."
		)
	},
	{
		/* .name = */ "addr",
		/* .type = */ T_OBJECT,
		/* .offset = */ offsetof(struct entry_type, addr),
		/* .flags = */ READONLY,
		/* .doc = */ PyDoc_STR(
			"The IPv4 or IPv6 address of the host in case of remote logins,\n"
			"as a string.\n"
			"\n"
			"This field is populated using the ``ut->ut_addr_v6`` or\n"
			"``ut->ut_addr`` fields, when available."
		)
	},

	{NULL}
};

PyTypeObject pyutmpx_utmp_entry_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.utmp_entry",
	.tp_doc = PyDoc_STR(
		"utmp entry representation, as described by either the\n"
		"``struct utmp`` type defined in ``<utmp.h>`` or the\n"
		"``struct utmpx`` type defined in ``<utmpx.h>``."
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

/* `pyutmpx_init_utmp_entry_type()`: setup utmp entries and utilities at
 * module-level for further usage. */

#define SETUP_CONST(STATIC_NAME, VALUE, IN_MODULE_NAME) \
	{ \
		if (!(STATIC_NAME = Py_BuildValue("i", VALUE))) \
			return -1; \
		if (PyModule_AddObject(m, IN_MODULE_NAME, STATIC_NAME) < 0) { \
			Py_XDECREF(STATIC_NAME); \
			return -1; \
		} \
	}

int pyutmpx_init_utmp_entry_type(PyObject *m)
{
	/* Create the utmp constants. */

	SETUP_CONST(empty,         PYUTMPX_EMPTY,         "EMPTY")
	SETUP_CONST(boot_time,     PYUTMPX_BOOT_TIME,     "BOOT_TIME")
	SETUP_CONST(old_time,      PYUTMPX_OLD_TIME,      "OLD_TIME")
	SETUP_CONST(new_time,      PYUTMPX_NEW_TIME,      "NEW_TIME")
	SETUP_CONST(user_process,  PYUTMPX_USER_PROCESS,  "USER_PROCESS")
	SETUP_CONST(init_process,  PYUTMPX_INIT_PROCESS,  "INIT_PROCESS")
	SETUP_CONST(login_process, PYUTMPX_LOGIN_PROCESS, "LOGIN_PROCESS")
	SETUP_CONST(dead_process,  PYUTMPX_DEAD_PROCESS,  "DEAD_PROCESS")
	SETUP_CONST(run_level,     PYUTMPX_RUN_LEVEL,     "RUN_LEVEL")
	SETUP_CONST(accounting,    PYUTMPX_ACCOUNTING,    "ACCOUNTING")

	/* Create the utmp entry type to the module. */

	if (PyType_Ready(&pyutmpx_utmp_entry_type) < 0)
		return -1;

	Py_INCREF((PyObject *)&pyutmpx_utmp_entry_type);
	if (PyModule_AddObject(m, "utmp_entry",
		(PyObject *)&pyutmpx_utmp_entry_type) < 0) {
		Py_DECREF(&pyutmpx_utmp_entry_type);
		return -1;
	}

	/* Prepare types. */

	return 0;
}

/* `pyutmpx_exit_utmp_entry_type()`: deinitialize exit status type
 * and specific utilities. */

void pyutmpx_exit_utmp_entry_type(void)
{
	/* Nothing to do here. */
}
