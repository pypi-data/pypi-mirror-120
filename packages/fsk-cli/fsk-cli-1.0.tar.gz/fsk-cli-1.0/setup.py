from setuptools import setup

setup(
  name='fsk-cli',
  version=1.0,
  packages=['fsk'],
  install_requires=['pytest'],
  entry_points={'console_scripts': ['fsk = fsk.cli.scripts.main:cli']}
)