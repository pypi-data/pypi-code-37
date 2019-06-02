# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sshh']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.6']

entry_points = \
{'console_scripts': ['sshh = sshh.sshh:main',
                     'sshh-add = sshh.sshh_add:main',
                     'sshh-agent = sshh.sshh_agent:main',
                     'sshh-askpass = sshh.sshh_askpass:main',
                     'sshh-config = sshh.sshh_config:main']}

setup_kwargs = {
    'name': 'sshh',
    'version': '0.10.0',
    'description': 'sshh is an ssh helper tool for batch registration of ssh private keys in ssh-agent',
    'long_description': '====\nsshh\n====\n\n``sshh`` is an ssh helper tool for batch registration of ssh private keys in ssh-agent.\n\nThe main purpose of sshh is to avoid ``ssh: Too many authentication failures`` that occurs when\nthe number of keys registered in ssh-agent exceeds a certain number. This error occurs when the\nupper limit of key attempts is exceeded when the server is setting the upper limit of private key\nattempts strictly.\n\nThis problem can be avoided by clearing all the keys registered in ssh-agent and registering\nas many as necessary, or entering the passphrase each time. However, in situations where there\nare multiple keys and servers, ssh connections can be very cumbersome. sshh uses Python\'s\nsubprocess package to start a new ssh-agent, and further calls ssh-add to collectively register\nas many private keys as necessary. This relieves you from the hassle.\n\nUsages\n=======\n\nInit\n-----\n\n::\n\n    (.venv) $ sshh-config init\n    Enter password for your registry: xxxxx\n    The registry file ~/.sshh.registry is created.\n\nChange password\n----------------\n\n::\n\n    (.venv) $ sshh-config chpw\n    Enter CURRENT password for your registry: xxxxx\n    Enter NEW password for your registry: yyyyy\n    Enter NEW password again for verification: yyyyy\n    Password has been changed.\n\nRegister key\n-------------\n\n::\n\n    (.venv) $ sshh-add -g prod ~/id_rsa_server1\n    Enter password for your registry: xxxxx\n    Enter passphrase for the keyfile: yyyyy\n    The keyfile is registered.\n\nList keys\n----------\n\n::\n\n    (.venv) $ sshh-add -l\n    Enter password for your registry: xxxxx\n    [prod]\n    /home/user/.ssh/id_rsa_server1\n    /home/user/.ssh/id_rsa_server2\n\n    [stg]\n    /home/user/.ssh/id_rsa_server7\n    /home/user/.ssh/id_rsa_server8\n\nInvoke ssh-agent\n-----------------\n\n::\n\n    (venv) $ sshh-agent -g prod\n    Enter password for your registry: xxxxx\n    Enter password for your registry:\n    Registering keys for session "prod"\n    ssh-agent PID=67779 session "prod" has been started. To close this session, exit shell.\n    [prod] (venv) $\n    [prod] (venv) $ exit\n    exit\n    ssh-agent PID=67779 session "prod" has been closed.\n    (venv) $\n\n',
    'author': 'Takayuki Shimizukawa',
    'author_email': 'shimizukawa@gmail.com',
    'url': 'https://github.com/shimizukawa/sshh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
