
================
 Module Globals
================

*A “Creational Pattern” inspired by Modula-2 and Modula-3*

.. admonition:: Verdict

   Both the core Python language and many third party packages
   offer access to convenient pre-built objects
   by assigning them a name in a module’s global namespace.
   Like the builtin module’s ``None``, ``True``, and ``False``,
   global objects are easy to understand, easy to use,
   and never conflict with names in other packages
   because every Python module is its own namespace.
   Module globals are more common in Python
   than the Gang of Four’s :doc:`gang-of-four/singleton`,
   which was a trick to avoid creating any more global names than necessary
   in languages without the benefit of a module system.

.. contents:: Contents:
   :backlinks: none

.. $ a --ignore site-packages '^[a-z_]+ = [a-z_]+\.[a-z_]+$' /usr/lib/python3.6

.. random
.. calendar
.. distutils.log?
.. NOT threading _start_new_thread = _thread.start_new_thread
   that instead is to pull things out of C
.. and NOT cases where it’s a classmethod like open = TarFile.open
.. semaphore tracker? forkserver?
.. copy constant is another thing.

.. TODO mention how for verbs, not nouns, we put methods in the global
   namespace; exmaples are random and json modules

functions: random; dumps loads pickle? definitely json. requests?

constants (strings.* etc) vs live objects

True False

don’t do I/O at top level to create object
if you really need to have a separate init or setup routine for it

