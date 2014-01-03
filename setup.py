#!/usr/bin/env python
import os

from distutils.core import setup

SCRIPT_DIR = os.path.dirname(__file__)
if not SCRIPT_DIR:
        SCRIPT_DIR = os.getcwd()


# put together list of requirements to install
install_requires = []
with open(os.path.join(SCRIPT_DIR, 'requirements.txt')) as fh:
        for line in fh.readlines():
                    install_requires.append(line.strip())

setup(name='docker-buildcache',
      version='0.0.1',
      description='Cache ADD steps in a Dockerfile',
      author='Roberto Aguilar',
      author_email='roberto@baremetal.io',
      scripts=['scripts/docker-buildcache'],
      long_description=open('README.md').read(),
      url='http://github.com/baremetal/docker-buildcache',
      license='LICENSE.txt',
      install_requires=install_requires,
)
