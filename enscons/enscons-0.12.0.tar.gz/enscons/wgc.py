#!/usr/bin/env python
# wgc "wheel greater compression"
# puts everything but *.dist-info/ in an interior archive

import pathlib
import os.path
import sys
import hashlib
import zipfile

from enscons import urlsafe_b64encode

compression=zipfile.ZIP_LZMA
compresslevel=None  # default

# top 512 wheels:
# original: 728M
# with default compresslevel: 678M
# with -9 compresslevel: 674M

# (savings in bytes) * (downloadcount) for last 30 days...

def add_manifest(wheel, dist_info):
    """
    Add the wheel manifest.
    """
    import hashlib
    import zipfile

    archive = zipfile.ZipFile(wheel, "a", compression=compression)
    lines = []
    for f in archive.namelist():
        data = archive.read(f)
        size = len(data)
        digest = hashlib.sha256(data).digest()
        digest = "sha256=" + (urlsafe_b64encode(digest).decode("ascii"))
        lines.append("%s,%s,%s" % (f.replace(",", ",,"), digest, size))

    record_path = dist_info + "/RECORD"
    lines.append(record_path + ",,")
    RECORD = "\n".join(lines)
    archive.writestr(record_path, RECORD, compresslevel=compresslevel)
    archive.close()

def greater(wheel):
    original = pathlib.Path(wheel)
    extra_crispy = original.with_suffix('.wgc')
    prefix = '-'.join(str(original.name).split('-', 2)[:2])
    dist_info = prefix + '.dist-info'
    data_zip = prefix + '.data.zip'

    for path in (extra_crispy, data_zip):
        p = pathlib.Path(path)
        if p.exists():
            p.unlink()

    with zipfile.ZipFile(original, 'r') as wheel_in:
        with zipfile.ZipFile(extra_crispy, 'w', compression=compression) as wheel_out:
            with zipfile.ZipFile(data_zip, 'w', compression=zipfile.ZIP_STORED) as interior:
                for info in wheel_in.filelist:
                    if not info.filename.startswith(dist_info):
                        interior.writestr(info.filename, wheel_in.read(info), compresslevel=compresslevel)
                    elif not info.filename.endswith('/RECORD'):
                        wheel_out.writestr(info.filename, wheel_in.read(info), compresslevel=compresslevel)
            wheel_out.write(data_zip, compresslevel=compresslevel)

    add_manifest(extra_crispy, dist_info)

    pathlib.Path(data_zip).unlink()

    return extra_crispy

for filename in sys.argv[1:]:
    try:
        output = greater(filename)
        sz_before = pathlib.Path(filename).stat().st_size
        sz_after = pathlib.Path(output).stat().st_size
        print("%s %0.0f%% %d" % (output, (sz_after / sz_before) * 100,  sz_after-sz_before))
    except Exception as e:
        print(e)
        print("%s fail" % filename)
