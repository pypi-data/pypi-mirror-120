==================
sklearn-tournament
==================

.. container::

    .. image:: https://img.shields.io/pypi/v/sklearn_tournament.svg
            :target: https://pypi.python.org/pypi/sklearn_tournament
            :alt: PyPI Version

    .. image:: https://img.shields.io/pypi/pyversions/sklearn_tournament.svg
            :target: https://pypi.python.org/pypi/sklearn_tournament/
            :alt: PyPI Python Versions

    .. image:: https://img.shields.io/pypi/status/sklearn_tournament.svg
            :target: https://pypi.python.org/pypi/sklearn_tournament/
            :alt: PyPI Status

    .. badges from below are commendted out

    .. .. image:: https://img.shields.io/pypi/dm/sklearn_tournament.svg
            :target: https://pypi.python.org/pypi/sklearn_tournament/
            :alt: PyPI Monthly Donwloads

.. container::

    .. image:: https://img.shields.io/github/workflow/status/sheypex/sklearn-tournament/CI/master
            :target: https://github.com/sheypex/sklearn-tournament/actions/workflows/ci.yml
            :alt: CI Build Status
    .. .. image:: https://github.com/sheypex/sklearn-tournament/actions/workflows/ci.yml/badge.svg?branch=master

    .. image:: https://img.shields.io/github/workflow/status/sheypex/sklearn-tournament/Documentation/master?label=docs
            :target: https://sheypex.github.io/sklearn-tournament/
            :alt: Documentation Build Status
    .. .. image:: https://github.com/sheypex/sklearn-tournament/actions/workflows/documentation.yml/badge.svg?branch=master

    .. image:: https://img.shields.io/codecov/c/github/sheypex/sklearn-tournament.svg
            :target: https://codecov.io/gh/sheypex/sklearn-tournament
            :alt: Codecov Coverage
    .. .. image:: https://codecov.io/gh/sheypex/sklearn-tournament/branch/master/graph/badge.svg

    .. image:: https://img.shields.io/requires/github/sheypex/sklearn-tournament/master.svg
            :target: https://requires.io/github/sheypex/sklearn-tournament/requirements/?branch=master
            :alt: Requires.io Requirements Status
    .. .. image:: https://requires.io/github/sheypex/sklearn-tournament/requirements.svg?branch=master

    .. badges from below are commendted out

    .. .. image:: https://img.shields.io/travis/sheypex/sklearn-tournament.svg
            :target: https://travis-ci.com/sheypex/sklearn-tournament
            :alt: Travis CI Build Status
    .. .. image:: https://travis-ci.com/sheypex/sklearn-tournament.svg?branch=master

    .. .. image:: https://img.shields.io/readthedocs/sklearn-tournament/latest.svg
            :target: https://sklearn-tournament.readthedocs.io/en/latest/?badge=latest
            :alt: ReadTheDocs Documentation Build Status
    .. .. image:: https://readthedocs.org/projects/sklearn-tournament/badge/?version=latest

    .. .. image:: https://pyup.io/repos/github/sheypex/sklearn-tournament/shield.svg
            :target: https://pyup.io/repos/github/sheypex/sklearn-tournament/
            :alt: PyUp Updates

.. container::

    .. image:: https://img.shields.io/pypi/l/sklearn_tournament.svg
            :target: https://github.com/sheypex/sklearn-tournament/blob/master/LICENSE
            :alt: PyPI License

    .. image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Fsheypex%2Fsklearn-tournament.svg?type=shield
            :target: https://app.fossa.com/projects/git%2Bgithub.com%2Fsheypex%2Fsklearn-tournament?ref=badge_shield
            :alt: FOSSA Status

.. container::

    .. image:: https://badges.gitter.im/sheypex/sklearn-tournament.svg
            :target: https://gitter.im/sklearn-tournament/community
            :alt: Gitter Chat
    .. .. image:: https://img.shields.io/gitter/room/sheypex/sklearn-tournament.svg

    .. image:: https://img.shields.io/badge/code%20style-black-000000.svg
            :target: https://github.com/psf/black
            :alt: Code Style: Black

Higher level controlls for searching (a collection of) sklearn models for best parameters.

* Free software: `BSD 3-Clause 'New' or 'Revised' License`_
* Documentation: https://sklearn-tournament.readthedocs.io.

.. _`BSD 3-Clause 'New' or 'Revised' License`: https://github.com/sheypex/sklearn-tournament/blob/master/LICENSE

Features
--------

* TODO

Install
-------

Use ``pip`` for install:

.. code-block:: console

    $ pip install sklearn_tournament

If you want to setup a development environment, use ``poetry`` instead:

.. code-block:: console

    $ # Install poetry using pipx
    $ python -m pip install pipx
    $ python -m pipx ensurepath
    $ pipx install poetry

    $ # Clone repository
    $ git clone https://github.com/sheypex/sklearn-tournament.git
    $ cd sklearn-tournament/

    $ # Install dependencies and hooks
    $ poetry install
    $ poetry run pre-commit install

Credits
-------

This package was created with Cookiecutter_ and the `elbakramer/cookiecutter-poetry`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`elbakramer/cookiecutter-poetry`: https://github.com/elbakramer/cookiecutter-poetry
