from __future__ import unicode_literals, absolute_import

import re
import sys
import zipp
import itertools

from .api import Distribution
from importlib_metadata.abc import DistributionFinder


if sys.version_info >= (3,):  # pragma: nocover
    from contextlib import suppress
    from pathlib import Path
else:  # pragma: nocover
    from contextlib2 import suppress  # noqa
    from itertools import imap as map  # type: ignore
    from pathlib2 import Path

    FileNotFoundError = IOError, OSError
    NotADirectoryError = IOError, OSError
    __metaclass__ = type


def install(cls):
    """Class decorator for installation on sys.meta_path."""
    sys.meta_path.append(cls())
    return cls


class NullFinder(DistributionFinder):
    """
    A "Finder" (aka "MetaClassFinder") that never finds any modules,
    but may find distributions.
    """
    @staticmethod
    def find_spec(*args, **kwargs):
        return None

    # In Python 2, the import system requires finders
    # to have a find_module() method, but this usage
    # is deprecated in Python 3 in favor of find_spec().
    # For the purposes of this finder (i.e. being present
    # on sys.meta_path but having no other import
    # system functionality), the two methods are identical.
    find_module = find_spec


class MetadataPathBaseFinder(NullFinder):
    """A degenerate finder for distribution packages on the file system.

    This finder supplies only a find_distributions() method for versions
    of Python that do not have a PathFinder find_distributions().
    """

    def find_distributions(self, name=None, path=None):
        """Return an iterable of all Distribution instances capable of
        loading the metadata for packages matching the name
        (or all names if not supplied) along the paths in the list
        of directories ``path`` (defaults to sys.path).
        """
        if path is None:
            path = sys.path
        pattern = '.*' if name is None else re.escape(name)
        found = self._search_paths(pattern, path)
        return map(PathDistribution, found)

    @classmethod
    def _search_paths(cls, pattern, paths):
        """
        Find metadata directories in paths heuristically.
        """
        return itertools.chain.from_iterable(
            cls._search_path(path, pattern)
            for path in map(Path, paths)
            )

    @classmethod
    def _predicate(cls, pattern, root, item):
        return re.match(pattern, str(item.name), flags=re.IGNORECASE)

    @classmethod
    def _search_path(cls, root, pattern):
        if not root.is_dir():
            return ()
        normalized = pattern.replace('-', '_')
        matcher = cls.search_template.format(pattern=normalized)
        return (item for item in root.iterdir()
                if cls._predicate(matcher, root, item))


@install
class MetadataPathFinder(MetadataPathBaseFinder):
    search_template = r'{pattern}(-.*)?\.(dist|egg)-info'


@install
class MetadataPathEggInfoFileFinder(MetadataPathBaseFinder):
    search_template = r'{pattern}(-.*)?\.egg-info'

    @classmethod
    def _predicate(cls, pattern, root, item):
        return (
            (root / item).is_file() and
            re.match(pattern, str(item.name), flags=re.IGNORECASE))


class PathDistribution(Distribution):
    def __init__(self, path):
        """Construct a distribution from a path to the metadata directory."""
        self._path = path

    def read_text(self, filename):
        with suppress(FileNotFoundError, NotADirectoryError):
            with self._path.joinpath(filename).open(encoding='utf-8') as fp:
                return fp.read()
        return None
    read_text.__doc__ = Distribution.read_text.__doc__

    def locate_file(self, path):
        return self._path.parent / path


@install
class WheelMetadataFinder(NullFinder):
    """A degenerate finder for distribution packages in wheels.

    This finder supplies only a find_distributions() method for versions
    of Python that do not have a PathFinder find_distributions().
    """
    search_template = r'{pattern}(-.*)?\.whl'

    def find_distributions(self, name=None, path=None):
        """Return an iterable of all Distribution instances capable of
        loading the metadata for packages matching the name
        (or all names if not supplied) along the paths in the list
        of directories ``path`` (defaults to sys.path).
        """
        if path is None:
            path = sys.path
        pattern = '.*' if name is None else re.escape(name)
        found = self._search_paths(pattern, path)
        return map(WheelDistribution, found)

    @classmethod
    def _search_paths(cls, pattern, paths):
        return (
            path
            for path in map(Path, paths)
            if re.match(
                cls.search_template.format(pattern=pattern),
                str(path.name),
                flags=re.IGNORECASE,
                )
            )


class WheelDistribution(Distribution):
    def __init__(self, archive):
        self._archive = zipp.Path(archive)
        name, version = archive.name.split('-')[0:2]
        self._dist_info = '{}-{}.dist-info'.format(name, version)

    def read_text(self, filename):
        target = self._archive / self._dist_info / filename
        return target.read_text() if target.exists() else None
    read_text.__doc__ = Distribution.read_text.__doc__

    def locate_file(self, path):
        return self._archive / path
