# -*- encoding: utf-8 -*-



from selenium.webdriver.support import select

from pytoolbox import module

_all = module.All(globals())


class Select(select.Select):
    """A Select with the attributes of the WebElement."""

    def __getattr__(self, name):
        return getattr(self._el, name)


__all__ = _all.diff(globals())
