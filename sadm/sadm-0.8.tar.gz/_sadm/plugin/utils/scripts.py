# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path
from subprocess import call

from _sadm import log, libdir
from _sadm.errors import PluginScriptNotFound, PluginScriptNoExec

__all__ = ['Scripts']

_TTL = 180

class Scripts(object):
	_dir = None

	def __init__(self, *dirparts):
		d = libdir.path('plugin', *dirparts)
		self._dir = path.join(d, 'scripts')

	def run(self, script, *args):
		spath = path.join(self._dir, script)
		log.debug("run %s %s" % (spath, args))
		s = _Script(spath, args)
		return s.dispatch()

class _Script(object):
	_cmd = None

	def __init__(self, script, *args):
		self._cmd = [script]
		self._cmd.extend(*args)

	def dispatch(self):
		try:
			return call(self._cmd, timeout = _TTL)
		except FileNotFoundError:
			raise PluginScriptNotFound(self._cmd[0])
		except PermissionError:
			raise PluginScriptNoExec(self._cmd[0])
