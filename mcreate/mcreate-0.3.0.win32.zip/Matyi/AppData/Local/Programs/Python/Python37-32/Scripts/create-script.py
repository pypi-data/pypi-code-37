#!C:\Users\Matyi\AppData\Local\Programs\Python\Python37-32\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'mcreate==0.3.0','console_scripts','create'
__requires__ = 'mcreate==0.3.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('mcreate==0.3.0', 'console_scripts', 'create')()
    )
