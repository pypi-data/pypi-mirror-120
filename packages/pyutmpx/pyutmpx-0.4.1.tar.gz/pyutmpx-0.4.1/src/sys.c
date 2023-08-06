/* ****************************************************************************
 * sys.c -- system-specific implementation.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>

/* ---
 * utmp, wtmp and btmp raw entries gathering.
 * --- */

#if defined(PYUTMPX_UTMP_PATH) || defined(PYUTMPX_WTMP_PATH) \
	|| defined(PYUTMPX_BTMP_PATH)

struct utmp_node_data {
	int type;
	int exit_termination_code;
	int exit_status_code;

	unsigned long pid;
	unsigned long sid;

	struct timeval time;
	struct utmp_exit_status exit;

	char data[];
};

/* ``get_utmp_node()``: get a utmp node for GNU/Linux. */

static struct utmp_node *get_utmp_node(struct utmp const *ent)
{
	int type;
	char formatted_addr[100];
	char const *addr;
	Py_ssize_t id_len, user_len, host_len, line_len, addr_len;
	struct utmp_node *node;
	size_t node_size;

	/* Get the entry type. */

# if defined(PYUTMPX_HAS_UTMP_TYPE) && PYUTMPX_HAS_UTMP_TYPE
	switch (ent->ut_type) {
#  ifdef EMPTY
	case EMPTY:
		type = PYUTMPX_EMPTY;
		break;
#  endif
#  ifdef BOOT_TIME
	case BOOT_TIME:
		type = PYUTMPX_BOOT_TIME;
		break;
#  endif
#  ifdef OLD_TIME
	case OLD_TIME:
		type = PYUTMPX_OLD_TIME;
		break;
#  endif
#  ifdef NEW_TIME
	case NEW_TIME:
		type = PYUTMPX_NEW_TIME;
		break;
#  endif
#  ifdef USER_PROCESS
	case USER_PROCESS:
		type = PYUTMPX_USER_PROCESS;
		break;
#  endif
#  ifdef INIT_PROCESS
	case INIT_PROCESS:
		type = PYUTMPX_INIT_PROCESS;
		break;
#  endif
#  ifdef LOGIN_PROCESS
	case LOGIN_PROCESS:
		type = PYUTMPX_LOGIN_PROCESS;
		break;
#  endif
#  ifdef DEAD_PROCESS
	case DEAD_PROCESS:
		type = PYUTMPX_DEAD_PROCESS;
		break;
#  endif
#  ifdef RUN_LVL
	case RUN_LVL:
		type = PYUTMPX_RUN_LEVEL;
		break;
#  endif
#  ifdef RUN_LEVEL
	case RUN_LEVEL:
		type = PYUTMPX_RUN_LEVEL;
		break;
#  endif
#  ifdef ACCOUNTING
	case ACCOUNTING:
		type = PYUTMPX_ACCOUNTING;
		break;
#  endif
	default:
		return NULL;
	}
# endif

	/* Prepare the address. */

	addr = NULL;

# if defined(PYUTMPX_HAS_UTMP_ADDR_V6) && PYUTMPX_HAS_UTMP_ADDR_V6
	if (ent->ut_addr_v6[1] || ent->ut_addr_v6[2] || ent->ut_addr_v6[3])
		addr = inet_ntop(AF_INET6, &ent->ut_addr_v6,
			formatted_addr, sizeof formatted_addr);
	else if (ent->ut_addr_v6[0])
		addr = inet_ntop(AF_INET, &ent->ut_addr_v6,
			formatted_addr, sizeof formatted_addr);
# endif

	if (!addr)
		addr = "";

	/* Get the lengths. */

# if defined(PYUTMPX_HAS_UTMP_ID) && PYUTMPX_HAS_UTMP_ID
	id_len = pyutmpx_get_len(ent->ut_id, 4);
# else
	id_len = 0;
# endif

	user_len = pyutmpx_get_len(ent->ut_user, sizeof ent->ut_user);
	host_len = pyutmpx_get_len(ent->ut_host, sizeof ent->ut_host);
	line_len = pyutmpx_get_len(ent->ut_line, sizeof ent->ut_line);
	addr_len = strlen(addr);

	/* Allocate the node. */

