# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path

from _sadm import log, env

_cfgfile = path.join(path.sep, 'etc', 'opt', 'sadm', 'deploy.cfg')

def run(envname):
	log.debug("run %s" % envname)
	rc, _ = env.run('deploy', envname, 'deploy', cfgfile = _cfgfile)
	return rc
