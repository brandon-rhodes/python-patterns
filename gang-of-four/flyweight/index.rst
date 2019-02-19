
===================
 Flyweight Pattern
===================

*A “Structural Pattern” from the* :doc:`/gang-of-four/index`

.. admonition:: Verdict

   Flyweight objects are such a perfect fit for Python
   that the language itself uses the pattern
   for values like integers, strings, and Boolean true and false.

.. TODO mention that this is confused with “singleton” once the
   Disambiguation section is written

A perfect example of the Flyweight Pattern
is the Python |intern|_ function.
(It’s a builtin in Python 2,
but was moved into the |sys|_ module in Python 3.)
It keeps exactly one copy of each string you pass.
Each time you ask for the same string,
exactly the same object is returned —
it keeps only one copy of each string object in memory.

Let’s compute the string ``'python'`` two different ways
(to make it likely that any given Python implementation
will really give us two different strings)
and pass them to the intern function:

.. |intern| replace:: ``intern()``
.. _intern: https://docs.python.org/3/library/sys.html#sys.intern

.. |sys| replace:: ``sys``
.. _sys: https://docs.python.org/3/library/sys.html

>>> from sys import intern  # not necessary in Python 2
>>> a = intern('py' + 'thon')
>>> b = intern('PYTHON'.lower())
>>> a
'python'
>>> b
'python'
>>> a is b
True

Python uses the |intern|_ function internally when parsing source code
to eliminate the cost of names that are repeated several times,
and you can use it yourself when tackling data sets
that involve repeated strings.
Strings have all three of the key properties of a flyweight object:

* Python strings are immutable,
  which makes them safe to share.
  Otherwise a routine that decided to change one of the string’s characters
  would affect the single copy shared with all of the other users
  of |intern|_.

* A python string carries no context about how it is being used.
  If it needed to maintain a reference back
  to the list, dictionary, or other object that was using it,
  then each string could only serve in one context at a time.

* Strings are important for their value,
  not their object identity.
  We compare them with ``==`` instead of with the ``is`` keyword;
  a well-written Python program will not even notice
  whether the string ``"brandon"`` used as a directory name
  and ``"brandon"`` used somewhere else in the code as a username
  are the same object or two different objects.

The Gang of Four describe these requirements a bit differently
when they require that, “Most object state can be made extrinsic.”
They imagine starting with an object that’s a mix
of what they call “extrinsic” and “intrinsic” state::

    a1 = Glyph(width=6, ascent=9, descent=3, x=32, y=8)
    a2 = Glyph(width=6, ascent=9, descent=3, x=8, y=60)

Given a typeface and size,
each copy of a given letter — say, the letter ``a`` —
will have the same width, ascent above the baseline, and descent below it.
The Gang of Four call these attributes “intrinsic”
to what it means to be the letter ``a``.
But each ``a`` on a page will have a different ``x`` and ``y`` coordinate;
that state is “extrinsic” and varies from one object to another.

They would then arrive at the Flyweight by refactoring::

    a = Glyph(width=6, ascent=9, descent=3)
    a1 = DrawnGlyph(glyph=a, x=32, y=8)
    a1 = DrawnGlyph(glyph=a, x=8, y=60)

Not only can the space savings can be considerable,
but the `original 1990 paper introducing Flyweights <https://www.researchgate.net/profile/Mark_Linton2/publication/220877079_Glyphs_flyweight_objects_for_user_interfaces/links/58adbb6345851503be91e1dc/Glyphs-flyweight-objects-for-user-interfaces.pdf?origin=publication_detail>`_
found that a document editor written using the pattern
had considerably simpler code.

Factory or Constructor
======================

The Gang of Four only imagined using a factory function like |intern|
for managing a collection of flyweights,
but Python often moves the logic into a class’s constructor instead.

The simplest example in Python is the ``bool`` type.
It has exactly two instances.
While they can be accessed
through their builtin names ``True`` and ``False``,
they are also returned by their class
when it is passed an object to test for truthiness or falsehood.

>>> bool(0)
False
>>> bool('')
False
>>> bool(12)
True

As an implementation detail,
the default C language version of Python
also treats the integers −5 through 256 as flyweights:
those integers are created ahead of time as the interpreter launches,
and are always reused when an integer with one of those values is needed.
Computing any other integer value
results in a unique object from each computation.

>>> 1 + 4 is 2 + 3
True
>>> 100 + 400 is 200 + 300
False

There are a few other flyweights hiding in the Standard Library
for very common immutable objects,
like the empty string and the empty tuple.

>>> str() is ''
True
>>> tuple([]) is ()
True

But remember that not every object pre-built by the interpreter
qualifies as a flyweight.
The ``None`` object, for example, does not qualify:
it’s the only instance of ``NoneType``,
but the Flyweight Pattern
requires there to be a collection of objects.

Implementing Flyweights
=======================

The simplest flyweights are allocated ahead of time.
A simple system for assigning letter grades
might use flyweights for the grades themselves:

.. testcode::

   class Grade(object):
       def __init__(self, minimum, maximum, name):
           self.value = value

   _grades = [letter + suffix for letter in 'ABCDF'
                              for suffix in ('+', '', '-')]

   def compute_grade(percent):
       percent = max(50, min(99, percent))
       return _grades[(99 - percent) * 3 // 10]

   print(compute_grade(55))
   print(compute_grade(89))
   print(compute_grade(90))

.. testoutput::

    F
    B+
    A-

Factories that need to build a flyweight population dynamically
are more complicated:
they’ll need a dynamic data structure
in which to enroll the flyweights
so they can find them again.
A dictionary is the typical choice:

.. testcode::

   _strings = {}

   def my_intern(string):
       s = _strings.setdefault(string, string)
       return s

   a1 = my_intern('A')
   b1 = my_intern('B')
   a2 = my_intern('A')

   print(a1 is b1)
   print(a1 is a2)

.. testoutput::

   False
   True

should you keep them all?

weakref.WeakValueDictionary

either with class __new__
