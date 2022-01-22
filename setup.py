from os import path
from typing import Dict
from functools import partial

from setuptools import setup
from setuptools import find_packages


version_info  = dict()
package_join_ = partial(path.join, path.abspath(path.dirname(__file__)), 'package_diff')
with open(package_join_('__version__.py')) as f:
    exec(f.read(), version_info)


setup(
    name="package-diff",
    version=version_info['__version__'],
    packages=find_packages(),
    install_requires=[
        'click>=8.0.3',
        'rich>=10.16.2',
    ],
    entry_points={
        'console_scripts': [
            'package-diff=package_diff:cli'
        ]
    }
)
