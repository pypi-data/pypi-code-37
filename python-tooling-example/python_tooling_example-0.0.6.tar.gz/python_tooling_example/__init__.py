r"""An example package to show usage of

- Automatic documentation building on `Read the Docs <readthedocs.org>`_.
- Automatic building and test running on `Travis <travis-ci.org>`_.
- Automatic pushing to PyPI using `git tag && git push`.


In this package, the ``__init__.py`` file here basically just serves as a home for
the package documentation and for top level imports designed to bring the
public API (potentially scattered throughout sub(modules/packages) to the top
level.

Arbitrary math can be displayed here using LaTeX

.. math::
    C_{vv}^{(\delta)}(t, \Delta n) = \frac{3k_BT}{\delta^2\sqrt{\xi k}}

.. math::
    \times \left\{ | t - \delta|^{1/2} G_{1,2}^{2,0}\left[\left. \frac{| \Delta{}n|^2 \xi}{4k} | t - \delta|^{-1} \right|^{3/2}_{0,1/2}\right] \right.

.. math::
    + | t + \delta|^{1/2} G_{1,2}^{2,0}\left[ \frac{| \Delta{}n|^2 \xi}{4k} | t + \delta|^{-1} | ^{3/2}_{0,1/2}\right]

.. math::
    \left. -2|t|^{1/2} G_{1,2}^{2,0}\left[ \frac{| \Delta{}n|^2 \xi}{4k} | t|^{-1} | ^{3/2}_{0,1/2}\right] \right\}.

as long as it helps describe the package."""

from .example_module import add_2
from .example_subpackage.daughter_module import concat_2

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
