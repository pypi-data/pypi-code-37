# coding: utf-8

from __future__ import print_function

import sys
import os
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


from ruamel.std.pathlib import PosixPath

from ruamel.doc.html.simple import SimpleHtml

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap


from ruamel.music.stemanalyser import StemAnalyser

# valkeys = EasyID3.valid_keys.keys()
# print(valkeys)
# sys.exit(1)

CalledProcessError = subprocess.CalledProcessError


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
        print('message', e.message)
        try:
            print('output', e.output)
        except:
            pass
        print(dir(e))
        sys.exit(1)


stem_analyser = StemAnalyser()


class Path(PosixPath):
    def analyse(self):
        return stem_analyser(self.stem)


class BaseMusicFormat(object):
    valid_tag_keys = EasyID3.valid_keys.keys()

    def __init__(self, path=None, verbose=0):
        self._path = Path(path) if isinstance(path, basestring) else path
        self._verbose = verbose
        self._tags = {}

    def dump_tags(self):
        if self._verbose < 0:
            return
        print('tags:')
        for k in sorted(self._tags):
            v = self._tags[k]
            if len(v) > 32:
                continue
            print(u'  {:15}: {}'.format(k, v))

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
        # x = self._flac.get('musicbrainz_trackid')

    def from_wav(self, wav):
        cmd = ['flac', '--silent', '--best', '--force', '--output-name', self._path, wav._path]
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
            # cmd = ['ffmpeg', '-i', self._path, wav._path]
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
        self.try_cmd(cmd)

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
        # """uses faad"""
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
            '2',
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
        for k in sorted(self._tracks):
            wav = WAV(tmpdir / '{:02}{}'.format(k, WAV._suffixes[0]))
            t = self._tracks[k]['title'].encode('utf-8')
            out_file = FLAC(path / '{:02} - {}{}'.format(k, t, fsuf))
            print('flac', out_file._path)
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
        # try:
        #     target = self._args.target
        # except AttributeError:
        #     target_format = music._primary_format
        file_names = []
        for pat in music._args.args:
            file_names.extend(glob.glob(os.path.expanduser(pat)))
        home_dir = os.path.expanduser('~')
        for file_name in file_names:
            rm_tmp_file = None
            if verbose > 0:
                print('converting file_name', file_name)
            path = Path(os.path.abspath(file_name))
            cue_file = Path(file_name) if music._args.cue else None
            if not cue_file and not music._args.no_cue_check:
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
                if music._args.max_size * 1024 ** 32 < os.path.getsize(file_name):
                    if verbose > 0:
                        print('too big, skipping')
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
                if verbose < 0:
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
            else:
                print('Unknown file type:', path.suffix)
            if rm_tmp_file:
                rm_tmp_file.remove()


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
        self.path = kw.pop('path')

    def __call__(self, *args, **kw):
        return self.tcls(*args, **kw)

    @staticmethod
    def tup_name(s, drop_int=False):
        if not isinstance(s, unicode):
            s = s.decode('utf-8')
        s = s.lower()
        n = []
        bn = os.path.basename(s)
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
        glob_path = os.path.join(self.path, name, '*')
        base_len = len(self.path) + len(name) + 1
        for full_name in glob.glob(glob_path):
            name = os.path.basename(full_name)
            # sname = name.split()
            name = self.tup_name(name, drop_int=True)
            names[name] = [full_name[base_len + 1 :]]
            # print(name)
        return names

    def get_names(self, base, letter):
        names = {}
        glob_path = os.path.join(base, letter, '*')
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
        #     print name, os.path.join(root,

    def match_releases(self, name, rel):
        if name[1] is None:
            name[1] = self.get_releases(name[0])
        trel = self.tup_name(rel, drop_int=True)
        # print('relname', name, trel)
        return name[1].get(trel)

    def match_names(self, letter, name):
        names = self._letter_names.setdefault(letter, self.get_names(self.path, letter))
        tname = self.tup_name(name)
        return names.get(tname)

    def find(self, name):
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
            m = self.match_names(l, x)
            if m:
                # print(x, y)
                r = self.match_releases(m, y)
                # print('r', r)
                if r:
                    return os.path.join(m[0], r[0])

    def exists(self, sub_path):
        full_path = os.path.join(self.path, sub_path)
        return os.path.exists(full_path)

    def has_extension(self, file_name):
        base, ext = os.path.splitext(file_name)
        return ext in self.tcls._suffixes


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
        convert = Convert()
        convert(self)

    def find(self):
        # assume secondary format has everything the primary format has
        if self._args.args == ['*']:
            args = sorted(glob.glob('*'))
        else:
            args = self._args.args
        for arg in args:
            res = self._secondary_format.find(arg)
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
        for root, directory_names, file_names in os.walk(tmp_path):
            sec_target_dir = None
            pri_target_dir = None
            rm_from_file_names = []
            # add this to the YAML metadata
            if file_names:  # no filenames means intermediary path
                _, artist, album = root.rsplit('/', 2)
                updated_dirs[root] = d = CommentedMap()
                d['artist'] = artist
                d['path'] = '{}/{}'.format(artist, album)
                try:
                    year, album = album.split(' - ', 1)
                except ValueError:
                    continue
                d['album'] = album
                d['year'] = year
                print('artist: "{}", album: "{}" [{}]'.format(artist, album, year))
            for file_name in file_names:
                full_name = os.path.join(root, file_name)
                if pri.has_extension(file_name):
                    if not pri_target_dir:
                        pri_target_dir = root.replace(tmp_path, pri.path)
                    self.dbg('match primary', pri_target_dir)
                    if not os.path.exists(pri_target_dir):
                        os.makedirs(pri_target_dir)
                    target = os.path.join(pri_target_dir, file_name)
                    if not self._args.dryrun:
                        os.rename(full_name, target)
                    self.pr('moving to', target)
                    rm_from_file_names.append(file_name)
                    d['typ'] = pri.typ_name
                    self.prisec(pri_target_dir)
                elif sec.has_extension(file_name):
                    if not sec_target_dir:
                        sec_target_dir = root.replace(tmp_path, sec.path)
                    self.dbg('match secondary', sec_target_dir)
                    if not os.path.exists(sec_target_dir):
                        os.makedirs(sec_target_dir)
                    target = os.path.join(sec_target_dir, file_name)
                    if not self._args.dryrun:
                        os.rename(full_name, target)
                    self.pr('moving to', target)
                    rm_from_file_names.append(file_name)
                    d['typ'] = sec.typ_name
            # remove processed files from list
            for file_name in rm_from_file_names:
                file_names.remove(file_name)
            for file_name in file_names:
                base, ext = os.path.splitext(file_name)
                if ext in ['.jpg', '.m3u', '.cue', '.png']:
                    src = os.path.join(root, file_name)
                    if pri_target_dir:
                        target = os.path.join(pri_target_dir, file_name)
                    elif sec_target_dir:
                        target = os.path.join(sec_target_dir, file_name)
                    self.dbg('copying', ext, 'to', target)
                    if not self._args.dryrun:
                        shutil.copy(src, target)
                    if not self._args.dryrun:
                        os.remove(src)
        # update new files yaml
        for updated_dir in updated_dirs:
            self.dbg('udpated_dir', updated_dir)
            dd = datetime.datetime.fromtimestamp(os.path.getmtime(updated_dir))
            data = updated_dirs[updated_dir]
            self.add_to_yaml(dd, data)
        if updated_dirs:
            ruamel.yaml.dump(
                self._mapping,
                open(self.yaml_file_name, 'w'),
                Dumper=ruamel.yaml.RoundTripDumper,
            )
            self.convert_yaml_html()
        self.remove_empty_dirs(tmp_path)

    def remove_empty_dirs(self, base):
        # remove all the empty directories, just try to do it an fail gracefully
        to_remove = []
        for root, directory_names, file_names in os.walk(base, topdown=False):
            for d in directory_names:
                to_remove.append(os.path.join(root, d))
        for d in to_remove:
            try:
                os.rmdir(d)
            except:
                pass

    prisec_dir_name = '/data0/Music/.prisec'

    def prisec(self, directory):
        if not os.path.exists(self.prisec_dir_name):
            os.makedirs(self.prisec_dir_name)
        file_name = directory
        for x in ' :-/':
            file_name = file_name.replace(x, '__')
        full_name = os.path.join(self.prisec_dir_name, file_name)
        if not os.path.exists(full_name):
            self.dbg('scheduling', full_name)
            with open(full_name, 'w') as fp:
                fp.write(directory)

    def convert_yaml_html(self):
        html_file_name = os.path.join(os.path.dirname(self.yaml_file_name), 'music.html')
        self.dbg('convert_yaml_html', os.path.exists(html_file_name))
        if os.path.exists(html_file_name) and (
            os.path.getmtime(html_file_name) > os.path.getmtime(self.yaml_file_name)
        ):
            return
        self.dbg('convert_yaml_html 23')
        lst = ruamel.yaml.load(open(self.yaml_file_name), Loader=ruamel.yaml.RoundTripLoader)
        print('length of yaml:', len(lst))
        paths = set()
        try:
            try:
                with SimpleHtml(html_file_name, 'New music') as html:
                    for count, x in enumerate(sorted(lst, reverse=True)):
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
            except KeyError:
                print('m', m)
        except:
            os.remove(html_file_name)
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
            if not os.path.exists(self.yaml_file_name):
                self._mapping = CommentedMap()
            else:
                self._mapping = ruamel.yaml.load(
                    open(self.yaml_file_name), Loader=ruamel.yaml.RoundTripLoader
                )
                if self._mapping is None:
                    self._mapping = CommentedMap()
        self._mapping[dd] = data

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
                path = os.path.join(root, d)
                if dir_is_empty(path):
                    os.rmdir(path)
                    dir_names.remove(d)

        def has_music(dir_name, file_names):
            for fn in file_names:
                base_name, ext = os.path.splitext(fn)
                if ext in suffixes:
                    return True
            return False

        def dir_is_empty(d):
            return len(os.listdir(d)) == 0

        def move_images_here(root, dir_names):
            # image extensions should match picards
            image_extensions = ['.jpg', '.gif', '.png', '.pdf']
            for dir_name in dir_names:
                path = os.path.join(root, dir_name)
                for file_name in os.listdir(path):
                    basename, ext = os.path.splitext(file_name)
                    ext_lower = ext.lower()
                    if ext_lower == '.jpeg':
                        ext_lower = '.jpg'
                    if ext_lower not in image_extensions:
                        continue
                    os.rename(
                        os.path.join(path, file_name), os.path.join(root, basename + ext_lower)
                    )

        for root, dir_names, file_names in os.walk(d):
            rm_empty_dirs(root, dir_names)
            if not dir_names:  # no subdirectory that may contain images
                continue
            if not has_music(root, file_names):
                continue
            # we  have subdir(s) and music files, move any images
            move_images_here(root, dir_names)
            print('moving images', root)
            rm_empty_dirs(root, dir_names)
            # for file_name in file_names:
            #     print(root, file_name)
