# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['iscc_cli']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2,<2.0',
 'click>=7.0,<8.0',
 'iscc>=1.0,<2.0',
 'tika>=1.19,<2.0']

entry_points = \
{'console_scripts': ['iscc = iscc_cli.cli:cli']}

setup_kwargs = {
    'name': 'iscc-cli',
    'version': '0.2.0',
    'description': 'ISCC CLI - Creates ISCC Codes from Media Files',
    'long_description': '# iscc-cli  - Command Line Tool\n\n[![Linux Build Status](https://img.shields.io/travis/iscc/iscc-cli.svg?label=Linux)](https://travis-ci.org/iscc/iscc-cli)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/titusz/iscc-cli.svg?label=Windows)](https://ci.appveyor.com/project/titusz/iscc-cli)\n[![Version](https://img.shields.io/pypi/v/iscc-cli.svg)](https://pypi.python.org/pypi/iscc-cli/)\n\n> A command line tool that creates **ISCC Codes** for digital media files based on the [reference implementation](<https://github.com/iscc/iscc-specs>).\n\n## Table of Contents\n\n- [Background](#background)\n- [Install](#install)\n- [Usage](#usage)\n- [Maintainers](#maintainers)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Background\n\nThe **International Standard Content Code** is a proposal for an [open standard](https://en.wikipedia.org/wiki/Open_standard) for decentralized content identification. **ISCC Codes** are generated algorithmically **from the content itself** and offer many powerful features like content similarity clustering and partial integrity checks. If you want to learn more about the **ISCC** please check out https://iscc.codes.\n\n## Requirements\n\n| NOTE: Requires JAVA to be installed and on your path! |\n| --- |\n\n**iscc-cli** is tested on Linux and Windows with Python 3.5/3.6/3.7.\n\nThis tool depends on [tika-python](<https://github.com/chrismattmann/tika-python>).  [Tika](<https://tika.apache.org/>)  is used for extracting metadata and content from media files before generating ISCC Codes. On first execution of the `iscc` command line tool it will automatically download and launch the Java Tika Server in the background (this may take some time). Consecutive runs will access the existing Tika instance. You may explicitly pre-launch the Tika server with `$ iscc init`\n\n## Install\n\nThe ISCC command line tool is published with the package name `iscc-cli` on the [Python Package Index](https://pypi.python.org/pypi/iscc-cli) and can be installed with pip:\n\n```console\n$ pip3 install iscc-cli\n```\n\n## Usage\n\nShow help by calling `iscc` without any arguments:\n\n```console\n$ iscc\nUsage: iscc [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  gen*   Generate ISCC Code for a single media file.\n  batch  Generate ISCC Codes for multiple files.\n  init   Inititalize and check Tika server.\n```\n\nThe `gen` command generates an ISCC Code for a single file:\n\n```console\n$ iscc gen tests/demo.jpg\nISCC:CCTcjug7rM3Da-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv\n```\n\nThe `gen` command is default so you can skip it and simply do `$ iscc tests/demo.jpg` \n\nTo get a more detailed result use the `-v` (`--verbose`) option:\n\n```console\n$ iscc -v tests/demo.jpg\nISCC:CCTcjug7rM3Da-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv\nNorm Title: concentrated cat\nTophash:    7a8d0c513142c45f417e761355bf71f11ad61d783cd8958ffc0712d00224a4d0\nFilepath:   tests/demo.jpg\nGMT:        image\n```\n\nGet help for a specific command:\n\n```console\n$ iscc batch --help\nUsage: iscc batch [OPTIONS] PATH\n\n  Batch create ISCC Codes.\n\n  Generates ISCC Codes for all media files in <PATH>.\n\nOptions:\n  -r, --recursive  Recurse into subdirectories.\n  --help           Show this message and exit.\n\n```\n\n## Maintainers\n\n[@titusz](https://github.com/titusz)\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\nYou may also want join our developer chat on Telegram at <https://t.me/iscc_dev>.\n\n## Change Log\n\n### [0.2.0] - 2019-05-31\n\n- Add support for doc, docx and rtf documents\n- Update to ISCC 1.0.4 (fixes whitespace bug)\n\n\n### [0.1.0] - 2019-05-31\n\n- Basic ISCC Code creation\n- Supported file types: jpg, png, pdf, epub\n\n## License\n\nMIT Â© 2019 Titusz Pan\n\n',
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'url': 'https://iscc.codes/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
