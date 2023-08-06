tfm_utils
===========

..
    image:: https://travis-ci.org/j-andrews7/pytfmpval.png?branch=master
    :target: https://travis-ci.org/j-andrews7/pytfmpval

..
    image:: https://badge.fury.io/py/pytfmpval.svg?style=flat
    :target: http://badge.fury.io/py/pytfmpval

..
    image:: https://readthedocs.org/projects/pytfmpval/badge/?version=latest
    :target: http://pytfmpval.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


This package is meant to be an improvement on the `pytfmpval <https://github.com/j-andrews7/pytfmpval>`_ by `Jared Andrews <https://github.com/j-andrews7>`_ which is itself
a wrapper for the incredibly useful `TFM-Pvalue C++ program <http://bioinfo.lifl.fr/tfm-pvalue/tfm-pvalue.php>`_.
It allows users to determine score thresholds for a given transcription factor position frequency matrix
associated with a specific p-value. Naturally, it can also perform the reverse, quickly calculating an accurate
p-value from a score for a given motif matrix.

The `pytfmpval <https://github.com/j-andrews7/pytfmpval>`_ is archived and has several super annoying uncaught
excpetions that cause the whole program to crash every time there is any error so to start this package will focus
on:
    1. making this package more robust at runtime
    2. modernizing the interface a bit
        2.1. This primarily includes adding support for pandas and numpy arrays as opposed to purely white space delimited lists and the like

This should make everyhting better to use and make it feel like you are writing python code
instead or old school R or something.

``tfm_utils`` allows this functionality to be easily utilized within a Python script, module, or package.

See full documentation and use examples `here <https://mcclain-thiel.github.io/tfm-utils/>`_.

Installation
---------------

tfm_utils is on PyPI, so you can install via ``pip`` easily::

    pip install tfm_utils


or locally with::

    git clone repo_name_here
    cd tfm_utils
    CC=clang CXX=clang++ python -m pip install e .


You need to use the weird install function to get the C++ code to work


Acknowledgments
---------------

`Jared Andrews <https://github.com/j-andrews7>`_ did most of the hard work on this project
I just wanted to fix a few things that were bugging me and his version was archived. It seems
like a pretty open license so I assume this is all chill.

Contribute
---------------

Any and all contributions are welcome. Bug reporting via the `Issue Tracker <https://github.com/McClain-Thiel/tfm-utils/issues>`_ is much appreciated. Here's how to contribute:

1. Fork the `pytfmpval repository <https://github.com/McClain-Thiel/tfm-utils>`_ on github (see `forking help <https://help.github.com/articles/fork-a-repo/>`_).

2. Make your changes/fixes/improvements locally.

3. Optional, but much-appreciated: write some tests for your changes. (Don't worry about integrating your tests into the test framework - writing some in your commit comments or providing a test script is fine. I will integrate them later.)

4. Send a pull request (see `pull request help <https://help.github.com/articles/about-pull-requests/>`_).


Reference
--------------

| Efficient and accurate P-value computation for Position Weight Matrices
| H. Touzet and J.S. Varré
| *Algorithms for Molecular Biology 2007, 2:15*

License
-----------

This project is licensed under the GPL3 license. You are free to use, modify, and distribute it as you see fit. The program is provided as is, with no guarantees.
