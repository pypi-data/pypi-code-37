# coding: utf-8

# from __future__ import print_function, absolute_import, division, unicode_literals
from __future__ import print_function, absolute_import, division

import sys
import os
import time
import tempfile
import subprocess
import glob
import shutil
import datetime
from textwrap import dedent

try:
    from gi.repository import Notify
except ImportError:
    Notify = None

import mutagen
import mutagen.flac
import mutagen.oggvorbis
import mutagen.apev2
import mutagen.mp3

# from mutagen.id3 import TIT2, APIC
from mutagen.easyid3 import EasyID3


from ruamel.std.pathlib import Path, PathLibConversionHelper

from ruamel.doc.html.simple import SimpleHtml

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap

from ruamel.music.stemanalyser import StemAnalyser
from ruamel.music.albumtype import AlbumType
from ruamel.yaml.compat import ordereddict

# valkeys = EasyID3.valid_keys.keys()
# print(valkeys)
# sys.exit(1)

pl = PathLibConversionHelper()

CalledProcessError = subprocess.CalledProcessError

MB_FRONT = 'mb_front.jpg'

img_suffixes = ['.jpeg', '.jpg', '.gif', '.png']
other_suffixes = img_suffixes + ['.cue', '.pdf', '.m3u']


def check_output(cmd, *args, **kw):
    lkw = kw.copy()
    verbose = lkw.pop('verbose', 0)
    cmd2 = [str(x) for x in cmd]
    if verbose > 0:
        print('cmd', ' '.join(cmd2))
    try:
        return subprocess.check_output(cmd2, *args, **lkw)
    except Exception as e:
        print(e)
        print('message', e)
        print('output', e.output)
        print(dir(e))
        sys.exit(1)


stem_analyser = StemAnalyser()


# class Path(PLPath):
#     def analyse(self):
#         return stem_analyser(self.stem)
def _analyse(self):
    return stem_analyser(self.stem)


Path.analyse = _analyse


def _replace(self, s, t, count=-1):
    return Path(str(self).replace(str(s), str(t), count))


Path.replace = _replace


