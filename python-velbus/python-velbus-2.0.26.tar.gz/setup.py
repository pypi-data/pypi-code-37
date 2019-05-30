from setuptools import setup

setup(name='python-velbus',
      version='2.0.26',
      url='https://github.com/thomasdelaet/python-velbus',
      license='MIT',
      author='Thomas Delaet',
      install_requires=["pyserial==3.3"],
      author_email='thomas@delaet.org',
      description="Python Library for the Velbus protocol",
      packages=['velbus', 'velbus.connections', 'velbus.messages', 'velbus.modules'],
      platforms='any',
)
