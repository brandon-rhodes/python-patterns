
===================
 Flyweight Pattern
===================

*A “Structural Pattern” from the* :doc:`/gang-of-four/index`

.. admonition:: Verdict

   Flyweight objects are such a perfect fit for Python
   that the language itself uses the pattern
   for values like integers, strings, and Boolean true and false.

A perfect example of the Flyweight Pattern
is the Python |intern|_ function.
(It’s a builtin in Python 2,
but was moved into the |sys|_ module in Python 3.)
It keeps exactly one copy of each string you pass.
Each time you ask for the same string,
exactly the same object is returned —
it keeps only one copy of each string object in memory.

.. |intern| replace:: ``intern()``
.. _intern: https://docs.python.org/3/library/sys.html#sys.intern

.. |sys| replace:: ``sys``
.. _sys: https://docs.python.org/3/library/sys.html

>>> from sys import intern  # not necessary in Python 2
>>> a = intern('Python'.lower())
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

The Gang of Four 
  The Gang of Four  “extrinsic” state




Usually I write my own introduction to each design pattern,
but let’s celebrate how well this pattern fits Python
with a direct quote from the :doc:`/gang-of-four/index`.
They recommend the pattern when:

* “An application uses a large number of objects.”
* “Storage costs are high because of the sheer quantity of objects.”
* “Most object state can be made extrinsic.”
* “Many groups of objects may be replaced by relatively few shared
  objects once extrinsic state is removed.”
* “The application doesn't depend on object identity. Since flyweight
  objects may be shared, identity tests will return true for
  conceptually distinct objects.”

It’s easy for a Python program to satisfy the first two criteria:
in Python, everything is an object.

The key is their concept of “extrinsic” state.



The key is what, in their third criterion, they call “extrinsic” state.
In Python we would express the same idea by asking
whether some of an object’s attributes
could be split off into an immutable object
that could serve as a shared value.
Imagine a document


Instead of copying the height, width, and  of a 


Their final criteria



The Flyweight pattern was invented
when objects were an expensive luxury.
While you might have used an object to represent a paragraph or sentence,
you would not represent each individual character with an object.

This expense could be 

and 
was originally developed
to make objects 
in a language


not the None object

originated in languages
where 

   Flyweight objects are crucial to Python’s design.
   In a language where “everything is an object” —
   where even integers, characters, and Boolean values
   are represented by full-fledged objects —
   it is common for classes to build popular values ahead of time.
   Most famously,
   no matter how many times the ``bool()`` constructor is called
   it always returns one of the two objects ``True`` or ``False``;
   new ``bool()`` objects are always
   

Prebuilt Objects
================


Interning
=========



height width x y    vs   x y  ->   height width


   
   a separate object every integer and floating point value
   
   When everything is an object,
   

.. TODO mention that this is confused with “singleton” once the
   Disambiguation section is written




A flyweight object (... “that is returned by constructor”?)

None?

>>> type(NotImplemented)()
NotImplemented

The Flyweight pattern is usually only appropriate
for classes whose instances are immutable;
if an instance’s value could be updated later

definition: pool of immutable objects

intern()


weakref.WeakValueDictionary

"State that a flyweight needs to function must be characterized as
either intrinsic or extrinsic. Intrinsic state is stored in the
ConcreteFlyweight object; extrinsic state is stored or computed by
Client objects. Clients pass this state to the flyweight when they
invoke its operations."

but they don't use constructor

int, str, bool

lazy vs ahead of time

outside of stdlib?


