
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
   and makes a single instance available through a class method.
   Instead, a Python class can simply rig its ``__new__()`` method
   to always return the same instance.
   But an even more Pythonic approach,
   if your design forces you to offer global access to a singleton object,
   is to use :doc:`/python/module-globals/index` instead.

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
   when they call an object a “singleton”:
   an object whose class returns the same object
   every time it’s called.

The Python 2 Standard Library included no examples of the Singleton Pattern.
While it did feature singleton objects like ``None`` and ``Ellipsis``,
the language provided access to them through the more Pythonic
:doc:`Global Object Pattern </python/module-globals/index>`
by giving them names in the ``__builtin__`` module.
Their classes were not callable:

::

    >>> type(None)
    <type 'NoneType'>
    >>> NoneType = type(None)
    >>> NoneType()
    TypeError: cannot create 'NoneType' instances
    >>> type(Ellipsis)()
    TypeError: cannot create 'ellipsis' instances

But in Python 3, the classes were upgraded to use the Singleton Pattern:

>>> result = type(None)()
>>> print(result)
None
>>> type(Ellipsis)()
Ellipsis

This makes life easier for programmers
needing a quick callable that always returns ``None``,
but such occasions are rare.
In most Python projects these classes are never called
and the benefit remains purely theoretical.
When Python programmers need ``None``
they use :doc:`/python/module-globals/index`
and simply type its name.

Gang of Four implementation
===========================

The C++ language that the Gang of Four were targeting
imposed a distinct syntax on object creation,
that looked something like::

    # Object creation in a language
    # that has a “new” keyword.

    log = new Logger()

A line of code that performed the ``new`` operation
would always return a new class instance —
never a singleton.
In the presence of this special syntax,
what were their options for offering singleton objects?

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
   no global object could depend upon being able to call any other,
   so the responsibility for initializing a global
   would often have fallen on client code.

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
but one alternative is to raise an exception in ``__init__()``
to make normal object instantiation impossible.
The class method can then use a dunder method trick
to create the object without triggering ``__init__()`` and its exception:

.. testcode::

    # What the Gang of Four’s original Singleton Pattern
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
from creating new instances by calling the class:

.. testcode::

    log = Logger()

.. testoutput::

    Traceback (most recent call last):
      ...
    RuntimeError: Call instance() instead

Instead, they are directed to use the ``instance()`` class method,
which does successfully create and return an object:

.. testcode::

    log1 = Logger.instance()
    print(log1)

.. testoutput::

    Creating new instance
    <Logger object at 0x7f0ff5e7c080>

Subsequent calls to ``instance()`` simply return the singleton
without repeating the initialization step
(note that “Creating new instance” isn’t printed again),
exactly as the Gang of Four intended:

.. testcode::

    log2 = Logger.instance()
    print(log2)
    print('Are they the same object?', log1 is log2)

.. testoutput::

    <Logger object at 0x7f0ff5e7c080>
    Are they the same object? True

There are more complicated schemes that I can imagine
for implementing the original Gang of Four class method.
For example, instead of always raising an exception in ``__init__()``,
it could introspect the stack and skip raising the exception
if it’s being called from ``instance()`` method.
That would let ``instance()`` call ``Logger()`` normally
and avoid the manual call to ``__new__()``.

But the above example does the best job, I think,
of illustrating the original scheme with the least magic possible.
Since the original approach is not a good fit for Python anyway,
I’ll resist the temptation to iterate on it further,
and instead move on to how the pattern is best supported in Python.

Pythonic Implementation
=======================

In one sense,
Python started out better prepared than C++ for the Singleton Pattern
because Python instantiation always uses the syntax of calling a factory::

    log = Logger()

But renaming the class
and putting a factory function named ``Logger`` in its place,
while successfully pivoting the above line of code,
would break code that expected ``isinstance()`` to work with ``Logger``
or that tried to subclass it.
So Python 2.4 added the ``__new__()`` dunder method
to support object creation patterns
like the Singleton Pattern and :doc:`/gang-of-four/flyweight/index`.

The Web is replete with Singleton Pattern recipes featuring ``__new__()``
that each propose a more or less complicated mechanism
for working around the method’s biggest quirk:
the fact that ``__init__()`` gets called on its return value
whether it returns a new object or not.
I will instead simply not define an ``__init__()`` method
and thus avoid having to work around it:

.. testcode::

    class Logger(object):
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                print('Creating the object')
                cls._instance = super(Logger, cls).__new__(cls)
                # Put any initialization here.
            return cls._instance

.. testcode::
   :hide:

   def fake_repr(self):
       return '<Logger object at 0x7fa8e9cf7f60>'

   Logger.__repr__ = fake_repr

The object is created on the first call to the class:

.. testcode::

    log1 = Logger()
    print(log1)

.. testoutput::

    Creating the object
    <Logger object at 0x7fa8e9cf7f60>

But no further objects are created on the second and subsequent calls.
The message “Creating the object” does not print,
nor is a different object returned:

.. testcode::

    log2 = Logger()
    print(log2)
    print('Are they the same object?', log1 is log2)

.. testoutput::

    <Logger object at 0x7fa8e9cf7f60>
    Are they the same object? True

The example above opts for simplicity,
at the expense of making two ``cls._instance`` class attribute lookups
in the common case;
if singleton access were in a program’s critical path,
a local name or other connivance could eliminate the double lookup.
Or the method could consist of a single ``return`` statement
that short circuits to returning the instance if it already exists,
``or`` calls another method to construct and store it.

But however elaborately tweaked,
the above pattern is the basis of every Python class
that hides a singleton object
behind what reads like normal class instantiation.

Examples
========

Lib/pydoc_data/topics.py


.. Doc/library/marshal.rst:46:singletons :const:`None`, and :exc:`StopIteration` can also be
   Doc/c-api/module.rst:258:singletons: if the *sys.modules* entry is removed and the module is re-imported,
   Doc/library/enum.rst:1026:The most interesting thing about Enum members is that they are singletons.

When our software’s architecture
has failed to provide a line of code
with a reference to an object it needs,
a common workaround in Python
is :doc:`/python/module-globals/index`:

should you?
does it really need to be unique?
use test-driven development.
you might be locking people in.
you make syntax ambiguous.
