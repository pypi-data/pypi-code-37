from distutils.core import setup

version = '1.0.7'

requirements = [
    'reportportal-client>=3.1.0',
    'pytest>=3.0.7',
    'six>=1.10.0',
    'dill>=0.2.7.1',
]

setup(
  name = 'pytest-reportportal',
  packages= ['pytest_reportportal'],
  version = version,
  description= 'Agent for Reporting results of tests to the Report Portal',
  author = 'Pavel Papou',
  author_email= 'SupportEPMC-TSTReportPortal@epam.com',
  url= 'https://github.com/reportportal/agent-python-pytest',
  keywords= ['testing', 'reporting', 'reportportal', 'pytest'],
  classifiers= [
        'Framework :: Pytest',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    entry_points={
        'pytest11': [
            'pytest_reportportal = pytest_reportportal.plugin',
        ]
    },
)