	node_size = sizeof(struct utmp_node)
		+ sizeof(struct utmp_node_data)
		+ id_len + user_len + host_len + line_len + addr_len;
	node = malloc(node_size);
	if (!node)
		return 0; /* We quit cowardly, pretenting nothing follows. */

	memset(node, 0, node_size);

	node->next = NULL;

	{
		struct utmp_node_data *data = (struct utmp_node_data *)&node->data;

# if defined(PYUTMPX_HAS_UTMP_TYPE) && PYUTMPX_HAS_UTMP_TYPE
		node->type = &data->type;
		data->type = type;
# endif

# if defined(PYUTMPX_HAS_UTMP_EXIT) && PYUTMPX_HAS_UTMP_EXIT
		if (type == PYUTMPX_DEAD_PROCESS) {
			node->exit = &data->exit;
			node->exit->termination_code = &data->exit_termination_code;
			node->exit->status_code = &data->exit_status_code;

			data->exit_termination_code = ent->ut_exit.e_termination;
			data->exit_status_code = ent->ut_exit.e_exit;
		}
# endif

# if defined(PYUTMPX_HAS_UTMP_PID) && PYUTMPX_HAS_UTMP_PID
		node->pid = &data->pid;
		data->pid = ent->ut_pid;
# endif

# if defined(PYUTMPX_HAS_UTMP_SESSION) && PYUTMPX_HAS_UTMP_SESSION
		node->sid = &data->sid;
		data->sid = ent->ut_session;
# endif

		node->time = &data->time;
# if defined(PYUTMPX_HAS_UTMP_TIMEVAL) && PYUTMPX_HAS_UTMP_TIMEVAL
		data->time.tv_sec = ent->ut_tv.tv_sec;
		data->time.tv_usec = ent->ut_tv.tv_usec;
# else
		data->time.tv_sec = ent->ut_time;
		data->time.tv_usec = 0;
# endif

		node->id = data->data;
		node->user = node->id + id_len;
		node->host = node->user + user_len;
		node->line = node->host + host_len;
		node->addr = node->line + line_len;

		node->id_size = id_len;
		node->user_size = user_len;
		node->host_size = host_len;
		node->line_size = line_len;
		node->addr_size = addr_len;

# if defined(PYUTMPX_HAS_UTMP_ID) && PYUTMPX_HAS_UTMP_ID
		if (id_len)
			memcpy(node->id, ent->ut_id, id_len);
# else
		node->id = NULL;
# endif

		if (user_len)
			memcpy(node->user, ent->ut_user, user_len);
		if (host_len)
			memcpy(node->host, ent->ut_host, host_len);
		if (line_len)
			memcpy(node->line, ent->ut_line, line_len);

# if defined(PYUTMPX_HAS_UTMP_ADDR_V6) && PYUTMPX_HAS_UTMP_ADDR_V6
		if (addr_len)
			memcpy(node->addr, addr, addr_len);
# else
		node->addr = NULL;
# endif
	}

	return (node);
}

static int get_utmp_nodes(struct utmp_node **nodep, char const *path)
{
	struct utmp_node *node, **inodep;
	struct utmp arr[500];
	char *arrp = (char *)&arr;
	size_t offset = 0;
	int fd;

	inodep = nodep;
	*nodep = NULL;

	fd = open(path, O_RDONLY, 0);
	if (fd < 0) {
		PyErr_SetFromErrnoWithFilename(PyExc_OSError, path);
		return -1;
	}

	while (1) {
		size_t arr_size, full_size;
		ssize_t read_size;

		read_size = read(fd, &arrp[offset],
			sizeof (arr) - offset);
		if (read_size < 0) {
			close(fd);
			while (*inodep) {
				node = *inodep;
				inodep = &node->next;
				free(node);
			}

			PyErr_SetFromErrnoWithFilename(PyExc_OSError, path);
			return -1;
		}

		if (!read_size)
			break; /* End of file! */

		full_size = read_size - read_size % sizeof (arr[0]);
		arr_size = full_size / sizeof (arr[0]);
		for (size_t i = 0; i < arr_size; i++) {
			/* If the entry is all zeroes, ignore it. */

			{
				char const *start = (char const *)&arr[i];
				char const *end = ((char const *)&arr[i + 1]) - 1;
				int all_zeroes = 1;

				for (; start < end; start++) {
					if (!*start)
						continue;

					all_zeroes = 0;
					break;
				}

				if (all_zeroes)
					continue ;
			}

			/* Get the node out of it. */

			node = get_utmp_node(&arr[i]);
			if (node) {
				*nodep = node;
				nodep = &node->next;
			}
		}

		read_size -= full_size;
		offset = 0;
		if (read_size) {
			memcpy(arrp, &arrp[full_size], read_size);
			offset = read_size;
		}
	}

	close(fd);

	if (offset) {
		while (*inodep) {
			node = *inodep;
			inodep = &node->next;
			free(node);
		}

		PyErr_SetString(PyExc_OSError,
			"Incomplete entry at end of file");
		return -1;
	}

	return 0;
}

