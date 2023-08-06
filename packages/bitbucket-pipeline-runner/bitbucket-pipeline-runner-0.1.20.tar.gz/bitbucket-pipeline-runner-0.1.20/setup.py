# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeline_runner']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'boto3>=1.16.63,<2.0.0',
 'click>=6.7,<8.0',
 'coloredlogs>=15.0,<16.0',
 'cryptography>=3.4.8,<4.0.0',
 'docker>=4.4.1,<5.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyfzf>=0.2.2,<0.3.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-slugify>=4.0.1,<5.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['pipeline-runner = pipeline_runner.cli:main']}

setup_kwargs = {
    'name': 'bitbucket-pipeline-runner',
    'version': '0.1.20',
    'description': 'Run a bitbucket pipeline locally',
    'long_description': None,
    'author': 'Mathieu Lemay',
    'author_email': 'acidrain1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
