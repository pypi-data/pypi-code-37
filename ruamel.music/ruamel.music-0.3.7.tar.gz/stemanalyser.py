# coding: utf-8

from __future__ import print_function

import io

# from musicbrainz2.webservice import Query, ArtistFilter, TrackFilter, \
#     WebServiceError
import musicbrainzngs


class StemAnalyser(object):
    def __init__(self, log=None):
        self._log_path = log
        self._musicbrainz = False

    def setup_musicbrainz(self):
        if not self._musicbrainz:
            musicbrainzngs.set_useragent('music_test', '0.1.5', 'a.van.der.neut@ruamel.eu')
            self._musicbrainz = True

    def __call__(self, stem):
        """try to guess at least the artist and track-title from path

        http://bugs.musicbrainz.org/browser/python-musicbrainz2/trunk/examples
        """
        self.log("StemAnalyser '{}'".format(stem))
        ret_val = {}
        # see if there is final comment like stuff in ()
        if stem[-1] == ')':
            stem, comment = stem[:-1].rsplit('(', 1)
            ret_val['comment'] = comment.strip()
        # track number?
        if stem[0].isdigit():
            try:
                track, rest = stem[0], stem[1:]
                while rest and rest[0].isdigit():
                    track += rest[0]
                    rest = rest[1:]
                if rest.isalpha():  # characters following number
                    raise NotImplementedError
                rest = rest.lstrip()
                if rest[0] in ['.-']:
                    rest = rest[1:].lstrip()
                # print(track, rest)
                stem = rest
                ret_val['track'] = int(track)
            except:
                del track
        if '-' in stem and ' - ' not in stem:
            parts = [p.strip() for p in stem.split('-')]
        else:
            parts = [p.strip() for p in stem.split(' - ')]
        parts = [p for p in parts if p]
        del_part = None
        self.setup_musicbrainz()
        # q = Query()
        artist_id = None
        while parts:  # until no parts left
            # print('parts', parts, del_part)
            if del_part is not None:
                try:
                    parts.pop(del_part)
                except IndexError:
                    print('error pop parts', parts, del_part)
                    raise
                del_part = None
            lyrics = 'lyrics'
            for idx, part in enumerate(parts):
                if part.lower().endswith(lyrics):
                    ret_val['title'] = part[: -len(lyrics)].rstrip()
                    del_part = idx
                    break
                if part[0].isdigit():
                    try:
                        track, rest = part[0], part[1:]
                        while rest and rest[0].isdigit():
                            track += rest[0]
                            rest = rest[1:]
                        if rest.isalpha():  # characters following number
                            raise NotImplementedError
                        rest = rest.lstrip()
                        if rest[0] in ['.-']:
                            rest = rest[1:].lstrip()
                        # print(track, rest)
                        stem = rest
                        ret_val['track'] = int(track)
                        del_part = idx
                        break
                    except:
                        del track
            if del_part is not None:
                continue
            if 'artist' not in ret_val:
                # if len(parts) == 1:
                #     ret_val['artist'] = parts.pop(0)
                for idx, part in enumerate(parts):
                    # try:
                    #     f = ArtistFilter(name=part, limit=1)
                    #     artist_results = q.getArtists(f)
                    # except WebServiceError, e:
                    #     continue
                    # result = artist_results[0]
                    result = musicbrainzngs.search_artists(artist=part, limit=1)
                    if ',' in part:
                        l, f = part.split(',', 1)
                        check_part = f.strip().lower() + ' ' + l.strip().lower()
                    else:
                        check_part = part.lower()
                    # for k, v in result.iteritems():
                    #     print(k, v)
                    artists = result['artist-list']
                    if not artists:
                        break
                    artist = artists[0]
                    # print("[{}] [{}]".format(artist['name'].lower(), check_part))
                    if artist['name'].lower().replace(' ', '') == check_part.replace(' ', ''):
                        # found exact match
                        ret_val['artist'] = artist['name']
                        ret_val['artistsort'] = artist['sort-name']
                        artist_id = artist['name']  # artist['id']
                        del_part = idx
                        break
                if del_part is not None:
                    continue
            if artist_id and 'title' not in ret_val:
                for idx, part in enumerate(parts):
                    # try:
                    #     f = TrackFilter(title=part,
                    #                     artistName=ret_val['artist'])
                    #     track_results = q.getTracks(f)
                    # except WebServiceError, e:
                    #     continue
                    release_results = musicbrainzngs.search_releases(
                        part, artistname=artist_id, limit=1
                    )
                    if not release_results['release-list']:
                        continue
                    # for k, v in release_results.iteritems():
                    #     print(k, v)
                    result = release_results['release-list'][0]
                    ret_val['title'] = result['title']
                    del_part = idx
                    break
                if del_part is not None:
                    continue
            break
        self.log("StemAnalyser '{}':\n   {!r}".format(stem, ret_val))
        return ret_val

    def log(self, *args, **kw):
        if self.log_path is None:
            return
        path = self.log_path
        if not isinstance(object, basestring):
            path = str(path)
        with io.open(path, 'a') as fp:
            kw1 = kw.copy()
            kw1['file'] = fp
            args = [unicode(x, 'utf-8', 'replace') for x in args]
            print(*args, **kw1)
            fp.flush()

    @property
    def log_path(self):
        return self._log_path

    @log_path.setter
    def log_path(self, log):
        # if isinstance(log, basestring):
        #     log = Path(log)
        self._log_path = log