# define UTMP_FILE_READER(FUNC_NAME, PATH) \
int FUNC_NAME(struct utmp_node **nodep) \
{ \
	return get_utmp_nodes(nodep, PATH); \
}

# if defined(PYUTMPX_UTMP_PATH)
UTMP_FILE_READER(pyutmpx_get_utmp_nodes, PYUTMPX_UTMP_PATH)
# endif

# if defined(PYUTMPX_WTMP_PATH)
UTMP_FILE_READER(pyutmpx_get_wtmp_nodes, PYUTMPX_WTMP_PATH)
# endif

# if defined(PYUTMPX_BTMP_PATH)
UTMP_FILE_READER(pyutmpx_get_btmp_nodes, PYUTMPX_BTMP_PATH)
# endif
#endif

/* ---
 * lastlog entries gathering.
 * --- */

/* `pyutmpx_get_lastlog_nodes()`: gather last nodes. */

int pyutmpx_get_lastlog_nodes(struct lastlog_node **nodep)
{
	struct lastlog_node *node, **inodep;
	struct lastlog arr[500];
	char *arrp = (char *)&arr;
	size_t offset = 0;
	int fd;

	inodep = nodep;
	*nodep = NULL;

	fd = open(_PATH_LASTLOG, O_RDONLY, 0);
	if (fd < 0) {
		PyErr_SetFromErrnoWithFilename(PyExc_OSError, _PATH_LASTLOG);
		return -1;
	}

	for (unsigned long uid_start = 0;;) {
		size_t arr_size, full_size;
		ssize_t read_size;

		read_size = read(fd, &arrp[offset], sizeof (arr) - offset);
		if (read_size < 0) {
			close(fd);
			while (*inodep) {
				node = *inodep;
				inodep = &node->next;
				free(node);
			}

			PyErr_SetFromErrnoWithFilename(PyExc_OSError, _PATH_LASTLOG);
			return -1;
		}

		if (!read_size)
			break; /* End of file! */

		full_size = read_size - read_size % sizeof (arr[0]);
		arr_size = full_size / sizeof (arr[0]);

		for (unsigned long uid_off = 0; uid_off < arr_size; uid_off++) {
			unsigned long uid = uid_start + uid_off;
			struct lastlog *ll = &arr[uid_off];
			Py_ssize_t host_len, line_len;

			if (!ll->ll_time)
				continue;

			/* This entry exists! Let's create our node. */

			host_len = pyutmpx_get_len(ll->ll_host, UT_HOSTSIZE);
			line_len = pyutmpx_get_len(ll->ll_line, UT_LINESIZE);

			node = malloc(sizeof(struct lastlog_node)
				+ host_len + line_len);
			if (!node)
				return 0; /* Escape cowardly. */

			node->uid = uid;
			node->date.tv_sec = ll->ll_time;
			node->next = NULL;

			node->host = node->data;
			node->line = node->host + host_len;

			node->host_size = host_len;
			node->line_size = line_len;

			memcpy(node->host, ll->ll_host, host_len);
			memcpy(node->line, ll->ll_line, line_len);

			*nodep = node;
			nodep = &node->next;
		}

		read_size -= full_size;
		offset = 0;
		if (read_size) {
			memcpy(arrp, &arrp[full_size], read_size);
			offset = read_size;
		}

		uid_start += arr_size;
	}

	close(fd);

	if (offset) {
		while (*inodep) {
			node = *inodep;
			inodep = &node->next;
			free(node);
		}

		PyErr_SetString(PyExc_OSError, "Incomplete entry at end of file");
		return -1;
	}

	return 0;
}
