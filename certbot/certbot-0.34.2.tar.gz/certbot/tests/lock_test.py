"""Tests for certbot.lock."""
import functools
import multiprocessing
import unittest
try:
    import fcntl  # pylint: disable=import-error,unused-import
except ImportError:
    POSIX_MODE = False
else:
    POSIX_MODE = True

import mock

from certbot import errors
from certbot.compat import os
from certbot.tests import util as test_util


class LockDirTest(test_util.TempDirTestCase):
    """Tests for certbot.lock.lock_dir."""
    @classmethod
    def _call(cls, *args, **kwargs):
        from certbot.lock import lock_dir
        return lock_dir(*args, **kwargs)

    def test_it(self):
        assert_raises = functools.partial(
            self.assertRaises, errors.LockError, self._call, self.tempdir)
        lock_path = os.path.join(self.tempdir, '.certbot.lock')
        test_util.lock_and_call(assert_raises, lock_path)


class LockFileTest(test_util.TempDirTestCase):
    """Tests for certbot.lock.LockFile."""
    @classmethod
    def _call(cls, *args, **kwargs):
        from certbot.lock import LockFile
        return LockFile(*args, **kwargs)

    def setUp(self):
        super(LockFileTest, self).setUp()
        self.lock_path = os.path.join(self.tempdir, 'test.lock')

    def test_acquire_without_deletion(self):
        # acquire the lock in another process but don't delete the file
        child = multiprocessing.Process(target=self._call,
                                        args=(self.lock_path,))
        child.start()
        child.join()
        self.assertEqual(child.exitcode, 0)
        self.assertTrue(os.path.exists(self.lock_path))

        # Test we're still able to properly acquire and release the lock
        self.test_removed()

    def test_contention(self):
        assert_raises = functools.partial(
            self.assertRaises, errors.LockError, self._call, self.lock_path)
        test_util.lock_and_call(assert_raises, self.lock_path)

    def test_locked_repr(self):
        lock_file = self._call(self.lock_path)
        try:
            locked_repr = repr(lock_file)
            self._test_repr_common(lock_file, locked_repr)
            self.assertTrue('acquired' in locked_repr)
        finally:
            lock_file.release()

    def test_released_repr(self):
        lock_file = self._call(self.lock_path)
        lock_file.release()
        released_repr = repr(lock_file)
        self._test_repr_common(lock_file, released_repr)
        self.assertTrue('released' in released_repr)

    def _test_repr_common(self, lock_file, lock_repr):
        self.assertTrue(lock_file.__class__.__name__ in lock_repr)
        self.assertTrue(self.lock_path in lock_repr)

    @test_util.skip_on_windows(
        'Race conditions on lock are specific to the non-blocking file access approach on Linux.')
    def test_race(self):
        should_delete = [True, False]
        stat = os.stat

        def delete_and_stat(path):
            """Wrap os.stat and maybe delete the file first."""
            if path == self.lock_path and should_delete.pop(0):
                os.remove(path)
            return stat(path)

        with mock.patch('certbot.lock.os.stat') as mock_stat:
            mock_stat.side_effect = delete_and_stat
            self._call(self.lock_path)
        self.assertFalse(should_delete)

    def test_removed(self):
        lock_file = self._call(self.lock_path)
        lock_file.release()
        self.assertFalse(os.path.exists(self.lock_path))

    def test_unexpected_lockf_or_locking_err(self):
        if POSIX_MODE:
            mocked_function = 'certbot.lock.fcntl.lockf'
        else:
            mocked_function = 'certbot.lock.msvcrt.locking'
        msg = 'hi there'
        with mock.patch(mocked_function) as mock_lock:
            mock_lock.side_effect = IOError(msg)
            try:
                self._call(self.lock_path)
            except IOError as err:
                self.assertTrue(msg in str(err))
            else:  # pragma: no cover
                self.fail('IOError not raised')

    def test_unexpected_os_err(self):
        if POSIX_MODE:
            mock_function = 'certbot.lock.os.stat'
        else:
            mock_function = 'certbot.lock.msvcrt.locking'
        # The only expected errno are ENOENT and EACCES in lock module.
        msg = 'hi there'
        with mock.patch(mock_function) as mock_os:
            mock_os.side_effect = OSError(msg)
            try:
                self._call(self.lock_path)
            except OSError as err:
                self.assertTrue(msg in str(err))
            else:  # pragma: no cover
                self.fail('OSError not raised')


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