class BaseMusicFormat(object):
    valid_tag_keys = EasyID3.valid_keys.keys()

    def __init__(self, path=None, verbose=0):
        self._path = Path(path) if isinstance(path, basestring) else path
        self._verbose = verbose
        self._tags = None

    def dump_tags(self):
        if self._verbose < 0:
            return
        print('tags:')
        for k in sorted(self._tags):
            v = self._tags[k]
            if len(v) > 32:
                continue
            print(u'  {:15}: {}'.format(k, v))

    @property
    def tags(self):
        if self._tags is None:
            self.scan_tags()
        return self._tags

    @property
    def has_cover_art(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, self.first_cover_art)  # self.check_cover_art())
        return getattr(self, attr)

    @property
    def first_cover_art(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            a = self.get_cover_art()
            setattr(self, attr, a[0] if a else None)
        return getattr(self, attr)

    def len_one_list_to_element(self):
        """formats like FLAC always store tags as lists, convert single element lists
        to that (string) element
        """
        x1 = {}
        for k in self._tags:
            v = self._tags[k]
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
            x1[k] = v
        self._tags = x1

    def set_tmp_name(self):
        'generate and set temporary filename'
        self._path = self._gen_tmp_name()
        return self._path

    def _gen_tmp_name(self, suffix=None):
        'generate a temporary filename'
        if suffix is None:
            suffix = self._suffixes[0]
        x = tempfile.mkstemp(suffix=suffix)
        file_name = x[1]
        os.close(x[0])
        path = Path(file_name)
        path.remove()
        return path

    def exists(self):
        return self._path.exists()

    def try_cmd(self, cmd):
        try:
            res = check_output(cmd, stderr=subprocess.STDOUT)
        except OSError as e:
            if 'Errno 2' in str(e):
                print(
                    dedent(
                        """\
                program "{prg}" not found. Try to install it with:
                sudo apt-get install {prg}""".format(
                            prg=cmd[0]
                        )
                    )
                )
                sys.exit(1)
        return res

    @property
    def original_year(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            year = self.tags.get('originalyear')
            if year is None:
                year = self.tags.get('originaldate')
                if year is not None:
                    year = year.split('-', 1)[0]
            # if year is None:
            #     self.dump_tags()
            setattr(self, attr, year)
        return getattr(self, attr)

    @property
    def year(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            year = self.tags.get('date')
            if year is not None:
                year = year.split('-', 1)[0]
            setattr(self, attr, year)
        return getattr(self, attr)

    def dump_tags(self):
        for k in self.tags:
            try:
                print('{} -> {}'.format(k, self.tags[k]))
            except UnicodeEncodeError:
                print('{} -> {!r}'.format(k, self.tags[k]))


class UncompressedMusicFormat(BaseMusicFormat):
    pass


class CompressedMusicFormat(BaseMusicFormat):
    pass


class LossyCompressedMusicFormat(CompressedMusicFormat):
    pass


class WAV(UncompressedMusicFormat):
    _suffixes = ['.wav']

    def __init__(self, path=None, temp_name=False):
        super(WAV, self).__init__(path)
        if temp_name:
            self.set_tmp_name()
        # print(self._path)


class FLAC(CompressedMusicFormat):
    _suffixes = ['.flac']

    def __init__(self, path=None):
        super(FLAC, self).__init__(path)

    def scan_tags(self, path=None):
        if path is None:
            path = self._path
        assert path.suffix == '.flac'
        self._tags = mutagen.flac.FLAC(str(self._path))
        # for p in  self._tags.pictures:
        #     print(p.mime)
        #     print(p.desc)
        #     print(len(p.data))
        #     print(dir(p))
        audio = mutagen.File(str(self._path))

        # for k in sorted(audio.keys()):
        #     print('k', k, u'covr' in k or u'APIC' in k)
        self.len_one_list_to_element()

        # x = self._flac.get('musicbrainz_trackid')

    def get_cover_art(self, path=None):
        if path is None:
            path = self._path
        audio = mutagen.File(str(self._path))
        try:
            pictures = audio.pictures
            if pictures:
                return pictures
        except:
            print('no pictures')
        for k in self.tags:
            if 'covr' in audio or 'APIC:' in audio:
                print('cover found', k, self.tags[k])
                raise NotImplementedError
        return []

    def from_wav(self, wav):
        cmd = ['flac', '--silent', '--best', '--force', '--output-name', self._path, wav._path]
        check_output(cmd, stderr=subprocess.STDOUT)

    def to_wav(self, wav):
        cmd = ['flac', '--decode', '--output-name', wav._path, self._path]
        check_output(cmd, stderr=subprocess.STDOUT)

    def set_tags(self, tags):
        audio = mutagen.flac.FLAC(str(self._path))
        for k, v in tags.iteritems():
            if k.startswith('Cover Art'):
                print('skipping tag', k, len(v))
                continue
            if isinstance(v, basestring):
                v = v.strip()
                if not v:
                    continue
            else:
                v = str(v)
            # if k.lower() not in self.valid_tag_keys:
            #     continue
            audio[k] = v
        audio.save()


class APE(CompressedMusicFormat):
    _suffixes = ['.ape']
    has_mac = True

    def __init__(self, **kw):
        super(APE, self).__init__(**kw)

    def scan_tags(self, path=None):
        if path is None:
            path = self._path
        assert path.suffix == '.ape'
        try:
            self._tags = mutagen.apev2.APEv2(str(self._path))
        except mutagen.apev2.APENoHeaderError:
            pass
        # x = self._flac.get('musicbrainz_trackid')

    def to_wav(self, wav):
        """this worked on Ubuntu 12.04. Mint 17 no longer works
        but has avconv standard. First do conversion, then use
        the WAV file to split, or install monkeys-audio from
        github download

        uses packages from ppa:g-christ/ppa

        /etc/apt/sources.list.d/g-christ-ppa-precise.list:
        deb http://ppa.launchpad.net/g-christ/ppa/ubuntu precise main
        deb-src http://ppa.launchpad.net/g-christ/ppa/ubuntu precise main

        sudo add-apt-repository -y ppa:g-christ/ppa
        sudo apt-get update
        sudo apt-get install mac
        """
        if APE.has_mac:
            cmd = ['mac', self._path, wav._path, '-d']
        else:
            cmd = ['avconv', '-i', self._path, wav._path]
        check_output(cmd, stderr=subprocess.STDOUT, verbose=self._verbose)


class OGG(LossyCompressedMusicFormat):
    # needs oggdec from vorbis-tools
    _suffixes = ['.ogg']

    def __init__(self, path=None, compression=192):
        super(OGG, self).__init__(path)

    def scan_tags(self, path=None):
        if path is None:
            path = self._path
        assert path.suffix == '.ogg'
        alt_tags = mutagen.oggvorbis.OggVorbis(str(self._path))
        self._tags = {}
        for k, v in alt_tags.iteritems():
            if isinstance(v, list) and len(v) == 1:
                v = v[0]
            self._tags[k] = v

    def to_wav(self, wav):
        cmd = ['oggdec', self._path, '-o', wav._path]
        check_output(cmd, stderr=subprocess.STDOUT)


class MP3(LossyCompressedMusicFormat):
    _suffixes = ['.mp3']

    def __init__(self, path=None, compression=192):
        super(MP3, self).__init__(path)
        self._compression = compression
        self._quality = 2

    def scan_tags(self, path=None):
        if path is None:
            path = self._path
        assert path.suffix == '.mp3'
        try:
            self._tags = mutagen.mp3.MP3(str(self._path))
        except mutagen.mp3.MP3NoHeaderError:
            pass

    def get_cover_art(self, path=None):
        if path is None:
            path = self._path
        audio = mutagen.File(str(self._path))
        try:
            pictures = audio.pictures
            if pictures:
                return pictures
        except:
            pass
        if 'covr' in audio:
            print('covr found', k, self.tags[k])
            raise NotImplementedError
        if 'APIC:' in audio:
            # print('APIC found', dir(audio['APIC:']))
            return [audio['APIC:']]
        return []

    def XXXcheck_cover_art(self, path=None):
        if path is None:
            path = self._path
        audio = mutagen.File(str(self._path))
        try:
            pictures = audio.pictures
            if pictures:
                return True
        except:
            pass
        for k in self.tags:
            if 'covr' in audio or 'APIC:' in audio:
                print('cover found', k, self.tags[k])
                raise NotImplementedError

    def from_wav(self, wav):
        cmd = [
            'lame',
            '--vbr-new',
            '-V',
            self.quality,
            '-b',
            self._compression,
            '-h',
            '--nohist',
            '--silent',
            wav._path,
            self._path,
        ]
        try:
            self.try_cmd(cmd)
        except KeyboardInterrupt:
            if wav._path.exists():
                wav._path.unlink()
            if self._path.exists():
                self._path.unlink()
            sys.exit(-1)

    def set_tags(self, tags):
        audio = mutagen.mp3.MP3(str(self._path), ID3=EasyID3)
        audio['title'] = 'Dummy'
        audio.save()
        audio = EasyID3(str(self._path))

        for k, v in tags.iteritems():
            if isinstance(v, basestring):
                if not v.strip():
                    continue
            else:
                v = str(v)
            if k.lower() not in self.valid_tag_keys:
                continue
            audio[k] = v
        audio.save()

    def add_picture(self, picture):
        from mutagen.id3 import APIC, ID3

        # audio = mutagen.File(str(self._path))
        audio = mutagen.mp3.MP3(str(self._path), ID3=ID3)
        audio.tags.add(
            APIC(
                encoding=3,
                mime=picture.mime,
                type=picture.type,
                desc=picture.desc,
                data=picture.data,
            )
        )
        audio.save()

    def add_image(self, image_file):
        from mutagen.id3 import APIC, ID3

        # audio = mutagen.File(str(self._path))
        mime = 'image/' + image_file.suffix[1:]
        audio = mutagen.mp3.MP3(str(self._path), ID3=ID3)
        audio.tags.add(
            APIC(
                encoding=3,  # 3 -> utf-8
                mime=mime,
                type=3,  # 3 -> cover image
                desc='Cover',
                data=image_file.read_bytes(),
            )
        )
        audio.save()

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, val):
        self._quality = int(val)


class MP4(LossyCompressedMusicFormat):
    _suffixes = ['.mp4', '.m4a', '.m4b']

    def __init__(self, path=None):
        super(MP4, self).__init__(path)

    def to_wav(self, wav):
        """uses ffmpeg"""
        # faad commandline not available for Solus
        # cmd = ['faad', '-o', wav._path, self._path]
        cmd = [
            'ffmpeg',
            '-i',
            self._path,
            '-vn',
            '-acodec',
            'pcm_s16le',
            '-ar',
            '44100',
            '-ac',
            '2',  # default?
            wav._path,
        ]
        self.try_cmd(cmd)

    def scan_tags(self, path=None):
        if path is None:
            path = self._path
        self._tags = path.analyse()


class BreakPoint(object):
    def __init__(self, val):
        self._val = [0, 0]
        if isinstance(val, basestring):
            sval = val.replace('.', ':').split(':')
            self._val = list(reversed([int(x) for x in reversed(sval)]))
        else:
            self._val = val
        if len(self._val) < 2:
            raise NotImplementedError

    def __str__(self):
        ret_val = u'{:d}'.format(self._val[0])
        for v in self._val[1:-1]:
            ret_val += u':{:02d}'.format(v)
        return ret_val + u'.{:02d}'.format(self._val[-1])


class Cue(BaseMusicFormat):
    """not a real music format, but reuses some methods"""

    def __init__(self, path=None):
        super(Cue, self).__init__(path)
        # self._path = Path(path) if isinstance(path, basestring) else path
        self._tracks = {}
        self._performer = None
        self._title = None
        self._year = None
        self._data_file = None
        current_track = None
        for line in self._path.open(encoding='latin-1'):
            if line.startswith('PERFORMER'):
                self._performer = self.from_quotes(line)
                continue
            if line.startswith('TITLE'):
                self._title = self.from_quotes(line)
                continue
            if line.startswith('FILE'):
                self._data_file = self.from_quotes(line)
                continue
            if line.startswith('REM DATE'):
                try:
                    self._year = int(line.split()[2])
                except:
                    pass
                continue
            sline = line.strip()
            if sline.startswith('TRACK '):
                track_num = int(sline.split()[1])
                current_track = self._tracks.setdefault(
                    track_num, dict(artist=self._performer, track=track_num, album=self._title)
                )
                if self._year:
                    current_track['date'] = self._year
                continue
            if current_track is None:
                continue
            if sline.startswith('PERFORMER'):
                current_track['artist'] = self.from_quotes(sline)
                continue
            if sline.startswith('TITLE'):
                # title = self.from_quotes(sline)
                # print(repr(title), title)
                current_track['title'] = self.from_quotes(sline)
                continue
            if sline.startswith('INDEX 01'):
                current_track['breakpoint'] = BreakPoint(sline.split()[2])
                continue
        # print("CUE", self._performer, self._title, self._tracks)

    def split(self, path=None):
        self._tmp_dir = self._gen_tmp_name(suffix='')
        self._tmp_dir.mkdir()
        break_points = self._tmp_dir / 'tmp.cuebrk'
        # break_points = Path('/tmp/cue.cuebrk')
        with break_points.open('w') as fp:
            for k in sorted(self._tracks)[1:]:
                print(u'{}'.format(self._tracks[k]['breakpoint']), file=fp)
        if path and path.exists():
            path = str(path)
        else:
            path = str(self._data_file)
        cmd = [
            'shntool',
            'split',
            '-f',
            str(break_points),
            '-d',
            str(self._tmp_dir),
            '-a',
            "",
            '-n',
            '%02d',
            '-o',
            'wav',
            path,
        ]
        self.try_cmd(cmd)
        # print('tmpdir', self._tmp_dir)

    def gen_flac(self, path=None, tmpdir=None):
        tmpdir = tmpdir if tmpdir else self._tmp_dir
        fsuf = FLAC._suffixes[0]
        print('path', path)
        for k in sorted(self._tracks):
            wav = WAV(tmpdir / '{:02}{}'.format(k, WAV._suffixes[0]))
            t = self._tracks[k]['title'].encode('utf-8')
            name = '{:02} - {}{}'.format(k, t, fsuf).replace('/', '-')
            out_file = FLAC(path / name)
            exists = ' exists' if out_file._path.exists() else ''
            print('flac {}{}'.format(out_file._path.name, exists))
            if exists:
                continue
            out_file.from_wav(wav)
            out_file.set_tags(self._tracks[k])
        for fn in tmpdir.glob('*'):
            fn.unlink()
        tmpdir.rmdir()

    def from_quotes(self, line):
        return line.split('"')[1]


# music_formats = [MP3, FLAC, WAV, APE, OGG]


class Convert(object):
    def __init__(self):
        self._notifier = None
        self._title = 'Music Convert'

    def notify(self, msg):
        if Notify:
            if self._notifier is None:
                self._notifier = Notify.init(self._title)
            nt = Notify.Notification.new(self._title, msg, 'dialog-information')
            nt.show()

    def __call__(self, music):
        assert isinstance(music, Music)
        verbose = music._args.verbose
        # print('verbose', verbose)
        # try:
        #     target = self._args.target
        # except AttributeError:
        #     target_format = music._primary_format
        file_names = []
        for pat in music._args.args:
            file_names.extend(glob.glob(pl.path.expanduser(pat)))
        # gather per directory, so you can do smarter things for printing and
        # for copying images, m3u etc
        directories = ordereddict()  # input dir -> [paths]
        for file_name in file_names:
            path = Path(file_name).resolve(strict=True)
            if path.is_dir():
                raise NotImplementedError
            directories.setdefault(path.parent, []).append(path)
        for idx, directory in enumerate(directories):
            file_names = directories[directory]
            if len(file_names) > 1:
                print('{}directory {}:'.format('\n' if idx > 0 else '', directory))
            self.files_in_one_dir(
                music, file_names, force=music._args.force, shorten=len(file_names) > 1
            )

    def files_in_one_dir(self, music, file_names, force=False, shorten=False):
        """you can assume these files are all in one directory,
        shorten = True will cause directory to be suppressed
        """
        if not file_names:
            return
        verbose = music._args.verbose
        home_dir = pl.path.expanduser('~')
        out_dir = None
        post_copy = []  # files to process if you know out_dir
        for path in file_names:
            if path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                post_copy.append(path)
                continue
            name = path.name if shorten else str(path)
            rm_tmp_file = None
            if verbose > 0:
                print('converting', name)
            cue_file = Path(file_name) if getattr(music._args, 'cue', False) else None
            if not cue_file and not getattr(music._args, 'no_cue_check', False):
                test_cue_file = path.with_suffix('.cue')
                if test_cue_file.exists():
                    print('matching .cue file exists')
                    cue_file = test_cue_file
            if cue_file and path.suffix == '.ape' and not APE.has_mac:
                print('converting to wav, ', end='')
                sys.stdout.flush()
                in_file = APE(path=path, verbose=verbose)
                in_file.scan_tags()
                wav = WAV(temp_name=True)
                in_file.to_wav(wav)
                rm_tmp_file = wav._path

            if cue_file:
                cue = Cue(cue_file)
                cue.split(path=rm_tmp_file if rm_tmp_file else path)
                cue.gen_flac(path=path.parent)
            elif path.suffix in MP4._suffixes:
                ts = pl.path.getsize(path) // (1024 ** 2)
                if music._args.max_size < ts:
                    if verbose > -1:
                        print('too big, skipping [{} < {}]'.format(music._args.max_size, ts))
                    continue
                in_file = MP4(path)
                out_file = MP3(path.with_suffix(MP3._suffixes[0]))
                if out_file.exists():
                    continue
                in_file.scan_tags()
                wav = WAV(temp_name=True)
                in_file.to_wav(wav)
                out_file.from_wav(wav)
                out_file.set_tags(in_file._tags)
                wav._path.remove()
                # print(out_file._path)
                if verbose > 0:
                    self.notify('Converted to ' + str(out_file._path).replace(home_dir, '~'))
            elif path.suffix == '.ogg':
                in_file = OGG(path)
                in_file.scan_tags()
                in_file.dump_tags()
                wav = WAV(temp_name=True)
                in_file.to_wav(wav)
                out_file = MP3(path.with_suffix(MP3._suffixes[0]))
                out_file.from_wav(wav)
                out_file.set_tags(in_file._tags)
                wav._path.remove()
            elif path.suffix == '.ape':
                in_file = APE(path=path, verbose=verbose)
                in_file.scan_tags()
                in_file.dump_tags()
                wav = WAV(temp_name=True)
                in_file.to_wav(wav)
                out_file = FLAC(path.with_suffix(FLAC._suffixes[0]))
                out_file.from_wav(wav)
                out_file.set_tags(in_file._tags)
                wav._path.remove()
            elif path.suffix == '.flac':
                in_file = FLAC(path)
                in_file.scan_tags()
                mp3_path = path.with_suffix(MP3._suffixes[0])
                # should explicitly test for FLAC and MP3
                try:
                    rel_path = path.relative_to(music._primary_format.path)
                    mp3_path = music._secondary_format.path / rel_path.with_suffix(
                        MP3._suffixes[0]
                    )
                    out_dir = mp3_path.parent
                    mp3_path.parent.mkdir(parents=True, exist_ok=True)
                except ValueError:
                    pass  # relative_to failed -> FLAC file not under /data0/Music/FLAC
                # lame does not support flac input
                if force or not mp3_path.exists():
                    wav = WAV(temp_name=True)
                    in_file.to_wav(wav)
                    out_file = MP3(mp3_path)
                    out_file.from_wav(wav)
                    out_file.set_tags(in_file._tags)
                    music.copy_cover_art(in_file, out_file._path)
                    wav._path.remove()
                    if verbose > 0:
                        self.notify(
                            'Converted to ' + str(out_file._path).replace(home_dir, '~')
                        )
                else:
                    if verbose > 0:
                        print('skipping existing file (can use --force to override)')
                    if music._args.re_tag:
                        out_file = MP3(mp3_path)
                        print('copying tags to', out_file._path.name)
                        out_file.set_tags(in_file._tags)
                        music.copy_cover_art(in_file, out_file._path)
            elif path.suffix.lower() in ['.m3u']:
                pass
            else:
                print('Unknown file type:', path.suffix)
            if rm_tmp_file:
                rm_tmp_file.remove()
        if out_dir is not None:
            for path in post_copy:
                dst_file = out_dir / path.name
                if dst_file.exists() and not force:
                    continue
                if verbose > 0:
                    print('copying "{}" to "{}"'.format(path.name, out_dir))
                path.copy(dst_file)


class FormatPreference(object):
    def __init__(self, typ, *args, **kw):
        self._letter_names = {}
        self.typ_name = typ

        class Dummy:
            def __init__(self):
                pass

        # orint('format pref', typ)
        this_module = sys.modules[__name__]
        # for i in globals():
        #     t = getattr(this_module, i)
        #     print(t)
        self.tcls = getattr(this_module, typ, Dummy)
        if not isinstance(self.tcls(), BaseMusicFormat):
            print('type {} not supported', typ)
            sys.exit()
        self.str_path = kw.pop('path')
        self.path = Path(self.str_path)

    def __call__(self, *args, **kw):
        return self.tcls(*args, **kw)

    @staticmethod
    def tup_name(s, drop_int=False):
        if not isinstance(s, unicode):
            s = s.decode('utf-8')
        s = s.lower()
        n = []
        bn = pl.path.basename(s)
        for ch in ',_-':
            bn = bn.replace(ch, ' ')
        for x in bn.split():
            if x in (u'&', u'feat.', u'with', 'and'):
                continue
            if drop_int:
                try:
                    int(x)
                except ValueError:
                    pass
                else:
                    continue
            n.append(x)
        return tuple(sorted(n))

    def get_releases(self, name):
        names = {}
        glob_path = pl.path.join(self.str_path, name, '*')
        base_len = len(self.str_path) + len(name) + 1
        for full_name in glob.glob(glob_path):
            name = pl.path.basename(full_name)
            # sname = name.split()
            name = self.tup_name(name, drop_int=True)
            names[name] = [full_name[base_len + 1 :]]
            # print(name)
        return names

    def get_names(self, base, letter):
        names = {}
        glob_path = pl.path.join(base, letter, '*')
        base_len = len(base)
        for full_name in glob.glob(glob_path):
            name = self.tup_name(full_name)
            # print(name)
            names[name] = [full_name[base_len + 1 :], None]
        return names

        # for root, directory_names, file_names in os.walk(base):
        #     if '/' in root[base_len+1:]:
        # #        continue
        # #    name = sorted(root[base_len+1:]).replace(',', '').split())
        #     print name, pl.path.join(root,

    def get_all_names(self):
        for x in self.path.glob('**/*'):
            yield x
        

    def match_releases(self, name, rel):
        if name[1] is None:
            name[1] = self.get_releases(name[0])
        trel = self.tup_name(rel, drop_int=True)
        print('relname', name, trel)
        return name[1].get(trel)

    def match_names(self, letter, name):
        names = self._letter_names.setdefault(letter, self.get_names(self.str_path, letter))
        tname = self.tup_name(name)
        #print('names', letter, name, names)
        #print('tname', tname)
        return names.get(tname)

    def find_org(self, name):
        # this was called by Music.find_org
        import string

        if '.' in name[-4:]:
            return
        if '-' not in name:
            return
        x, y = map(string.strip, name.split('-', 1))
        # if ' ' not in x:
        #     return
        # if not 'Dire Straits' in name:
        #     return
        for l in [w[0] for w in x.split()]:
            print('l', l)
            m = self.match_names(l, x)
            if m:
                # print(x, y)
                r = self.match_releases(m, y)
                # print('r', r)
                if r:
                    return pl.path.join(m[0], r[0])

    def exists(self, sub_path):
        full_path = pl.path.join(self.str_path, sub_path)
        return pl.path.exists(full_path)

    def has_extension(self, file_name):
        if isinstance(file_name, Path):
            return file_name.suffix.lower() in self.tcls._suffixes
        base, ext = pl.path.splitext(file_name)
        return ext in self.tcls._suffixes

    def target(self, other, path):
        return path.replace(self.path, other.path, 1).with_suffix(other.tcls._suffixes[0])


class OldMusic(object):
    def __init__(self):
        stem_analyser.log_path = Path(self._config.get_file_name()).parent.joinpath(
            'stem_analyser.log'
        )


class Music:
    def __init__(self, args, config):
        self._args = args
        self._config = config
        # self._primary_format = FormatPreference('FLAC',
        #                                         path='/data0/Music/FLAC')
        # self._secondary_format = FormatPreference('MP3', compression=192,
        #                                           path='/data0/Music/MP3')
        cfg = config['primary']
        typ = cfg.pop('typ')
        self._primary_format = FormatPreference(typ, **cfg)
        cfg = config['secondary']
        typ = cfg.pop('typ')
        self._secondary_format = FormatPreference(typ, **cfg)
        self._mapping = None  # yaml loaded

    def convert(self):
        self.converter(self)

    def check(self):
        pri = self._primary_format
        sec = self._secondary_format

        # for root, directory_names, file_names in pri.path.walk():
        for root, directory_names, file_names in pl.walk(pri.path):
            directory_names.sort()
            for fn in sorted(file_names):
                if not pri.has_extension(fn):
                    continue
                pfn = root / fn
                target = pri.target(sec, pfn)
                if not target.exists():
                    print('no file', target)
                    if self._args.convert:
                        self.converter.files_in_one_dir(self, [pfn], force=True)
                    else:
                        continue
                if target.stat().st_mtime < pfn.stat().st_mtime:
                    print('older', target)
                    if self._args.convert:
                        self.converter.files_in_one_dir(self, [pfn], force=True)
            sys.stdout.flush()
        print('done')

    @staticmethod
    def all_lower_args(args):
        for arg in args:
            for ch in arg:
                if ch.isupper():
                    return False
        return True

    @staticmethod
    def all_match(fn, args):
        for arg in args:
            if arg not in fn:
                return False
        return True

    def find(self):
        # assume secondary format contains superset of the primary format
        count = 0
        last_displayed = None
        all_lower = self.all_lower_args(self._args.args)
        base_len = len(str(self._secondary_format.path)) + 3  # 3 = len('/' + initial char + '/')
        for full_name in self._secondary_format.get_all_names():
            count += 1
            fn = str(full_name).lower() if all_lower else str(full_name)
            if not self.all_match(fn, self._args.args):
                continue
            fn = fn[base_len:]
            if fn.count('/') < 2:
                continue
            if self._args.artist:
                fn, _, _ = fn.rsplit('/', 2)
            elif self._args.album:
                fn, _ = fn.rsplit('/', 1)
            if fn == last_displayed:
                continue
            print(fn)
            last_displayed = fn
        print(count)

    def find_org(self):
        # this is the original find, and I have no idea anymore what it actually tried
        # to achieve. It might be that it assumes you have a renamed folder (using
        # Picard), to match
        if self._args.args == ['*']:
            args = sorted(glob.glob('*'))
        else:
            args = self._args.args
        for arg in args:
            res = self._secondary_format.find(arg)
            print('arg', arg, res)
            if not res:
                continue
            resf = self._primary_format.exists(res)
            if resf:
                print('{:4} "{}" {!r}'.format(self._primary_format.typ_name, arg, res))
                continue
            print('{:4} "{}" {!r}'.format(self._secondary_format.typ_name, arg, res))

    def sort(self):
        if self._args.dryrun and self._args.verbose == 0:
            self._args.verbose = 2
        updated_dirs = {}
        tmp_path = self._config['tmp_path']
        self.dbg(tmp_path)
        pri = self._primary_format
        sec = self._secondary_format
        self.dbg('primary', pri.typ_name)
        self.dbg('secondary', sec.typ_name)
        to_convert = []
        total_files = 0
        files_done = 0
        # build up this list, immediately so additional data copied in later, doesn't interfere
        # especially necessary for slow --convert 
        to_do = []  
        for root, directory_names, file_names in pl.walk(tmp_path):
            if self._args.startwith and not str(root).startswith(self._args.startwith):
                continue
            total_files += len(file_names)
            to_do.append((root, directory_names, file_names))
#        for root, directory_names, file_names in pl.walk(tmp_path):
#            if self._args.startwith and not str(root).startswith(self._args.startwith):
#                continue
        for root, directory_names, file_names in to_do:
            sec_target_dir = None
            pri_target_dir = None
            rm_from_file_names = []
            directory_names.sort()
            file_names.sort()
            # add this to the YAML metadata
            if file_names:  # no filenames means intermediary path
                _, artist, album = str(root).rsplit('/', 2)
                updated_dirs[root] = d = CommentedMap()
                d['artist'] = artist
                d['path'] = '{}/{}'.format(artist, album)
                try:
                    year, album = album.split(' - ', 1)
                except ValueError:
                    continue
                org_year = ''
                for file_name in file_names:
                    if pri.has_extension(file_name):
                        typ = pri(root / file_name)
                        if typ.original_year != year:
                            org_year = typ.original_year
                        break
                    elif sec.has_extension(file_name):
                        typ = sec(root / file_name)
                        if typ.original_year != year:
                            org_year = typ.original_year
                        break
                d['album'] = album
                d['year'] = year
                year_info = '{} ({})'.format(org_year, year) if org_year else year
                album_info = 'artist: "{}", album: "{}" [{}]'.format(artist, album, year_info)
                if total_files > 100:
                    print('{} ({}/{})'.format(album_info, files_done, total_files))
                else:
                    print(album_info)
            sys.stdout.flush()
            # continue
            for file_name in file_names:
                files_done += 1
                full_name = pl.path.join(root, file_name)
                if pri.has_extension(file_name):
                    if not pri_target_dir:
                        try:
                            pri_target_dir = root.replace(tmp_path, pri.path)
                        except TypeError:
                            print('\n{!r}\n{!r}\n'.format(root, pri.path))
                            raise
                        if org_year:
                            assert year in str(pri_target_dir)
                            try:
                                pri_target_dir = Path(
                                    str(pri_target_dir).replace(year, org_year, 1)
                                )
                            except UnicodeDecodeError:
                                # print('1', type(str(pri_target_dir)))
                                # print('2', type(year))
                                # print('3', type(org_year))
                                pri_target_dir = Path(
                                    str(pri_target_dir)
                                    .decode('utf-8')
                                    .replace(u'{}'.format(year), u'{}'.format(org_year), 1)
                                )
                    self.dbg('match primary', pri_target_dir)
                    if not pl.path.exists(pri_target_dir):
                        pl.makedirs(pri_target_dir)
                    target = pl.path.join(pri_target_dir, file_name)
                    if not self._args.dryrun:
                        pl.rename(full_name, target)
                    self.pr('moving to', target)
                    rm_from_file_names.append(file_name)
                    d['typ'] = pri.typ_name
                    self.prisec(pri_target_dir)  # delayed conversion (not used)
                    if self._args.convert:
                        self.try_convert_one(target)
                        # to_convert.append(target)
                elif sec.has_extension(file_name):
                    if not sec_target_dir:
                        sec_target_dir = root.replace(tmp_path, sec.path)
                        if org_year:
                            assert year in str(sec_target_dir)
                            sec_target_dir = Path(
                                str(sec_target_dir).replace(year, org_year, 1)
                            )
                    self.dbg('match secondary', sec_target_dir)
                    if not pl.path.exists(sec_target_dir):
                        pl.makedirs(sec_target_dir)
                    target = pl.path.join(sec_target_dir, file_name)
                    if not self._args.dryrun:
                        pl.rename(full_name, target)
                    self.pr('moving to', target)
                    rm_from_file_names.append(file_name)
                    d['typ'] = sec.typ_name
            sys.stdout.flush()
            # remove processed files from list
            for file_name in rm_from_file_names:
                file_names.remove(file_name)
            for file_name in file_names:
                base, ext = pl.path.splitext(file_name)
                if ext in other_suffixes:
                    src = pl.path.join(root, file_name)
                    if pri_target_dir:
                        target = pl.path.join(pri_target_dir, str(file_name))
                    elif sec_target_dir:
                        target = pl.path.join(sec_target_dir, str(file_name))
                    else:  # if no music files don't know where to put
                        raise NotImplementedError
                    self.dbg('copying', ext, 'to', target)
                    if not self._args.dryrun:
                        pl.copy(src, target)
                    if not self._args.dryrun:
                        pl.remove(src)
        # update new files yaml
        for updated_dir in updated_dirs:
            self.dbg('udpated_dir', updated_dir)
            dd = datetime.datetime.fromtimestamp(pl.path.getmtime(updated_dir))
            data = updated_dirs[updated_dir]
            self.add_to_yaml(dd, data)
        if updated_dirs:
            yaml = ruamel.yaml.YAML()
            yaml.dump(
                self._mapping,
                open(self.yaml_file_name, 'w'),
            )
            self.convert_yaml_html()
        self.remove_empty_dirs(tmp_path)
        if to_convert:
            for idx, target in enumerate(to_convert):
                self.try_convert_one(target, '{}/{}'.format(idx, len(to_convert)))

    def try_convert_one(self, path, progress=''):
        print('converting{}{}: {}'.format(' ' if progress else '', progress, path))
        try:
            self.converter.files_in_one_dir(self, [path], force=True)
        except Exception as e:
            print('exception converting', e)

    @property
    def converter(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, Convert())
        return getattr(self, attr)

    def remove_empty_dirs(self, base):
        # remove all the empty directories, just try to do it an fail gracefully
        to_remove = []
        for root, directory_names, file_names in pl.walk(base, topdown=False):
            for d in directory_names:
                to_remove.append(pl.path.join(root, d))
        for d in to_remove:
            try:
                pl.rmdir(d)
            except:
                pass

    prisec_dir_name = '/data0/Music/.prisec'

    def prisec(self, directory):
        # not sure why I added this, but this could be used for delayed conversion
        if not pl.path.exists(self.prisec_dir_name):
            pl.makedirs(self.prisec_dir_name)
        file_name = directory
        for x in ' :-/':
            file_name = file_name.replace(x, '__')
        full_name = pl.path.join(self.prisec_dir_name, str(file_name))
        # print('fullname', full_name)
        if not pl.path.exists(full_name):
            self.dbg('scheduling', full_name)
            with open(full_name, 'w') as fp:
                try:
                    fp.write(str(directory))
                except Exception as e:
                    print('directory type:', type(directory))
                    raise

    def convert_yaml_html(self):
        html_file_name = pl.path.join(pl.path.dirname(self.yaml_file_name), 'music.html')
        self.dbg('convert_yaml_html', pl.path.exists(html_file_name))
        force = getattr(self._args, 'force', None)
        if force and pl.path.exists(html_file_name) and (
            pl.path.getmtime(html_file_name) > pl.path.getmtime(self.yaml_file_name)
        ):
            return
        self.dbg('convert_yaml_html 23')
        yaml = ruamel.yaml.YAML()
        lst = yaml.load(open(self.yaml_file_name))
        print('length of yaml:', len(lst))
        paths = set()
        try:
            try:
                with SimpleHtml(html_file_name, 'New music') as html:
                    for count, x in enumerate(sorted(lst, reverse=True)):
                        try:
                            # if count > 25:
                            #     break
                            m = lst[x]
                            path = m['path']
                            if path in paths:
                                self.dbg('found', path)
                                continue
                            paths.add(path)
                            # if m.get('url'):
                            #     music = u'<a target=_new href="{url}">{name}</a>'.format(**m)
                            # else:
                            #     music = m['name']
                            data = [m['artist'], m['album'], m['year']]
                            # if m.get('path'):
                            #     data.append(u'<a target=_new href="file://V:/{}">{}</a>'.
                            #                 format(m.get('path'), x.date()))
                            # else:
                            data.append(x.date())
                            html.add_row(data)
                        except KeyError as e:
                            print('keyerror', e, 'not in', m)
            except KeyError:
                print('m', m)
        except:
            pl.remove(html_file_name)
            raise

    def pr(self, *args, **kw):
        # higher levels, the more --verbose you need to specify to see
        lvl = kw.pop('level', 0)
        if self._args.verbose < lvl:
            return
        print(*args, **kw)

    def dbg(self, *args, **kw):
        """print at verbosity level 2 or higher"""
        if 'level' not in kw:
            kw['level'] = 2
        self.pr(*args, **kw)

    def trace(self, *args, **kw):
        """print at verbosity level 1 or higher"""
        if 'level' not in kw:
            kw['level'] = 1
        self.pr(*args, **kw)

    yaml_file_name = '/data0/Music/.music.yaml'

    def add_to_yaml(self, dd, data):
        if self._mapping is None:
            if not pl.path.exists(self.yaml_file_name):
                self._mapping = CommentedMap()
            else:
                yaml = ruamel.yaml.YAML()
                self._mapping = yaml.load(
                    open(self.yaml_file_name), 
                )
                if self._mapping is None:
                    self._mapping = CommentedMap()
        self._mapping[dd] = data

    def analyse(self):
        album_dirs = ordereddict()  # may have multiple subdirs like [CD1, CD2]
        dirs = ['.'] if not self._args.args else self._args.args
        for d in dirs:
            self.get_album_dirs(d, album_dirs=album_dirs)
        for ad in album_dirs:
            typ = album_dirs[ad]
            print(ad)
            # print('ad', ad, album_dirs[ad])
            typ.check_non_relevant_files(remove=True)
            typ.check_images(move=True)
            typ.check_empty_dirs(remove=True)
        print('done')

    def get_album_dirs(self, d, album_dirs=None, extensions=None):
        if extensions is None:
            extensions = ['mp3', 'flac', 'wav', 'wv']
        potential_dirs = ordereddict()
        for root, directory_names, file_names in os.walk(d):
            root = Path(root)
            if root.parent in potential_dirs:
                continue
            directory_names.sort()
            album_type = AlbumType()
            for file_name in file_names:
                file_ext = file_name.rsplit('.')[-1].lower()
                for ext in extensions:
                    if ext == file_ext:
                        stem = root.stem.lower()
                        for mcd in ['cd1', 'cd01', 'cd 1', 'cd2', 'cd02', 'cd 2']:
                            if mcd in stem:
                                album_type.set_subdir(root.stem)
                                root = root.parent
                                break
                        if not str(root).startswith('test_') and not str(root).startswith('_UNPACK'):
                            potential_dirs[root] = album_type
                            album_type.set_dir(root)
                        break
                else:
                    continue
                break
        #for x in potential_dirs:
        #    print(x)
        if album_dirs is not None:
            album_dirs.update(potential_dirs)
        return potential_dirs

    def flatten(self):
        suffixes = []
        for i in globals():
            t = getattr(sys.modules[__name__], i)
            try:
                if not issubclass(t, BaseMusicFormat):
                    continue
            except TypeError:
                continue
            if not hasattr(t, '_suffixes'):
                continue
            suffixes.extend(t._suffixes)
        dirs = ['.'] if not self._args.args else self._args.args
        for d in dirs:
            self.flatten_dir(d, suffixes)

    def flatten_dir(self, d, suffixes):
        def rm_empty_dirs(root, dir_names):
            for d in dir_names:
                path = pl.path.join(root, d)
                if dir_is_empty(path):
                    pl.rmdir(path)
                    dir_names.remove(d)

        def has_music(dir_name, file_names):
            for fn in file_names:
                base_name, ext = pl.path.splitext(fn)
                if ext in suffixes:
                    return True
            return False

        def dir_is_empty(d):
            return len(pl.listdir(d)) == 0

        def move_images_here(root, dir_names):
            # image extensions should match picards
            image_extensions = ['.jpg', '.gif', '.png', '.pdf']
            for dir_name in dir_names:
                path = pl.path.join(root, dir_name)
                for file_name in pl.listdir(path):
                    basename, ext = pl.path.splitext(file_name)
                    ext_lower = ext.lower()
                    if ext_lower == '.jpeg':
                        ext_lower = '.jpg'
                    if ext_lower not in image_extensions:
                        continue
                    pl.rename(
                        pl.path.join(path, file_name), pl.path.join(root, basename + ext_lower)
                    )

        for root, dir_names, file_names in pl.walk(d):
            rm_empty_dirs(root, dir_names)
            if not dir_names:  # no subdirectory that may contain images
                continue
            if not has_music(root, file_names):
                print('trying alt root for music')
                for music_sub in ['CD1']:
                    alt_root = Path(root) / music_sub
                    print(alt_root)
                continue
            # we  have subdir(s) and music files, move any images
            move_images_here(root, dir_names)
            print('moving images', root)
            rm_empty_dirs(root, dir_names)
            # for file_name in file_names:
            #     print(root, file_name)

    def meta(self):
        for path in self._args.args:
            if path.suffix == '.mp3':
                in_file = MP3(path)
            elif path.suffix == '.flac':
                in_file = FLAC(path)
            print(path)
            for tag in sorted(in_file.tags):
                print(' ', tag, in_file.tags[tag])
            print('  cover_art:', in_file.has_cover_art)

    def image(self):
        if self._args.get:
            path = self._args.get[0]
            self.get_file_cover_art(path)
            return
        if self._args.check:
            print('checking for images on', self._args.check)
            for path in self._args.check:
                if path.is_dir():
                    self.check_dirs_for_cover_art(path)
                else:
                    self.check_file_for_cover_art(path)
            return
        if self._args.mp3:

            def best_image(l, d):
                if len(l) == 1:
                    return l[0]
                order = {}
                idx = 7
                for fn in l:
                    ln = fn.lower()
                    if '00' in ln and 'front' in ln:
                        order[1] = fn
                        continue
                    if '00' in ln and 'cover' in ln:
                        order[2] = fn
                        continue
                    if 'cover' in ln and 'front' in ln:
                        order[3] = fn
                        continue
                    if 'front' in ln:
                        order[4] = fn
                        continue
                    if 'cover' in ln:
                        order[5] = fn
                        continue
                    if 'folder' in ln:
                        order[6] = fn
                        continue
                    order[idx] = fn
                    idx += 1
                for k in sorted(order):
                    if k > 6:
                        print('order', order, d)
                    return order[k]

            sec = self._secondary_format
            count = 0
            image_count = 0
            image_names = set()
            offset = len(str(sec.path)) + 3
            has_cover_count = 0
            for root, dir_names, file_names in pl.walk(sec.path, topdown=False):
                sys.stdout.flush()
                nr_mp3 = len([x for x in file_names if x.endswith('.mp3')])
                if nr_mp3 == 0:
                    continue
                count += 1
                root_path = Path(root)
                has_cover = root_path / '.has_cover'
                if has_cover.exists():
                    has_cover_count += 1
                    continue
                for file_name in file_names:
                    break
                    if not file_name.endswith('.mp3'):
                        continue
                    full_name = root_path / file_name
                    out_file = MP3(full_name)
                    if not out_file.has_cover_art:
                        break
                else:
                    has_cover.write_bytes(b'')
                    continue
                possible_cover_art_names = []
                for file_name in file_names:
                    if file_name.endswith('.mp3'):
                        continue
                    nl = file_name.lower()
                    if 'front' in nl or 'cover' in nl or 'folder' in nl:
                        # print('cover found <<<<<<<<', file_name)
                        possible_cover_art_names.append(file_name)
                        image_count += 1
                        # image_names.add(file_name.lower())
                if possible_cover_art_names:
                    bi = root_path / best_image(possible_cover_art_names, root)
                    print('bi', bi)
                    for file_name in file_names:
                        if not file_name.endswith('.mp3'):
                            continue
                        try:
                            fn = root_path / file_name
                            self.add_to_mp3(fn, bi)
                        except AttributeError:
                            print('>>> error in adding to', fn)
                            break
                    else:
                        has_cover.write_bytes(b'')
                    # print(root, nr_mp3)
            print('count', count, image_count, has_cover_count)
            # print('image_names', image_names)
            return
        if self._args.all:
            pri = self._primary_format
            sec = self._secondary_format
            # print('primary', pri.typ_name, pri.path)
            # print('secondary', sec.typ_name)
            count = 0
            image_count = 0
            offset = len(str(pri.path)) + 3
            has_cover_count = 0
            for root, dir_names, file_names in pl.walk(pri.path, topdown=False):
                sys.stdout.flush()
                root_path = Path(root)
                mp3_path = Path(str(root).replace('/FLAC/', '/MP3/'))
                has_cover = mp3_path / '.has_cover'
                if has_cover.exists():
                    has_cover_count += 1
                    continue
                has_cover_art = False
                for file_name in file_names:
                    if not file_name.endswith('.flac'):
                        continue
                    if not file_name.startswith('01'):
                        continue
                    file_name = root_path / file_name
                    count += 1
                    if has_cover_art:
                        image_count += 1
                        print(
                            '*', str(file_name)[offset:-5], len(list(mp3_path.glob('*.mp3')))
                        )
                        continue
                    in_file = FLAC(file_name)
                    if in_file.has_cover_art:
                        image_count += 1
                        has_cover_art = True
                        print(
                            '*', str(file_name)[offset:-5], len(list(mp3_path.glob('*.mp3')))
                        )
                        all_done = True
                        for out_name in mp3_path.glob('*.mp3'):
                            # print(out_name)
                            if not self.copy_cover_art(in_file, out_name):
                                all_done = False
                        if all_done:
                            try:
                                has_cover.write_bytes(b'')
                            except IOError:
                                print('cannot write', has_cover)
                            continue
                    else:
                        print(' ', str(file_name)[offset:-5])
            print('count', count, image_count, has_cover_count)
            return
        in_path = getattr(self._args, 'from')
        out_path = self._args.to
        if in_path.suffix == '.flac':
            in_file = FLAC(in_path)
        if out_path.suffix == '.mp3':
            out_file = MP3(out_path)
        if out_file.has_cover_art:
            print('already done')
            return
        if not in_file.has_cover_art:
            return
        # print('cover art', in_file.first_cover_art)

    def add_to_mp3(self, path, image_path):
        assert path.suffix == '.mp3'
        out_file = MP3(path)
        if out_file.has_cover_art:
            return
        out_file.add_image(image_path)

    def copy_cover_art(self, in_file, out_path):
        if not isinstance(in_file, FLAC):
            assert in_path.suffix == '.flac'
            in_file = FLAC(in_path)
        if not in_file.has_cover_art:
            return False
        assert out_path.suffix == '.mp3'
        out_file = MP3(out_path)
        if out_file.has_cover_art:
            return True
        out_file.add_picture(in_file.first_cover_art)
        return True

    def get_file_cover_art(self, path):
        import musicbrainzngs

        music_file = None
        if self._primary_format.has_extension(path):
            music_file = self._primary_format(path)
        elif self._secondary_format.has_extension(path):
            music_file = self._secondary_format(path)
        print(path)
        if not music_file:
            print('not recognised')
            return False
        tags = music_file.tags
        if False:
            for tag in tags:
                print('', tag, tags[tag])
            sys.exit(0)
        album_id = tags.get('musicbrainz_albumid')
        release_id = tags.get('musicbrainz_releaseid')
        # print(album_id)
        cover_art_file = path.parent / MB_FRONT
        # print(cover_art_file)
        # image_list = musicbrainzngs.get_image_list(album_id)
        # ruamel.yaml.round_trip_dump(image_list, sys.stdout)
        # print(image_list)
        image = None
        try:
            image = musicbrainzngs.get_image_front(album_id, 500)
        except Exception as e:
            if '503' in str(e):
                raise
            if release_id:
                try:
                    image = musicbrainzngs.get_release_group_image_front(release_id, 500)
                except Exception as e:
                    print('exception', e)
                    if '503' in str(e):
                        raise
        if image is not None:
            print('writing ca', path.parent)
            cover_art_file.write_bytes(image)
            return True
        return False

    def check_dirs_for_cover_art(self, path, show_all=False, check_files=True):
        count = 0
        for root, dir_names, file_names in pl.walk(path):
            sys.stdout.flush()
            if not file_names:
                continue
            mb_no_cover = root / '.mb_no_cover'
            if mb_no_cover.exists():
                continue
            has_cover = root / '.has_cover'
            mb_front = root / MB_FRONT
            if has_cover.exists() or mb_front.exists():
                if show_all:
                    print('*{}'.format(root))
                continue
            music_file = None
            if check_files and not has_cover.exists():
                for file_name in sorted(file_names):
                    file_name = Path(file_name)
                    if self._primary_format.has_extension(file_name):
                        music_file = self._primary_format(root / file_name)
                        break
                    elif self._secondary_format.has_extension(file_name):
                        music_file = self._secondary_format(root / file_name)
                        break
                    else:
                        continue
            if music_file is None:
                continue
            res = self.get_file_cover_art(music_file._path)
            if res:
                time.sleep(5)
                continue
            else:
                mb_no_cover.write_bytes(b'')
            link_found = False
            for file_name in file_names:
                if '.desktop' in file_name:
                    link_found = True
                    break
            if link_found:
                continue
            if music_file and music_file.has_cover_art:
                has_cover.write_bytes(b'')
            if not has_cover.exists():
                count += 1
                print('{}{}'.format(' ' if show_all else '', root))
                if music_file:
                    print(' ', music_file.has_cover_art)
        print('count', count)

    @property
    def tmp_path(self):
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            setattr(self, attr, Path(self._config['tmp_path']))
        return getattr(self, attr)

    def cleanup(self):
        if self._args.dedup:
            return self.cleanup_dedup()
        if self._args.year:
            return self.cleanup_year()
        empty_directories = []
        print(self.tmp_path)
        one_done = True
        while one_done:
            one_done = False
            for root, dir_names, file_names in pl.walk(self.tmp_path, topdown=False):
                print(root, dir_names, file_names)
                if root == self.tmp_path:
                    break
                if not dir_names and not file_names:
                    empty_directories.append(root)
            for name in empty_directories:
                one_done = True
                try:
                    name.rmdir()
                except:
                    pass

    def cleanup_dedup(self):
        pri = self._primary_format
        sec = self._secondary_format
        for root, dir_names, file_names in pl.walk(pri.path):
            # paths with : used to be changed to _
            for d in dir_names:
                if ':' not in d:
                    continue
                old = d.replace(':', '_')
                if old not in dir_names:
                    continue
                x = root / old
                print('x', x)
                fl = list(x.glob('*'))
                print('l', len(fl), fl)
                if (
                    len(fl) == 0
                    or len(fl) == 1
                    and fl[0].name in ['.has_cover', '.mb_no_cover']
                ):
                    y = x.replace(pri.path, sec.path)
                    if y.exists():
                        print('y', y)
                        y.rmtree()
                    x.rmtree()
                sys.stdout.flush()
            # paths ending in '.'
            for d in dir_names:
                if d[-1] != '.':
                    continue
                old = d[:-1] + '_'
                if old not in dir_names:
                    continue
                x = root / old
                print('z', x)
                for fn in x.glob('*.flac'):
                    fn.unlink()
                for fn in x.glob('*'):
                    if fn.suffix.lower() in other_suffixes:
                        fn.move(root / d)
                fl = list(x.glob('*'))
                print('l', len(fl), fl)
                if (
                    len(fl) == 0
                    or len(fl) == 1
                    and fl[0].name in ['.has_cover', '.mb_no_cover']
                ):
                    y = x.replace(pri.path, sec.path)
                    if y.exists():
                        print('y', y)
                        y.rmtree()
                    x.rmtree()
                sys.stdout.flush()

        print('done')
        sys.stdout.flush()

    def cleanup_year(self):
        if self._args.gen:
            return self.cleanup_year_gen()
        ymd = ruamel.yaml.round_trip_load(self.year_meta_data_file)
        count0 = count1 = 0
        for artist_path in ymd:
            albi = ymd[artist_path]
            # first the ones already in right place
            for album in albi:
                year, org_year = albi[album]
                if not album.startswith(str(org_year)):
                    continue
                ok_flac_path = Path(artist_path) / album
                new_flac_path = ok_flac_path.replace(org_year, year, 1)
                ok_mp3_path = ok_flac_path.replace('FLAC', 'MP3', 1)
                new_mp3_path = new_flac_path.replace('FLAC', 'MP3', 1)
                if not new_flac_path.exists() and not new_mp3_path.exists():
                    # cleaned up
                    continue
                count0 += 1
                print('1: {!r} {!r} {} {}'.format(artist_path, album, year, org_year))
                print(new_flac_path.exists(), ok_mp3_path.exists(), new_mp3_path.exists())
                if new_mp3_path.exists():
                    # just remove MP3 files, can generate from FLAC
                    for fn in new_mp3_path.glob('*.mp3'):
                        fn.unlink()
                    for fn in new_mp3_path.glob('*'):
                        if fn.name in ['.has_cover', '.no_mb_cover']:
                            fn.unlink()
                            continue
                        org = ok_flac_path / fn.name
                        if org.exists():
                            fn.unlink()
                            continue
                        print(fn)
                    if len(list(new_mp3_path.glob('*'))) == 0:
                        new_mp3_path.rmdir()
                if new_flac_path.exists():
                    for fn in new_flac_path.glob('*.flac'):
                        print(fn)
                        raise NotImplementedError
                    for fn in new_flac_path.glob('*'):
                        if fn.name in ['.has_cover', '.mb_no_cover']:
                            fn.unlink()
                            continue
                        print(fn)
                    if len(list(new_flac_path.glob('*'))) == 0:
                        new_flac_path.rmdir()
                    # print(new_flac_path)
            for album in albi:
                year, org_year = albi[album]
                if album.startswith(str(org_year)):
                    continue
                new_flac_path = Path(artist_path) / album
                ok_flac_path = new_flac_path.replace(year, org_year, 1)
                ok_mp3_path = ok_flac_path.replace('FLAC', 'MP3', 1)
                new_mp3_path = new_flac_path.replace('FLAC', 'MP3', 1)
                if not new_flac_path.exists() and not new_mp3_path.exists():
                    # cleaned up
                    continue
                if new_flac_path.exists() and ok_flac_path.exists():
                    for fn in ok_flac_path.glob('*'):
                        if fn.name in ['.has_cover', '.mb_no_cover']:
                            fn.unlink()
                            continue
                        print(fn)
                    if len(list(ok_flac_path.glob('*'))) == 0:
                        ok_flac_path.rmdir()
                        continue

                count1 += 1
                print('2: {!r} {!r} {} {}'.format(artist_path, album, year, org_year))
                print(
                    ok_flac_path.exists(),
                    new_flac_path.exists(),
                    ok_mp3_path.exists(),
                    new_mp3_path.exists(),
                )
                if (
                    not ok_flac_path.exists()
                    and new_flac_path.exists()
                    and not ok_mp3_path.exists()
                    and new_mp3_path.exists()
                ):
                    # just rename
                    new_flac_path.rename(ok_flac_path)
                    new_mp3_path.rename(ok_mp3_path)
                    continue
                if ok_flac_path.exists() and new_flac_path.exists():
                    raise NotImplementedError
                if new_flac_path.exists():
                    new_flac_path.rename(ok_flac_path)
                # ok_flac_count = len(list(ok_flac_path.glob('*.flac')))
                # new_flac_count = len(list(new_flac_path.glob('*.flac')))
                if ok_mp3_path.exists() and new_mp3_path.exists():
                    for fn in new_mp3_path.glob('*'):
                        target = ok_mp3_path / fn.name
                        if target.exists():
                            target.unlink()
                        fn.rename(target)
                    if len(list(new_mp3_path.glob('*'))) == 0:
                        new_mp3_path.rmdir()

            sys.stdout.flush()
        print('done', count0, count1)

    @property
    def year_meta_data_file(self):
        return Path(self._config.file_in_config_dir('year.yaml'))

    def cleanup_year_gen(self):
        # print(self.year_meta_data_file)
        ymd = CommentedMap()

        pri = self._primary_format
        sec = self._secondary_format
        to_remove = []
        count = 0
        for root, dir_names, file_names in pl.walk(pri.path):
            dir_names.sort()
            if root.name == 'xFLAC':  # 'A' in dir_names:
                print(root)
                for c in 'BCDEFGHIJKLMNOPQRSTUVWYZ':
                    dir_names.remove(c)
            sys.stdout.flush()
            if not file_names:
                continue
            # skip intermediary directories
            if str(root).count('/') - str(pri.path).count('/') < 2:
                continue
            # if len(file_names) == 1 and file_names[0] in ['.has_cover', '.mb_no_cover']:
            #     to_remove.append(root)
            p = None
            for x in file_names:
                x1 = root / x
                if x1.suffix != '.flac':
                    continue
                p = pri(x1)
                break
            else:
                # print('root', root, file_names, str(root).count('/'))
                continue

            org_year = p.original_year
            if org_year is None:
                continue
            if p.year == org_year:
                continue
            artist_path = p._path.parent.parent
            album = p._path.parent.name  # might be different from what is in tags
            print(artist_path, album, p.year, org_year)
            ymd.setdefault(str(artist_path), CommentedMap())[album] = [
                int(p.year),
                int(org_year),
            ]
            count += 1
            sys.stdout.flush()
        for d in to_remove:
            print('rm', d)

            continue

            # paths with : used to be changed to _
            for d in dir_names:
                if ':' not in d:
                    continue
                old = d.replace(':', '_')
                if old not in dir_names:
                    continue
                x = root / old
                print('x', x)
                fl = list(x.glob('*'))
                print('l', len(fl), fl)
                if (
                    len(fl) == 0
                    or len(fl) == 1
                    and fl[0].name in ['.has_cover', '.mb_no_cover']
                ):
                    y = x.replace(pri.path, sec.path)
                    if y.exists():
                        print('y', y)
                        y.rmtree()
                    x.rmtree()
                sys.stdout.flush()
            # paths ending in '.'
        print('count', count)
        # ruamel.yaml.round_trip_dump(ymd, sys.stdout)
        ruamel.yaml.round_trip_dump(ymd, self.year_meta_data_file)


"""
bi /data0/Music/MP3/B/Björk/1977 - Björk/Cover.jpg
bi /data0/Music/MP3/B/Björk/1994 - Debut/Cover 6.jpg
bi /data0/Music/MP3/B/Björk/2001 - Post/Cover 19.jpg
bi /data0/Music/MP3/B/Björk/2002 - Greatest Hits/Cover 7.jpg
bi /data0/Music/MP3/B/Björk/2004 - Medúlla/Cover 7.jpg
bi /data0/Music/MP3/B/Björk/2007 - Volta/Cover.jpg
bi /data0/Music/MP3/B/Björk/2008 - Vespertine/Cover 6.jpg
bi /data0/Music/MP3/B/Björk/2011 - Biophilia/Front.jpg
bi /data0/Music/MP3/B/Black Eyed Peas, The/1998 - Behind the Front/00-the_black_eyed_peas-behind_the_front-cd-flac-1998-blackeyedpeas.jpg
"""
