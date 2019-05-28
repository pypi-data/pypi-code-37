# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from pytest import raises

from _sadm import libdir
from _sadm.errors import PluginError, PluginScriptNotFound, PluginScriptNoExec
from _sadm.plugin.utils import scripts

s = scripts.Scripts('testing')

def test_scripts_dir():
	assert s._dir == libdir.path('plugin', 'testing', 'scripts')

def test_noscript():
	spath = libdir.path('plugin', 'testing', 'scripts', 'noscript.sh')
	with raises(PluginScriptNotFound, match = "PluginScriptNotFound: %s" % spath) as err:
		s.run('noscript.sh')
	assert err.errisinstance(PluginError)

def test_run():
	rc = s.run('testing.sh')
	assert rc == 0

def test_run_error():
	rc = s.run('testing-error.sh')
	assert rc == 1

def test_run_noexec():
	spath = libdir.path('plugin', 'testing', 'scripts', 'testing-noexec.sh')
	with raises(PluginScriptNoExec, match = "PluginScriptNoExec: %s" % spath) as err:
		s.run('testing-noexec.sh')
	assert err.errisinstance(PluginError)
