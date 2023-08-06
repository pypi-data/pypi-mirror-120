# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sklearn_tournament']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sklearn_tournament = sklearn_tournament.cli:main']}

setup_kwargs = {
    'name': 'sklearn-tournament',
    'version': '0.1.0',
    'description': 'Higher level controlls for searching (a collection of) sklearn models for best parameters.',
    'long_description': "==================\nsklearn-tournament\n==================\n\n.. container::\n\n    .. image:: https://img.shields.io/pypi/v/sklearn_tournament.svg\n            :target: https://pypi.python.org/pypi/sklearn_tournament\n            :alt: PyPI Version\n\n    .. image:: https://img.shields.io/pypi/pyversions/sklearn_tournament.svg\n            :target: https://pypi.python.org/pypi/sklearn_tournament/\n            :alt: PyPI Python Versions\n\n    .. image:: https://img.shields.io/pypi/status/sklearn_tournament.svg\n            :target: https://pypi.python.org/pypi/sklearn_tournament/\n            :alt: PyPI Status\n\n    .. badges from below are commendted out\n\n    .. .. image:: https://img.shields.io/pypi/dm/sklearn_tournament.svg\n            :target: https://pypi.python.org/pypi/sklearn_tournament/\n            :alt: PyPI Monthly Donwloads\n\n.. container::\n\n    .. image:: https://img.shields.io/github/workflow/status/sheypex/sklearn-tournament/CI/master\n            :target: https://github.com/sheypex/sklearn-tournament/actions/workflows/ci.yml\n            :alt: CI Build Status\n    .. .. image:: https://github.com/sheypex/sklearn-tournament/actions/workflows/ci.yml/badge.svg?branch=master\n\n    .. image:: https://img.shields.io/github/workflow/status/sheypex/sklearn-tournament/Documentation/master?label=docs\n            :target: https://sheypex.github.io/sklearn-tournament/\n            :alt: Documentation Build Status\n    .. .. image:: https://github.com/sheypex/sklearn-tournament/actions/workflows/documentation.yml/badge.svg?branch=master\n\n    .. image:: https://img.shields.io/codecov/c/github/sheypex/sklearn-tournament.svg\n            :target: https://codecov.io/gh/sheypex/sklearn-tournament\n            :alt: Codecov Coverage\n    .. .. image:: https://codecov.io/gh/sheypex/sklearn-tournament/branch/master/graph/badge.svg\n\n    .. image:: https://img.shields.io/requires/github/sheypex/sklearn-tournament/master.svg\n            :target: https://requires.io/github/sheypex/sklearn-tournament/requirements/?branch=master\n            :alt: Requires.io Requirements Status\n    .. .. image:: https://requires.io/github/sheypex/sklearn-tournament/requirements.svg?branch=master\n\n    .. badges from below are commendted out\n\n    .. .. image:: https://img.shields.io/travis/sheypex/sklearn-tournament.svg\n            :target: https://travis-ci.com/sheypex/sklearn-tournament\n            :alt: Travis CI Build Status\n    .. .. image:: https://travis-ci.com/sheypex/sklearn-tournament.svg?branch=master\n\n    .. .. image:: https://img.shields.io/readthedocs/sklearn-tournament/latest.svg\n            :target: https://sklearn-tournament.readthedocs.io/en/latest/?badge=latest\n            :alt: ReadTheDocs Documentation Build Status\n    .. .. image:: https://readthedocs.org/projects/sklearn-tournament/badge/?version=latest\n\n    .. .. image:: https://pyup.io/repos/github/sheypex/sklearn-tournament/shield.svg\n            :target: https://pyup.io/repos/github/sheypex/sklearn-tournament/\n            :alt: PyUp Updates\n\n.. container::\n\n    .. image:: https://img.shields.io/pypi/l/sklearn_tournament.svg\n            :target: https://github.com/sheypex/sklearn-tournament/blob/master/LICENSE\n            :alt: PyPI License\n\n    .. image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Fsheypex%2Fsklearn-tournament.svg?type=shield\n            :target: https://app.fossa.com/projects/git%2Bgithub.com%2Fsheypex%2Fsklearn-tournament?ref=badge_shield\n            :alt: FOSSA Status\n\n.. container::\n\n    .. image:: https://badges.gitter.im/sheypex/sklearn-tournament.svg\n            :target: https://gitter.im/sklearn-tournament/community\n            :alt: Gitter Chat\n    .. .. image:: https://img.shields.io/gitter/room/sheypex/sklearn-tournament.svg\n\n    .. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n            :target: https://github.com/psf/black\n            :alt: Code Style: Black\n\nHigher level controlls for searching (a collection of) sklearn models for best parameters.\n\n* Free software: `BSD 3-Clause 'New' or 'Revised' License`_\n* Documentation: https://sklearn-tournament.readthedocs.io.\n\n.. _`BSD 3-Clause 'New' or 'Revised' License`: https://github.com/sheypex/sklearn-tournament/blob/master/LICENSE\n\nFeatures\n--------\n\n* TODO\n\nInstall\n-------\n\nUse ``pip`` for install:\n\n.. code-block:: console\n\n    $ pip install sklearn_tournament\n\nIf you want to setup a development environment, use ``poetry`` instead:\n\n.. code-block:: console\n\n    $ # Install poetry using pipx\n    $ python -m pip install pipx\n    $ python -m pipx ensurepath\n    $ pipx install poetry\n\n    $ # Clone repository\n    $ git clone https://github.com/sheypex/sklearn-tournament.git\n    $ cd sklearn-tournament/\n\n    $ # Install dependencies and hooks\n    $ poetry install\n    $ poetry run pre-commit install\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `elbakramer/cookiecutter-poetry`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`elbakramer/cookiecutter-poetry`: https://github.com/elbakramer/cookiecutter-poetry\n",
    'author': 'Sheypex',
    'author_email': 'sheypex@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sheypex/sklearn-tournament',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
