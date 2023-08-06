/* ****************************************************************************
 * pyutmpx.h -- pyutmpx module header.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */
#ifndef  PYUTMPX_H
# define PYUTMPX_H 2018020602
# define PY_SSIZE_T_CLEAN 1
# include <Python.h>
# include <pyerrors.h>
# include <structmember.h>
# include <netinet/in.h>
# include <arpa/inet.h>

/* Let's determine platform capabilities using feature macros. */

# if defined(__linux__)
#  include <utmp.h>

/* Linux paths for utmp, wtmp, btmp and lastlog. */

#  define PYUTMPX_UTMP_PATH    _PATH_UTMP
#  define PYUTMPX_WTMP_PATH    _PATH_WTMP
#  ifdef _PATH_BTMP
#   define PYUTMPX_BTMP_PATH   _PATH_BTMP
#  else
#   define PYUTMPX_BTMP_PATH    "/var/log/btmp"
#  endif
#  define PYUTMPX_LASTLOG_PATH _PATH_LASTLOG

/* Linux utmp structure and available elements. */

#  define PYUTMPX_HAS_UTMP_ID      1
#  define PYUTMPX_HAS_UTMP_TYPE    1
#  define PYUTMPX_HAS_UTMP_ADDR_V6 1
#  define PYUTMPX_HAS_UTMP_EXIT    1
#  define PYUTMPX_HAS_UTMP_PID     1
#  define PYUTMPX_HAS_UTMP_SESSION 1
#  define PYUTMPX_HAS_UTMP_TIMEVAL 1
# elif defined(__OpenBSD__)
#  include <utmp.h>

/* OpenBSD paths for utmp, wtmp and lastlog. */

#  define PYUTMPX_UTMP_PATH    _PATH_UTMP
#  define PYUTMPX_WTMP_PATH    _PATH_WTMP
#  define PYUTMPX_LASTLOG_PATH _PATH_LASTLOG

#  define ut_user ut_name
# endif

/* General definitions. */

# ifdef PYUTMPX_UTMP_PATH
#  define PYUTMPX_HAS_UTMP 1
# endif

# ifdef PYUTMPX_WTMP_PATH
#  define PYUTMPX_HAS_WTMP 1
# endif

# ifdef PYUTMPX_BTMP_PATH
#  define PYUTMPX_HAS_BTMP 1
# endif

# ifdef PYUTMPX_LASTLOG_PATH
#  define PYUTMPX_HAS_LASTLOG 1
# endif

/* Platform specific functions for gathering entries. */

struct utmp_exit_status {
	int *termination_code;
	int *status_code;
};

struct utmp_node {
	struct utmp_node *next;

	struct timeval *time;
	struct utmp_exit_status *exit;

	int *type;

	char *id;
	char *user;
	char *host;
	char *line;
	char *addr;

	unsigned long *pid;
	unsigned long *sid;

	Py_ssize_t id_size;
	Py_ssize_t user_size;
	Py_ssize_t host_size;
	Py_ssize_t line_size;
	Py_ssize_t addr_size;

	unsigned long data[]; /* For alignment purposes. */
};

struct lastlog_node {
	struct lastlog_node *next;

	char *host;
	char *line;

	Py_ssize_t host_size;
	Py_ssize_t line_size;

	unsigned long uid;
	struct timeval date;

	char data[];
};

# if defined(PYUTMPX_HAS_UTMP) && PYUTMPX_HAS_UTMP
extern int pyutmpx_get_utmp_nodes(struct utmp_node **nodep);
# endif

# if defined(PYUTMPX_HAS_WTMP) && PYUTMPX_HAS_WTMP
extern int pyutmpx_get_wtmp_nodes(struct utmp_node **nodep);
# endif

# if defined(PYUTMPX_HAS_BTMP) && PYUTMPX_HAS_BTMP
extern int pyutmpx_get_btmp_nodes(struct utmp_node **nodep);
# endif

# if defined(PYUTMPX_HAS_LASTLOG) && PYUTMPX_HAS_LASTLOG
extern int pyutmpx_get_lastlog_nodes(struct lastlog_node **nodep);
# endif

/* Common utilities defined in utils.c. */

extern void pyutmpx_put_str(char **ps, size_t *pn, char const *s);
extern void pyutmpx_put_repr(char **ps, size_t *pn, PyObject *o);

extern Py_ssize_t pyutmpx_get_len(char const *s, Py_ssize_t n);

extern PyObject *pyutmpx_build_datetime(struct timeval const *tv);
extern PyObject *pyutmpx_build_utmp_entry(struct utmp_node const *node);
extern PyObject *pyutmpx_build_lastlog_entry(struct lastlog_node const *node);

/* Common API defined in utmp_entry.c:
 * Define a utmp entry (for utmp and wtmp files). */

# define PYUTMPX_EMPTY          0
# define PYUTMPX_BOOT_TIME      1
# define PYUTMPX_OLD_TIME       2
# define PYUTMPX_NEW_TIME       3
# define PYUTMPX_USER_PROCESS   4
# define PYUTMPX_INIT_PROCESS   5
# define PYUTMPX_LOGIN_PROCESS  6
# define PYUTMPX_DEAD_PROCESS   7
# define PYUTMPX_RUN_LEVEL      8
# define PYUTMPX_ACCOUNTING     9

extern PyTypeObject pyutmpx_exit_status_type;
extern PyTypeObject pyutmpx_utmp_entry_type;
extern PyTypeObject pyutmpx_lastlog_entry_type;

/* Setup and un-setup functions for all modules. */

extern int pyutmpx_init_utils(PyObject *module);
extern void pyutmpx_exit_utils(void);

extern int pyutmpx_init_exit_status_type(PyObject *module);
extern void pyutmpx_exit_exit_status_type(void);

extern int pyutmpx_init_utmp_entry_type(PyObject *module);
extern void pyutmpx_exit_utmp_entry_type(void);

# if defined(PYUTMPX_HAS_UTMP) && PYUTMPX_HAS_UTMP
extern int pyutmpx_init_utmp_type(PyObject *module);
extern void pyutmpx_exit_utmp_type(void);
# endif

# if defined(PYUTMPX_HAS_WTMP) && PYUTMPX_HAS_WTMP
extern int pyutmpx_init_wtmp_type(PyObject *module);
extern void pyutmpx_exit_wtmp_type(void);
# endif

# if defined(PYUTMPX_HAS_BTMP) && PYUTMPX_HAS_BTMP
extern int pyutmpx_init_btmp_type(PyObject *module);
extern void pyutmpx_exit_btmp_type(void);
# endif

extern int pyutmpx_init_lastlog_entry_type(PyObject *module);
extern void pyutmpx_exit_lastlog_entry_type(void);

# if defined(PYUTMPX_HAS_LASTLOG) && PYUTMPX_HAS_LASTLOG
extern int pyutmpx_init_lastlog_type(PyObject *module);
extern void pyutmpx_exit_lastlog_type(void);
# endif

#endif /* PYUTMPX_H */
