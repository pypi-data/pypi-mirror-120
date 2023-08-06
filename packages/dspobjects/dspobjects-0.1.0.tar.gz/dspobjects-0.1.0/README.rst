========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-dspobjects/badge/?style=flat
    :target: https://python-dspobjects.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/fonganthonym/python-dspobjects.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/fonganthonym/python-dspobjects

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/fonganthonym/python-dspobjects?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/fonganthonym/python-dspobjects

.. |requires| image:: https://requires.io/github/fonganthonym/python-dspobjects/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/fonganthonym/python-dspobjects/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/fonganthonym/python-dspobjects/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fonganthonym/python-dspobjects

.. |version| image:: https://img.shields.io/pypi/v/dspobjects.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/dspobjects

.. |wheel| image:: https://img.shields.io/pypi/wheel/dspobjects.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/dspobjects

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/dspobjects.svg
    :alt: Supported versions
    :target: https://pypi.org/project/dspobjects

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/dspobjects.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/dspobjects

.. |commits-since| image:: https://img.shields.io/github/commits-since/fonganthonym/python-dspobjects/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/fonganthonym/python-dspobjects/compare/v0.1.0...master



.. end-badges

Extra objects for handling and typing HDF5 files.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install dspobjects

You can also install the in-development version with::

    pip install https://github.com/fonganthonym/python-dspobjects/archive/master.zip


Documentation
=============


https://python-dspobjects.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
