# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hume', 'hume.decorators']

package_data = \
{'': ['*']}

install_requires = \
['sty>=1.0-beta.1,<2.0']

setup_kwargs = {
    'name': 'hume',
    'version': '0.3.0b0',
    'description': 'really simple profiling for mere mortals',
    'long_description': '# hume - simple & quick profiling for mortals\n\n\n## Installation\n\nYou can install \'hume` from [PyPI](https://pypi.org/):\n\n    pip install hume\n\n**Note:** Python >= 3.6 required.\n\n## ★ hume.decorators\n\n### ★★ profile\n\nA simple decorator to measure function execution times. \n\n- Supports N simulations and average times. \n- Supports, recognizes, and reports recursive functions.\n- (optional) List `args` and `kwargs` as provided to the decorated function.\n- (optional) Display the decorated function\'s return value\n- (optional) Supress `print` statements in decorated functions (default is `False`, output is only reported for one simulation)\n\n#### ★★★ how to use\n\nSimply decorate any function:\n\n```python\nfrom hume.decorators import profile\n\n@profile(nums=3)\ndef slow_add(num):\n    """slow_add does somethig\n    """\n    time.sleep(1)\n    return num\n\nprint(slow_add(3))\n```\n\nAnd let it do its job:\n\n```terminal\nprofiling slow_add \n------------\n→ name: slow_add\n→ simulations: 3\n→ average execution time: 1.0033866766666666 seconds\n\n3\n```\n\n`profile` supports the following params:\n\n- `nums: int = 1` → how many simulations to conduct\n- `show_args: bool = False` → display `args` passed to the decorated function\n- `show_kwargs: bool = False` →  display `kwargs` passed to the decorated function\n- `show_result: bool = False` →  display decorated function return value\n- `mute_console: bool = False` →  supress `print` statements from the decorated function\n\n#### ★★★ recursion\n\nFor recursive functions, `profile` just knows (and doesn\'t pollute the console):\n\n```python\n# recursive function\n@profile(7)\ndef factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\n\nprint(factorial(3))\n```\n\n```terminal\nprofiling factorial (recursive function detected) \n------------\n→ name: factorial\n→ simulations: 7\n→ average execution time: 3.6912857141706875e-06 seconds\n\n6\n```\n\n#### ★★★ colorized output\n\nOutput is colorized:\n\n![console output demo](/docs/console_demo.png)',
    'author': 'Shibel K. Mansour',
    'author_email': 'hi@shibel.com',
    'url': 'https://github.com/SHxKM/hume',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
