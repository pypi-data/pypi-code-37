import pathlib

from collections import defaultdict

import settings


def find_duplicates():
    paths = settings.get("pic_paths", [])
    extensions = [".jpg"]
    files = defaultdict(list)

    for path in paths:
        for file_ext in extensions:
            for filepath in pathlib.Path(path).glob("**/*" + file_ext):
                files[filepath.name].append(filepath)
    return {k: v for k, v in files.items() if len(v) > 1}


if __name__ == "__main__":
    find_duplicates()
