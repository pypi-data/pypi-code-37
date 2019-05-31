# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pybee', 'pybee.action', 'pybee.platform', 'pybee.platform.linux']

package_data = \
{'': ['*']}

install_requires = \
['PyFunctional>=1.2,<2.0',
 'click>=7.0,<8.0',
 'hfilesize>=0.1.0,<0.2.0',
 'jinja2>=2.10,<3.0',
 'psutil>=5.6,<6.0',
 'tqdm>=4.31,<5.0']

setup_kwargs = {
    'name': 'pybee',
    'version': '0.3.2',
    'description': 'Provides some useful functions to write maintainer scripts or deployment scripts',
    'long_description': "# pybee\n\n   pybee 提供一些辅助函数，方便使用 Python 来写系统维护/部署脚本, 使用 Bash 写维护/部署脚本实在不爽；例如提供 sed、awk 工具对应的功能函数，但 pybee 目标不是编写一个 python 版的 sed/awk 工具\n\n\n\n## 编译\n\n### 安装依赖工具\n\n* python 3.4+\n* poetry\n\n执行下面命令安装依赖包\n\n```\npoetry install\n```\n\n### 编译\n\n```\npoetry build\n```\n\n### pybee 模块\n  pybee 模块封装了或者增加常见系统维护需要的函数\n\n* pybee.path 增强 os.path 模块的一些函数\n* pybee.compress 封装 zip/tar.gz 压缩函数\n* pybee.sed 提供 sed 工具类似功能的函数 \n* pybee.ask 封装在 termia 常见交互操作的函数\n* pybee.importutil 提供把一个 py 文件当作模块 import 的函数\n\n还有其他模块，这里就不一一列出\n\n### pybee.action 模块\n  在 pybee 模块的基础上把常见的操作封装成 action，下面就是一个列子\n\n  ```\nimport pybee\n\nac = pybee.action.ActionContext([\n    ('SCRIPT_DIR', pybee.path.get_script_path(__file__)),\n    ('DIST_DIR', '$CURRENT_DIR/dist'),\n    ('OUT_PUT_DIR', '$DIST_DIR/test-demo-portable'),\n])\n\nac.prepare_dir(\n    [\n        '$DIST_DIR', '$OUT_PUT_DIR',\n        '$OUT_PUT_DIR/portable',\n    ]\n)\n\nac.check_bin([\n    ('gradle','please install gradle', 'GRADLE_BIN'),\n])\n\nac.exec_cmd(\n    [\n        '$GRADLE_BIN', 'packDist', '-x', 'test'\n    ]\n)\n\nac.unzip(\n    '$DIST_DIR/test-demo/test-demo.jar',\n    '$OUT_PUT_DIR'\n)\n\n\ndef ignore_config_files(src, names):\n    return ['project.groovy', ]\n\nac.copy(\n    [\n        ('$CURRENT_DIR/config', '$OUT_PUT_DIR', {\n            'ignore': ignore_config_files\n        }),\n        ('$CURRENT_DIR/public', '$OUT_PUT_DIR'),\n    ]\n)\n\nac.copy(\n    [\n        ('run.ps1', '$OUT_PUT_DIR'),\n        ('run.sh', '$OUT_PUT_DIR'),\n        ('portable.groovy', '$OUT_PUT_DIR/config'),\n    ],\n    work_dir='$SCRIPT_DIR/portable'\n)\n\nac.zip(\n    '$OUT_PUT_DIR',\n    '$DIST_DIR/test-demo-portable-{datetime}.zip',\n    env_name='DIST_FILE'\n)\n\n\ndef print_success(context):\n    print('')\n    zip_file = context.get_env('DIST_FILE')\n    print('pack successfully, dist file is %s' % zip_file)\n\n\nac.execute(succ_func=print_success)\n  ```",
    'author': 'riag',
    'author_email': 'riag@163.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
