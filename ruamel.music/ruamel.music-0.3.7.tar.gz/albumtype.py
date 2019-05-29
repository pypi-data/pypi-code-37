
from ruamel.std.pathlib import Path
import os

image_extensions = ['.jpg', '.gif', '.png', '.pdf', '.jepg', '.bmp']


class AlbumType(object):
    def __init__(self):
        self._dir = None
        self._subdirs = []

    def set_dir(self, d):
        self._dir = d

    def set_subdir(self, d):
        self._subdirs.append(d)

    def check_images(self, move=False):
        assert self._dir is not None
        dirs = []
        for root, directory_names, file_names in os.walk(str(self._dir)):
            rp = Path(root)
            for ext in image_extensions:
                for file_name in file_names:
                    file_name_l = file_name.lower()
                    if file_name_l.endswith(ext):
                        sd = self._subdirs[0] if self._subdirs else None
                        # print(str(self._dir), root[len(str(self._dir))+1:], file_name, sd)
                        if move:
                            fp = rp / file_name
                            td = self._dir / sd if sd else self._dir
                            if rp == td:
                                continue
                            # print('fp', fp, 'td', td)
                            print('sd', sd)
                            fp.rename(td / fp.name)

    def check_non_relevant_files(self, remove=False):
        for root, directory_names, file_names in os.walk(str(self._dir)):
            rp = Path(root)
            for file_name in file_names:
                fp = rp / file_name
                fnl = file_name.lower()
                if fnl.startswith('audiocheck') or fnl == 'thumbs.db':
                    fp.remove()
                    continue
        
    def check_empty_dirs(self, remove=False):
        for root, directory_names, file_names in os.walk(str(self._dir)):
            rp = Path(root)
            for dir_name in directory_names:
                fdn = rp / dir_name
                if len(os.listdir(str(fdn))) == 0:
                    directory_names.remove(dir_name)
                    fdn.rmdir()
