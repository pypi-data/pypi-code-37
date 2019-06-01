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
    'version': '0.3.20b0',
    'description': 'really simple profiling for mere mortals',
    'long_description': '# hume - simple & quick profiling for mere mortals\n\nhume is a fun-expirement turned Python package. In short, it exposes a decorator `profile` that you can use to measure \nthe execution time of functions. It goes out of its way to make its protocol clear, usage simple, and configuration flexible. \n\nLike many profiling libraries, hume adds overhead which means its measurements are (often) slower than real execution time when testing small pieces of code. **Don\'t** use it for super-scientific benchmarking.\n\n**Note:** Python >= 3.6 required.\n\n## Installation\n\nYou can install `hume` from [PyPI](https://pypi.org/):\n\n    pip install hume\n\nor:\n\n    pipenv install hume\n\n## ★ hume.decorators\n\n### ★★ profile\n\nA simple decorator to measure function execution times. \n\n- Supports N simulations and average times. \n- Supports, recognizes, and reports recursive functions.\n- (optional) List `args` and `kwargs` as provided to the decorated function.\n- (optional) Display the decorated function\'s return value\n- (optional) Supress `print` statements in decorated functions (default is `False`, output is only reported for one simulation)\n\n\n`profile` does not in any way modify what\'s returned by the decorated function. The only thing it will possibly augment are `print` statements.\n\n#### ★★★ usage\n\nSimply decorate any function:\n\n```python\nfrom hume.decorators import profile\n\n@profile(6)\ndef slow_add(num):\n    """\n    slow_add sleeps one second and returns num + 1\n    """\n\n    time.sleep(1)\n    return num + 1\n\nprint(slow_add(3))\n```\n\nAnd let it do its job:\n\n```terminal\nprofiling slow_add \n------------------------------------------------\n→ name: slow_add\n→ simulations: 6\n→ average execution time: 1.0034156345 seconds\n\n4\n```\n\n#### ★★★ options and defaults\n\n`profile` supports the following params:\n\n- `nums: int = 1` → how many simulations to conduct\n- `show_args: bool = False` → display `args` passed to the decorated function\n- `show_kwargs: bool = False` →  display `kwargs` passed to the decorated function\n- `show_result: bool = False` →  display decorated function return value\n- `mute_console: bool = False` →  supress `print` statements inside the decorated function\'s body. Useful when you have a bunch of these that you don\'t want to remove just for the sake of measurement.<sup>1</sup>\n\n<span style="font-size:12px;"><sup>1</sup> Even if `mute_console` is `False`, recursive functions will print normally and not per `nums`.</small>\n\n#### ★★★ recursion\n\nFor recursive functions, `profile` just knows (and doesn\'t pollute the console):\n\n```python\n# recursive function\n@profile(2)\ndef factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\n\nfactorial(3)\n```\n\n```terminal\nprofiling factorial (recursive function detected) \n------------------------------------------------\n→ name: factorial\n→ simulations: 2\n→ average execution time: 0.00011469949999964868 seconds\n```\n\n#### ★★★ changing & overriding defaults\n\nIf you don\'t like `profile`\'s [default configuration](#-options-and-defaults), you can import the `CONFIG` dict and override them. For example, if you want `profile` to include the `return` from the decorated function by default, you would do the following:\n\n```python\nfrom hume.decorators import profile, CONFIG\n\nCONFIG["show_results"] = True\n\n@profile(2)\ndef return_one():\n    return 1\n\n# you can always override your own defaults:\n@profile(show_result=False)\ndef return_two_ignored():\n    return 2\n```\n\n#### ★★★ colorized output\n\nOutput is colorized, because priorities:\n\n![console output demo](https://raw.githubusercontent.com/SHxKM/hume/master/docs/console_demo.png?token=ABSE3IVTPJ6CWFRQUHSW75C47APAU)',
    'author': 'SHxKM',
    'author_email': 'hi@shibel.com',
    'url': 'https://github.com/SHxKM/hume',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
