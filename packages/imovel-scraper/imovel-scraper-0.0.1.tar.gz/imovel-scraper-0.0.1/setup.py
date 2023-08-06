# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imovel_scraper']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['imovel-scraper = imovel_scraper.__main__:main']}

setup_kwargs = {
    'name': 'imovel-scraper',
    'version': '0.0.1',
    'description': 'Imovel Scraper',
    'long_description': "Imovel Scraper\n==============\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/imovel-scraper.svg\n   :target: https://pypi.org/project/imovel-scraper/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/imovel-scraper.svg\n   :target: https://pypi.org/project/imovel-scraper/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/imovel-scraper\n   :target: https://pypi.org/project/imovel-scraper\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/imovel-scraper\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/imovel-scraper/latest.svg?label=Read%20the%20Docs\n   :target: https://imovel-scraper.readthedocs.io/\n   :alt: Read the documentation at https://imovel-scraper.readthedocs.io/\n.. |Tests| image:: https://github.com/acha-imovel/imovel-scraper/workflows/Tests/badge.svg\n   :target: https://github.com/acha-imovel/imovel-scraper/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/acha-imovel/imovel-scraper/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/acha-imovel/imovel-scraper\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Imovel Scraper* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install imovel-scraper\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Imovel Scraper* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/acha-imovel/imovel-scraper/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://imovel-scraper.readthedocs.io/en/latest/usage.html\n",
    'author': 'Victor Mattos',
    'author_email': '5757883+vicmattos@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/acha-imovel/imovel-scraper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
