
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
before the Singleton Pattern was defined by
the object oriented design pattern community,
so we should first enumerate its other definitions.

1. A “singleton” is a ``tuple`` of length one.
   While this definition might surprise programmers,
   it reflects the original definition of a “singleton” in mathematics —
   a set containing only one element.
   The Python Tutorial itself introduces newcomers to this definition
   when its chapter on `Data Structures
   <https://docs.python.org/3/tutorial/datastructures.html>`_
   calls an example one-element tuple a “singleton”,
   and through the rest of Python’s documentation
   “singleton” continues to be used to mean a 1-element tuple.
   When the `Extending and Embedding <https://docs.python.org/3/extending/extending.html#calling-python-functions-from-c>`_
   guide says,
   “To call the Python function … with one argument,
   pass a singleton tuple,”
   it means a tuple containing exactly one item.

2. Modules are “singletons”
   because no matter how many times you ``import`` a given module,
   Python only imports it once.
   All subsequent imports of the same name return the same module instance
   (assuming you don’t manipulate the ``sys.modules`` dictionary
   behind the scenes).
   When the `Module Objects <https://docs.python.org/3/c-api/module.html>`_
   chapter of the Python/C API Reference Manual
   asserts that “Single-phase initialization creates singleton modules,”
   it means modules that are only ever instantiated once.

3. An object instantiated and assigned a name
   at a module’s outer level of indentation —
   the :doc:`/python/module-globals/index` —
   is also called a “singleton” object.
   For example, the official Python
   `Programming FAQ <https://docs.python.org/3/faq/programming.html>`_
   answer to the question
   `“How do I share global variables across modules?”
   <https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules>`_
   by illustrating how a global constant like ``x = 0``
   can be set in one module and then used in many other modules.
   Then, turning from simple constants to more complicated objects,
   it asserts that in Python
   “using a module is also the basis for implementing the Singleton design” —
   in Python we create a shared singleton object
   by assigning it a global name at the top level of a module.

A flyweight object (... “that is returned by constructor”?)
“CPython's empty tuple is a singleton and cached in” - NO, that’s a flyweight
True False are flyweights
.. “call frozenset() to get the empty frozenset singleton”

The one unique object that is ever returned
from a class that implements the Gang of Four’s Singleton Pattern.
object of which there is only one instance
ellipsis

Doc/library/marshal.rst:46:singletons :const:`None`, :const:`Ellipsis` and :exc:`StopIteration` can also be
None
NotImplemented

Lib/pydoc_data/topics.py

Doc/c-api/module.rst:258:singletons: if the *sys.modules* entry is removed and the module is re-imported,

Doc/library/stdtypes.rst:4646:``None`` (a built-in name).  ``type(None)()`` produces the same singleton.
but not Python 2
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

Singleton Pattern was a step towards Python:
substituted factory for syntactic instantiation.
