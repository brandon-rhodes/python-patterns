
=======================
 The Singleton Pattern
=======================

*A “Creational Pattern” from the* :doc:`/gang-of-four/index`

.. admonition:: Verdict

   The Singleton Pattern is a stunt.
   It wasn’t even necessary in its original context
   and is a poor fit for the Python language.
   When you must offer global access to a singleton object,
   use :doc:`/python/module-globals/index` instead.

The topic of singletons in Python is a complicated one
because Python had already existed for 5 years
when the :doc:`gang-of-four/singleton` was published,
introducing its own meaning for “Singleton”
on the design patterns community.

We will therefore launch this topic
with a favorite approach of the Wikipedia:
disambiguation.

Disambiguation
==============

Python was already using the term “singleton”
before it became the name of an object oriented design pattern,
using the term to mean:

1. A tuple of length one.
   This definition is introduced in the Python Tutorial
   when the `Data Structures
   <https://docs.python.org/3/tutorial/datastructures.html>`_
   chapter calls its example one-element tuple a ``singleton``,
   and “singleton” is used repeatedly to mean a 1-element tuple
   throughout Python’s documentation.
   When the `Extending and Embedding <https://docs.python.org/3/extending/extending.html#calling-python-functions-from-c>`_
   guide says,
   “To call the Python function … with one argument,
   pass a singleton tuple,”
   it means a tuple containing exactly one item.

2. An object offered through :doc:`/python/module-globals/index`.
   

A flyweight object (... “that is returned by constructor”?)
“CPython's empty tuple is a singleton and cached in” - NO, that’s a flyweight
True False are flyweights
.. “call frozenset() to get the empty frozenset singleton”

Modules are singletons!
what singleton means

The one unique object that is ever returned
from a class that implements the Gang of Four’s Singleton Pattern.
object of which there is only one instance
ellipsis
Doc/library/marshal.rst:46:singletons :const:`None`, :const:`Ellipsis` and :exc:`StopIteration` can also be
None
NotImplemented

Lib/pydoc_data/topics.py

Doc/faq/programming.rst:283:Note that using a module is also the basis for implementing the Singleton design
Doc/c-api/module.rst:258:singletons: if the *sys.modules* entry is removed and the module is re-imported,
Doc/c-api/module.rst:452:Single-phase initialization creates singleton modules that can be looked up

Doc/library/stdtypes.rst:4646:``None`` (a built-in name).  ``type(None)()`` produces the same singleton.
Doc/library/stdtypes.rst:4673:``type(NotImplemented)()`` produces the singleton instance.

Doc/library/enum.rst:1026:The most interesting thing about Enum members is that they are singletons.

When our software’s architecture
has failed to provide a line of code
with a reference to an object it needs,
a common workaround in Python
is :doc:`/python/module-globals/index`:

``None`` not ``NoneType()``

py2

::

>>> type(None)
<type 'NoneType'>
>>> type(None)()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot create 'NoneType' instances
>>> 

py3 without error

.. TODO add to Global Object that the Python FAQ calls it a singleton object
   https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules
