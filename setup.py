#!/usr/bin/env python
#
# Copyright 2013 Trey Morris
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='gister',
    author='Trey Morris',
    author_email='trey@treymorris.com',
    description='gist making script',
    long_description=read('README.md'),
    install_requires=['argparse', 'keyring', 'requests'],
    packages=find_packages(),
    url='https://github.com/tr3buchet/gister',
    entry_points={
        'console_scripts': [
            'gister = gister.gister:create_gist']})
