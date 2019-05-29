# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

import sys
import argcomplete

from ruamel.std.argparse import (
    ProgramBase,
    option,
    sub_parser,
    version,
    CountAction,
    SmartFormatter,
)
from ruamel.appconfig import AppConfig
from ruamel.std.pathlib import Path

from .__init__ import __version__


def to_stdout(*args):
    sys.stdout.write(' '.join(args))


class MusicCmd(ProgramBase):
    def __init__(self):
        super(MusicCmd, self).__init__(
            formatter_class=SmartFormatter,
            # aliases=True,
        )

    # you can put these on __init__, but subclassing MusicCmd
    # will cause that to break
    @option(
        '--verbose',
        '-v',
        help='increase verbosity level',
        action=CountAction,
        const=1,
        nargs=0,
        default=0,
        global_option=True,
    )
    @option(
        '--quiet',
        '-q',
        action=CountAction,
        dest='verbose',
        const=-1,
        nargs=0,
        global_option=True,
    )
    @option('--dryrun', action='store_true')
    @version('version: ' + __version__)
    def _pb_init(self):
        # special name for which attribs are included in help
        pass

    def run(self):
        from .music import Music
        self._music = Music(self._args, self._config)
        if hasattr(self._args, 'func'):  # not there if subparser selected
            return self._args.func()
        if self._args.func:
            return self._args.func()

    def parse_args(self):
        self._config = AppConfig(
            'music',
            filename=AppConfig.check,
            parser=self._parser,  # sets --config option
            warning=to_stdout,
            add_save=True,  # add a --save-defaults (to config) option
        )
        # self._config._file_name can be handed to objects that need
        # to get other information from the configuration directory
        self._config.set_defaults()
        argcomplete.autocomplete(self._parser)
        self._parse_args()

    @sub_parser(help='convert music file')
    @option('--cue', help='split args according to cue file and convert')
    @option(
        '--no-cue-check',
        action='store_true',
        help='do not check if there is a matching cue file',
    )
    @option('--force', action='store_true', help='force conversion even if target exists')
    @option('--re-tag', '--retag', action='store_true', help='copy tags to existing files')
    @option(
        '--max-size',
        type=int,
        default=32,
        help='max file size to convert (default: %(default)sMb)',
    )
    @option('args', nargs='+', help='music files to convert')
    # @option('--session-name', default='abc')
    def convert(self):
        self._music.convert()

    @sub_parser(help='check if primary secondary conversion is necessary')
    @option('--convert', action='store_true', help='convert files checked to be older/missing')
    def check(self):
        self._music.check()

    @sub_parser(help='find some music file in primary or secondary format')
    @option('--artist', action='store_true', help='only show artist level')
    @option('--album', action='store_true', help='only show album level')
    @option('args', nargs='+', help='list of elements of filename to be found')
    def find(self):
        self._music.find()

    @sub_parser(help='sort tmp directory to the primary and secondary format')
    @option('--convert', action='store_true', help='generate secondary format from primary')
    @option('--test', action='store_true')
    @option('--startwith', help='only sort if starting with path')
    def sort(self):
        self._music.sort()

    @sub_parser(help='flatten pictures into music directory (for picard to move along)')
    @option('args', nargs='*', help='list of directories to recursively parse (default: . )')
    def flatten(self):
        self._music.flatten()

    @sub_parser(help='analyse a directory tree, to find music')
    @option('args', nargs='*', help='list of directories to recursively parse (default: . )')
    def analyse(self):
        self.redirect()

    @sub_parser(help='cleanup empty directories, old path formats, etc.')
    @option(
        '--dedup',
        action='store_true',
        help='check and remove old paths in primary and secondary storage',
    )
    @option('--year', action='store_true', help='move albums to original year')
    @option('--gen', action='store_true', help='generate year related metadata file')
    def cleanup(self):
        self._music.cleanup()

    @sub_parser(help='show tag metadata')
    @option('args', nargs='+', type=Path, help='music files to process')
    def meta(self):
        self._music.meta()

    @sub_parser(help='copy image from to')
    @option('--from', type=Path, help='music file to read image from')
    @option('--to', type=Path, help='music file to write to')
    @option('--all', action='store_true')
    @option('--mp3', action='store_true')
    @option('--check', type=Path, nargs='+', help='check dirs for cover art')
    @option('--get', type=Path, nargs='+', help='get file cover art')
    def image(self):
        self._music.image()

    @sub_parser(help='generate html from .music.yaml')
    @option('--force', action='store_true', help='force conversion even if up-to-date')
    # @option('args', nargs='+', help='list of music filenames to find')
    def html(self):
        self._music.convert_yaml_html()

    def _version_information(self):
        version_data = [(_package_data['full_package_name'], __version__)]
        longest = len(version_data[0][0])
        if isinstance(_package_data['install_requires'], list):
            pkgs = _package_data['install_requires']
        else:
            pkgs = _package_data['install_requires'].get('any', [])
        for pkg in pkgs:
            try:
                version_data.append((pkg, sys.modules[pkg].__version__))
                longest = max(longest, len(pkg))
            except KeyError:
                pass
        for pkg, ver in version_data:
            print('{{:{{}}s}} {{}}'.format(pkg + ':', longest+1, ver))
        sys.exit(0)

    def redirect(self, *args, **kw):
        """
        redirect to a method on self.develop, with the same name as the
        method name of calling method
        """
        return getattr(self._music, sys._getframe(1).f_code.co_name)(*args, **kw)


def main():
    n = MusicCmd()
    n.parse_args()
    sys.exit(n.run())


if __name__ == '__main__':
    main()
