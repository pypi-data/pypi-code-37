from twine.commands import upload as twine_upload
from pip._internal import main as pip_main
from .setup_text import setup_text
from .help_text import help_text
from pathlib import Path
import shutil
import sys


class Command:
    @classmethod
    def execute(cls, cmd='help', *args):
        """Execute command."""
        return getattr(cls(), cmd, Command.help)(*args)

    @staticmethod
    def init(*args):
        """Create a setup.py file."""
        with open('setup.py', 'w', encoding='utf-8') as f:
            f.write(setup_text)
        return 'Successfully!'

    @staticmethod
    def upload(*args):
        """Package the project and upload it to pypi."""
        if len(args) > 1:
            raise ValueError('Please check the command (pysetup upload <is_clear>).')

        is_clear = args and args[0] in ['t', 'T', 'true', 'True', 'TRUE']
        username = input('pypi-username: ')
        password = input('pypi-password: ')

        if is_clear: Command.clear()
        Command.package()
        twine_upload.main(['-u', username, '-p', password, 'dist/*'])
        if is_clear: Command.clear()
        return 'Successfully!'

    @staticmethod
    def upload_test(*args):
        """Package the project and upload it to testpypi."""
        if len(args) > 1:
            raise ValueError('Please check the command (pysetup upload_test <is_clear>).')

        is_clear = args and args[0] in ['t', 'T', 'true', 'True', 'TRUE']
        username = input('testpypi-username: ')
        password = input('testpypi-password: ')

        if is_clear: Command.clear()
        Command.package()
        twine_upload.main(['-u', username, '-p', password, '--repository-url', 'https://test.pypi.org/legacy/', 'dist/*'])
        if is_clear: Command.clear()
        return 'Successfully!'

    @staticmethod
    def help(*args):
        """View command list."""
        return help_text

    @staticmethod
    def package(*args):
        """Package the project."""
        setup_file = Path.cwd() / Path('setup.py')
        if not setup_file.exists():
            raise FileNotFoundError('The setup.py not found.')

        original_argv = sys.argv
        sys.argv = [setup_file, 'sdist', 'bdist_wheel']
        with open(setup_file, 'r') as f:
            exec(f.read())
        sys.argv = original_argv
        return 'Successfully!'

    @staticmethod
    def clear(*args):
        """clear packaged files (build/dist/*.egg-info)."""
        for p in [Path('build'), Path('dist'), *Path.cwd().glob('*.egg-info')]:
            if p.exists(): shutil.rmtree(p)
        return 'Successfully!'

    @staticmethod
    def install_test(*args):
        if len(args) != 1: raise ValueError('Please check the command (pysetup install_test <package_name>).')

        package_name = args[0]
        pip_main(['install', '-i', 'https://test.pypi.org/simple/', package_name, '--upgrade'])
        return 'Successfully!'
