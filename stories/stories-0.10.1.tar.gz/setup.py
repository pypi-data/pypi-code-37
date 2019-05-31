# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['stories',
 'stories._exec',
 'stories.contrib',
 'stories.contrib.debug_toolbars',
 'stories.contrib.debug_toolbars.django',
 'stories.contrib.sentry']

package_data = \
{'': ['*'],
 'stories.contrib.debug_toolbars.django': ['templates/stories/debug_toolbar/*']}

entry_points = \
{'pytest11': ['stories = stories.contrib.pytest']}

setup_kwargs = {
    'name': 'stories',
    'version': '0.10.1',
    'description': 'Define a user story in the business transaction DSL',
    'long_description': ".. |travis| image:: https://travis-ci.org/dry-python/stories.svg?branch=master\n    :target: https://travis-ci.org/dry-python/stories\n\n.. |codecov| image:: https://codecov.io/gh/dry-python/stories/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/dry-python/stories\n\n.. |docs| image:: https://readthedocs.org/projects/stories/badge/?version=latest\n    :target: https://stories.readthedocs.io/en/latest/?badge=latest\n\n.. |gitter| image:: https://badges.gitter.im/dry-python/stories.svg\n    :target: https://gitter.im/dry-python/stories\n\n.. |pypi| image:: https://img.shields.io/pypi/v/stories.svg\n    :target: https://pypi.python.org/pypi/stories/\n\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://raw.githubusercontent.com/dry-python/brand/master/logo/stories.png\n\n|travis| |codecov| |docs| |gitter| |pypi| |black|\n\n----\n\nThe business transaction DSL\n============================\n\n- `Source Code`_\n- `Issue Tracker`_\n- `Documentation`_\n- `Discussion`_\n\nInstallation\n------------\n\nAll released versions are hosted on the Python Package Index.  You can\ninstall this package with following command.\n\n.. code:: bash\n\n    pip install stories\n\nUsage\n-----\n\n``stories`` provide a simple way to define a complex business scenario\nthat include many processing steps.\n\n.. code:: python\n\n    from stories import story, arguments, Success, Failure, Result\n\n    class Subscribe:\n\n        @story\n        @arguments('category_id', 'user_id')\n        def buy(I):\n\n            I.find_category\n            I.find_profile\n            I.check_balance\n            I.persist_subscription\n            I.show_subscription\n\n        def find_category(self, ctx):\n\n            category = Category.objects.get(id=ctx.category_id)\n            return Success(category=category)\n\n        def find_profile(self, ctx):\n\n            profile = Profile.objects.get(user_id=ctx.user_id)\n            return Success(profile=profile)\n\n        def check_balance(self, ctx):\n\n            if ctx.category.cost < ctx.profile.balance:\n                return Success()\n            else:\n                return Failure()\n\n        def persist_subscription(self, ctx):\n\n            subscription = Subscription(ctx.category, ctx.profile)\n            subscription.save()\n            return Success(subscription=subscription)\n\n        def show_subscription(self, ctx):\n\n            return Result(ctx.subscription)\n\n.. code:: python\n\n    >>> Subscribe().buy(category_id=1, user_id=1)\n    <Subscription object>\n    >>> _\n\nThis code style allow you clearly separate actual business scenario\nfrom implementation details.\n\nLicense\n-------\n\nStories library is offered under the two clause BSD license.\n\n.. _source code: https://github.com/dry-python/stories\n.. _issue tracker: https://github.com/dry-python/stories/issues\n.. _documentation: https://stories.readthedocs.io/en/latest/\n.. _discussion: https://gitter.im/dry-python/stories\n",
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'url': 'https://dry-python.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
