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

Let us start from a clear screen by removing all text in the edition box:

.. image:: http://logc.github.com/seqdiag_gui/images/screen-01.png
  :alt: Step 01: cleared up

We can add a message between two entities by writing their names, an arrow that
goes from one to the other, and a semicolon at the end of the described
message. If the entities were not mentioned yet in the diagram, they are
created new. Here we create two of them, 'user'  and 'interface'. We then press
the 'Evaluate' button to show the following diagram:

.. image:: http://logc.github.com/seqdiag_gui/images/screen-02.png
   :alt: Step 02: first message

A return value is signaled in the diagram by an arrow flowing back from one
entity to another. This is written in the edition box simply inverting the
arrow in a line following the first one:

.. image:: http://logc.github.com/seqdiag_gui/images/screen-03.png
   :alt: Step 03: return value

If the second entity needed to call other entities to compute the return value,
these messages must be listed between the original call and the return value
call. Here we create a third entity ('handler') and send it a message. We
obtain a return value in the same line by writing a double arrow in the edition
box.

.. image:: http://logc.github.com/seqdiag_gui/images/screen-04.png
   :alt: Step 04: nested calls

When you finish describing the flow of messages that make up your sequence, you
can save the resulting diagram in a PNG file by pressing the 'Save' button.

There are many more features in the seqdiag package. You can read up on them in
[its documentation](http://blockdiag.com/en/seqdiag/index.html) and end up
producing something like this!

.. image:: http://logc.github.com/seqdiag_gui/images/screen-05.png
   :alt: Step 05: complex diagram


Un-install
==========

TODO

LICENSE
=======

TBD
