########
 setux
########

**Setup Tux**

Install, Deploy, Admin

========
Abstract
========

This is a meta package including all the packages needed for setux to be functionnal.

`core <https://pypi.org/project/setux_core>`_
Abstract base classes for all other packages.

`distros <https://pypi.org/project/setux_distros>`_
core.distro.Distro implementations
Supported OSs
(Debian, FreeBSD)

`targets <https://pypi.org/project/setux_targets>`_
core.target.Target implementations
Connection to the target machine
(Local, SSH)

`managers <https://pypi.org/project/setux_managers>`_
core.manage.Manager implementations
Resources managers
(Pakages, Services)

`mappings <https://pypi.org/project/setux_mappings>`_
core.mapping.Mapping implementations
Mapping resources names
(Pakages, Service)

`modules <https://pypi.org/project/setux_modules>`_
core.module.Module implementations
User defined functionality

`logger <https://pypi.org/project/setux_logger>`_
Logging


Additional packages:

`REPL <https://pypi.org/project/setux-repl>`_
Rudimentary Setux REPL / CLI
Note that setux is mainly intended to be used as a Python framework.

`PLUS <https://pypi.org/project/setux-plus>`_
Augmented Setux distribution
Additional implementations of core's abstract classes.


=====
Usage
=====

REPL:
.. code-block:: shell

    setux

Python:
.. code-block:: python

   import setux

============
Installation
============

.. code-block:: shell 

    $ pip install setux
