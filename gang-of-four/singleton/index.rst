
=======================
 The Singleton Pattern
=======================

.. TODO add to Global Object that the Python FAQ calls it a singleton object
   https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules

*A “Creational Pattern” from the* :doc:`/gang-of-four/index`

.. admonition:: Verdict

   Python programmers almost never implement the Singleton Pattern
   as described in the :doc:`/gang-of-four/index`,
   where an object forbids normal instantiation
   and forces callers to invoke a class method instead.
   Instead, Python programmers are more likely to rig ``__new__()``
   so it always returns the same instance.
   But an even more Pythonic approach,
   if your design forces you to offer global access to a singleton object,
   is to use :doc:`/python/module-globals/index` instead.

should you?
does it really need to be unique?
use test-driven development.
you might be locking people in.
you make syntax ambiguous.

Disambiguation
==============

Python was already using the term “singleton”
before the Singleton Pattern was defined by
the object oriented design pattern community.
So we should start by distinguishing the several meanings
of “singleton” in Python:

1. A “singleton” is a tuple of length one.
   While this definition might surprise some programmers,
   it reflects the original definition of a “singleton” in mathematics:
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
   because ``import`` creates a single instance of each module
   at the moment the module is first imported,
   and subsequent imports of the same name
   return that same module instance.
   When the `Module Objects <https://docs.python.org/3/c-api/module.html>`_
   chapter of the Python/C API Reference Manual
   asserts that “Single-phase initialization creates singleton modules,”
   it means by “singleton module” a module that is only ever instantiated once.

3. A “singleton” is a class instance
   that has been assigned a module global name
   through :doc:`/python/module-globals/index`.
   For example, the official Python
   `Programming FAQ <https://docs.python.org/3/faq/programming.html>`_
   answers the question
   `“How do I share global variables across modules?”
   <https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules>`_
   with the assertion that in Python
   “using a module is also the basis for implementing the Singleton design” —
   because not only can a module’s global namespace store constants
   (the FAQ’s example is ``x = 0`` shared between several modules),
   but mutable class instances as well.

4. Individual flyweight objects
   that are examples of :doc:`/gang-of-four/flyweight/index`
   are often called “singleton” objects by Python programmers.
   For example, a comment inside the Standard Library’s ``itertoolsmodule.c``
   asserts that “CPython’s empty tuple is a singleton” —
   meaning that only one empty tuple object is ever created,
   and ``tuple()`` returns it over and over again
   every time it’s passed a zero-length sequence.
   A comment in ``marshal.c`` similarly refers
   to the “empty frozenset singleton.”
   But neither of these singleton objects
   is an example of the Gang of Four’s Singleton Pattern,
   because neither object is the sole instance of its class:
   ``tuple`` lets you build other tuples besides the empty tuple,
   and ``frozenset`` lets you build other frozen sets.
   Similarly, the ``True`` and ``False`` objects are a pair of flyweights,
   not examples of the Singleton Pattern,
   because neither is the sole instance of ``bool``.

5. Finally, Python programmers on a few rare occasions
   do actually mean “The Singleton Pattern”
   when they call an object a “singleton”.
   Which Python objects qualify?
   See the next section for the pattern’s formal definition.

Original implementation
=======================

The C++ language that the Gang of Four were targeting
imposed a distinct syntax on object creation,
that looked something like::

    # Object creation in a language
    # that has a “new” keyword.

    log = new Logger()

In the presence of this special syntax,
how did they manage to offer singleton objects?

1. The Gang of Four did not take the easy way out
   and use :doc:`/python/module-globals/index`
   because it did not work particularly well
   in early versions of the C++ language.
   There, global names all shared a single crowded global namespace,
   and elaborate naming conventions were necessary
   to prevent names from different libraries from colliding.
   So the Gang judged that adding both a class and its singleton instance
   to the global namespace was excessive.
   And since C++ programmers couldn’t control the order
   in which global objects were initialized,
   no global object could depend upon being able to call any other.

2. There was no way to override the meaning of ``new`` in C++
   so an alternative syntax was necessary
   if all clients were to receive the same object.
   It was, though, at least possible to make it a compile-time error
   for client code to call ``new`` and create additional instances,
   by marking the class constructor as either ``protected`` or ``private``.

3. So the Gang of Four wound up pivoting
   in the same direction Python pivoted for its own object design,
   by having clients invoke a callable to ask for the singleton object.
   They chose a class method as their preferred callable.
   Unlike a global function,
   a class method avoids adding yet another name to the global namespace,
   and unlike a static method,
   it can be used to instantiate subclasses of the main singleton class.

How could Python code illustrate their approach?
Python lacks the complicated concepts of ``protected`` or ``private`` methods,
but an alternative would be to simply raise an exception in ``__init__()``
to make normal object instantiation impossible.
The class method can then use a trick
to create the object while skipping initialization:

.. testcode::

    # What the Gang of Four’s actual Singleton Pattern
    # might look like in Python.

    class Logger(object):
        _instance = None

        def __init__(self):
            raise RuntimeError('Call instance() instead')

        @classmethod
        def instance(cls):
            if cls._instance is None:
                print('Creating new instance')
                cls._instance = cls.__new__(cls)
                # Put any initialization here.
            return cls._instance

.. testcode::
   :hide:

   def fake_repr(self):
       return '<Logger object at 0x7f0ff5e7c080>'

   Logger.__repr__ = fake_repr

This successfully prevents clients
from accidentally creating new instances
by calling the class:

.. testcode::

    log = Logger()

.. testoutput::

    Traceback (most recent call last):
      ...
    RuntimeError: Call instance() instead

Instead, they are directed to use the class method,
which does successfully return an object:

.. testcode::

    log1 = Logger.instance()
    print(log1)

.. testoutput::

    Creating new instance
    <Logger object at 0x7f0ff5e7c080>

Subsequent calls to ``instance()`` simply return the singleton
without repeating the initialization step,
exactly as the Gang of Four intended:

.. testcode::

    log2 = Logger.instance()
    print(log2)
    print('Are they the same object?', log1 is log2)

.. testoutput::

    <Logger object at 0x7f0ff5e7c080>
    Are they the same object? True

There are more complicated schemes that I can imagine
for implementing the original Gang of Four class method —
for example, some magic could be added to ``__init__()``
that checks the stack
and performs initialization instead of raising an exception
if its caller is the ``instance()`` method.
That would allow ``instance()`` to call ``Logger()`` normally
without making a manual call to ``__new__()``.

But the above example does the best job, I think,
of illustrating the original scheme with the least magic possible.
As the original approach is not a good fit for Python anyway,
I’ll resist the temptation to iterate on it
and move along to a more likely implementation of the pattern in Python.

Pythonic Implementation
=======================

Second, Python not only allows object initialization to be customized
through the ``__init__()`` method,
but object creation itself through the ``__new__()`` method.
Thanks to these two features,
calling code will not need to be rewritten
because a Python class decides to switch to the Singleton Pattern.

The Web is replete with

.. testcode::

    class Logger(object):
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                print('new')
                cls._instance = super(Logger, cls).__new__(cls)
            return cls._instance

        def __init__(self):
            print('init')

    print('First call')
    log1 = Logger()
    print('Second call')
    log2 = Logger()
    print('Are they the same object?', log1 is log2)

.. testoutput::

    First call
    new
    init
    Second call
    init
    Are they the same object? True

Um

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
