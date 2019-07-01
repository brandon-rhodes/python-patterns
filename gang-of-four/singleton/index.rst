
=======================
 The Singleton Pattern
=======================

.. TODO add to Global Object that the Python FAQ calls it a singleton object
   https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules

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
so we should start by distinguishing its several meanings.

1. A “singleton” is a tuple of length one.
   While this definition will surprise some programmers,
   it reflects the original definition of a “singleton” in mathematics —
   a set containing exactly one element.
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
   because ``import`` only creates a single instance of each module,
   at the moment when it is first imported.
   All subsequent imports of the same name return the same module instance.
   (If you don’t manipulate the ``sys.modules`` dictionary behind the scenes.)
   When the `Module Objects <https://docs.python.org/3/c-api/module.html>`_
   chapter of the Python/C API Reference Manual
   asserts that “Single-phase initialization creates singleton modules,”
   it means modules that are only ever instantiated once.

3. A “singleton” is a class instance
   that has been assigned a module global name
   through :doc:`/python/module-globals/index`.
   For example, the official Python
   `Programming FAQ <https://docs.python.org/3/faq/programming.html>`_
   answer to the question
   `“How do I share global variables across modules?”
   <https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules>`_
   asserts that in Python
   “using a module is also the basis for implementing the Singleton design” —
   because not only can a module’s global namespace store constants
   (the FAQ’s example is ``x = 0`` shared between several modules),
   but mutable class instances as well.

4. Individual flyweight objects from :doc:`/gang-of-four/flyweight/index`
   are often called “singleton” objects by Python programmers.
   For example, a comment inside the Standard Library’s ``itertoolsmodule.c``
   asserts that “CPython’s empty tuple is a singleton” —
   meaning that only a single empty tuple object is ever created,
   which ``tuple()`` returns over and over again
   every time it’s passed a zero-length sequence.
   A comment in ``marshal.c`` similarly refers
   to the “empty frozenset singleton.”
   But neither of these singleton objects
   is an example of the Gang of Four’s Singleton Pattern,
   because neither object is the sole instance of its class;
   ``tuple`` lets you build other tuple objects besides the empty tuple,
   and ``frozenset`` lets you build other frozen sets.
   The ``True`` and ``False`` objects are a pair of flyweights
   because neither is the sole instance of ``bool``.

Implementing
============

The 

Singleton Pattern was a step towards Python:
substituted factory for syntactic instantiation.


Examples
========

Python 3 has elevated several objects
to full-fledged examples of the Singleton Pattern
that previously had simply been “singletons”
in the sense of unique module globals.

Both ``None`` and ``Ellipsis`` in Python 2
are examples of :doc:`/python/module-globals/index`
where the interpreter provides access to an object
by assigning a name to it,
in this case in the ``__builtin__`` module.
But the objects are not available
through the objected oriented Singleton Pattern,
because Python doesn’t offer a callable constructor
by which either of them can be created.
Neither of their type objects is callable:

::

   >>> # Python 2
   >>> type(None)
   <type 'NoneType'>
   >>> NoneType = type(None)
   >>> NoneType()
   TypeError: cannot create 'NoneType' instances
   >>> type(Ellipsis)()
   TypeError: cannot create 'ellipsis' instances

py3 without error



Lib/pydoc_data/topics.py


.. Doc/library/marshal.rst:46:singletons :const:`None`, and :exc:`StopIteration` can also be
   Doc/c-api/module.rst:258:singletons: if the *sys.modules* entry is removed and the module is re-imported,
   Doc/library/enum.rst:1026:The most interesting thing about Enum members is that they are singletons.

When our software’s architecture
has failed to provide a line of code
with a reference to an object it needs,
a common workaround in Python
is :doc:`/python/module-globals/index`:
