====================================
 rope, a python refactoring IDE ...
====================================


Overview
========

`Ropeide`_ is a python refactoring IDE.  It uses rope_ library to
provide features like refactoring, code assist, and auto-completion.
It is written in python.  The IDE uses `Tkinter` library.

You should install `rope`_ library before using this IDE.

.. _`ropeide`: http://rope.sf.net/
.. _`rope`: http://rope.sf.net/


New Features
============

* added usefunction refactoring
* indent/deindent lines
* not using a deprecated templates in codeassist
* better help files finding
* indenter module was improved


Getting Started
===============

* List of features: `docs/ropeide.txt`_
* Tutorial: `docs/tutorial.txt`_

To change rope IDE preferences like font edit your ``~/.ropeide``
(which is created the first time you start rope).  To change your
project preferences edit ``$PROJECT_ROOT/.ropeproject/config.py``
where ``$PROJECT_ROOT`` is the root folder of your project (this file
is created the first time you open a project).

If you don't like rope's default emacs-like keybinding, edit the
default ``~/.ropeide`` file and change `i_like_emacs` variable to
`False`.


Bug Reports
===========

Send your bug reports and feature requests to `rope-dev (at)
googlegroups.com`_.

.. _`rope-dev (at) googlegroups.com`: http://groups.google.com/group/rope-dev


License
=======

This program is under the terms of GPL (GNU General Public License).
Have a look at ``COPYING`` file for more information.


.. _`docs/tutorial.txt`: docs/tutorial.html
.. _`docs/ropeide.txt`: docs/ropeide.html
