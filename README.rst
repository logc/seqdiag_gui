======================
seqdiag_gui user guide
======================

seqdiag_gui is a graphic user interface to Takeshi Komiya's simple sequence
diagram package, called seqdiag_

.. _seqdiag: https://bitbucket.org/tk0miya/seqdiag

Install
=======

This package needs the following dependencies installed on your system:

  - python >= 2.7.2
  - wxPython >= 2.9.3.1

If you are on OS X, you can install these packages via Macports::

  $ sudo port install python27 @2.7.2_4+universal
  $ sudo port install py27-wxpython-devel @2.9.3.1_0

This project has been tested on a system running OS X 10.8.2

Setup
=====

In order to run this project, you need to build it using the following
commands::

  $ python bootstrap.py
  $ bin/buildout

After the build is successfully completed, you may start the graphical user
interface with the following command::

  $ bin/run

Create a diagram
================

TODO

Un-install
==========

TODO

LICENSE
=======

TBD
