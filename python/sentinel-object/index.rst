
=================
 Sentinel Object
=================

*A Python variation on the “Creational Pattern” inspired by Modula-2 and Modula-3*

.. admonition:: Verdict

   python’s


.. contents:: Contents:
   :backlinks: none



Sentinel value
==============

The crucial 

*within* domain

Nan?

Empty string

An older pattern dictating
 still coming in statically typed languages

A traditional problem in computing
is the need to mark a particular value as special
in a sequence of values that which will otherwise all be taken
as having their literal meaning.
This need arises in two cases in particular:

* To mark particular values in a sequence as “unknown” or “blank”.
* To mark the end of a sequence with a special value.

In each case,
the solution is to designate a special “sentinel” value
that we promise never to use as a normal value in the sequence,
so that it can mean “unknown” (or “end”) without ambiguity.
Whether the values are integers, floating point numbers,
strings, or something more exotic,
the key to the Sentinel Value pattern
is that all code handling the values
knows to treat the sentinel as special when it appears.

There are thus two costs to the Sentinel Value:

1. The range of the non-sentinel values contracts by one.
   This isn’t a problem when the sequence by nature
   uses only a fraction of the domain’s possible values;
   if a numeric sequence is entirely of positive numbers,
   for example, then choosing zero as the sentinel
   entails no inconvenience.
   But in the general case,
   one less number or string will be available
   for use in the data.

2. Most the code that touches the raw sequence
   will need to treat the sentinel values specially.
   If the sentinel means “missing” then sums and averages
   will need to check every value against the sentinel
   so it doesn’t affect the result.
   If the sentinel means “end”,
   then every step of an iterator
   will need to check the current value against the sentinel
   to decide whether to proceed.

--

The traditional practice of designating a sentinel value
among the possible values a routine might return
will be familiar to Python programmers
from the
`str.find() <https://docs.python.org/3/library/stdtypes.html#str.find>`_
method.
While its sibling method
`str.index() <https://docs.python.org/3/library/stdtypes.html#str.index>`_
is more rigorous,
raising an exception if it can’t find the substring you ask about,
``find()`` lets you skip the exception handling
by returning the sentinel value ``-1`` when the substring is not found.
This often saves a line of code:

.. testcode::

   try:
       i = a.index(b)
   except:
       return

   # versus

   i = a.find(b)
   if i == -1:
       return

This is a classic example of a sentinel value.
It is an integer,
just like the function’s other possible return values,
but with a special meaning that has been agreed upon ahead of time —
woe upon the code that uses ``find()``’s return value without checking,
and looks for the substring at position ``-1`` in the original string!

If ``find()`` had been invented today,
it would instead have been designed to return ``None`` for “not found”
and so would have avoided the problem of also being a possibly valid
string index — but then we could not have used it as our example!

and even among types that lack enata number value
 like the integer and string
 recent languages like ago
 which don't make it convenient to return none if you are required to return an integer
 the less you to clear up whatever go calls an optional type
 are convincing many programmers
 that they can go much farther than they had expected without substantial confusion
 using 0 and the empty string
 where they have no more specific data to contribute
 all the python programmer will often value
 the semantic Clarity that comes with the use of none
probably do it in situations
 where oh with in tight Sentinel value
 would satisfy as well

Null pointers
=============

This pattern is impossible in Python.
Every name in Python either does not exist,
or it exists and refers to an object.
You can remove a name with ``del name``,
or else you can assign a new object to it;
Python offers no other alternatives.
Behind the scenes, each name in Python is a pointer
that stores the address of the object to which it currently refers.
Even if the name points to an object as simple as the ``None`` object,
it must contain a valid address for as long as it exists.

This guarantee supports an interesting sentinel pattern
down in the C language implementation
of the default version of the Python language.
The C language lacks Python’s guarantee that a name —
which C calls a “pointer” —
will always hold the address of a valid object.
Taking advantage of this flexibility,
C programmers use the special address of zero
to mean “this pointer currently doesn’t point at anything” —
turning zero, or ``NULL`` as many C programs define it,
into a sentinel value that code must carefully compare each pointer against
before trying to read from that address.
Trying to read bytes from memory location zero is usually fatal,
the operating system stopping the process in its tracks
and reporting a ``segmentation fault``.

The fact that all Python values, even ``None`` and ``False``,
are real objects with non-zero addresses
means that Python functions implemented in C
have the value ``NULL`` available to mean something special.
And they use it:
a zero pointer means
“this function did _not_ complete and return a value;
instead, it raised an exception.”
This allows the C code beneath Python
to avoid the two-value return pattern
that pervades Go code::

    byte_count, err := fmt.Print("Hello, world!")
    if err != nil {
            ...
    }

Instead, C language routines that call Python
can distinguish legitimate return values from an exception
using only the single return value supported by C functions:

    PyObject *my_repr = PyObject_Repr(obj);
    if (my_repr == NULL) {
         ...
    }

The exception itself is stored elsewhere
and can be retrieved using the Python C API.

Null objects
============

My attention was drawn to this pattern
while reading :doc:`fowler-refactoring/index`
which credits Bobby Woolf for its explication.
It has nothing to do with the “null pointer” explained
in the previous section!
Instead it describes a special kind of sentinel object.

Imagine a sequence of ``Employee`` objects
which usually have another employee as their ``manager`` attribute
but not always.
The default Pythonic approach to represent “no manager”
would be to assign ``None`` to the attribute.

A routine tasked with displaying an employee profile
will have to check for the sentinel object ``None``
before trying to invoke any methods on the manager::

    for e in employees:
        if e.manager is None:
            m = 'no one'
        else:
            m = e.manager.display_name)
        print(e.name, '-', m)

And this pattern will be repeated in all code
that needs to reference the attribute.

Woolf offers the intriguing possibility
of replacing all of the exceptional ``None``
values with an ``Employee`` object
specifically designed to represent the idea of “no one”::

    NO_PERSON = Person(name='no one')

Employee objects will now be assigned this ``NO_PERSON`` object asb
their manager instead of ``None``,
and both kinds of code touching employee managers will benefit:

* Code that produces simple displays or summaries
  can simply print or tally the ``NO_ONE`` manager object
  as though it were a normal employee object.
  If the code can run successfully against the Null Object,
  then the need for a special ``if`` statement disappears.

* Code that does need to specially handle the case
  of an employee with no acting manager
  now becomes a bit more readable —
  instead of using the generic ``is None``
  it will perform the check with the specific ``is NO_PERSON``
  and will thereby gain a bit more readability.

While not appropriate in all situations —
it can, for example, take some attention to design Null Objects
that keep averages and other statistics valid —
Null Objects appear even in the Python Standard Library,
such as the ``NullHandler`` provided by the ``logging`` module.

Sentinel objects
================

You will need a sentinel object
in the special circumstance

1 youre one year in Python none see not in C

2 

 the Sentinel you will want a sentinel object
 The Sentinel object 

File: Lib/bz2.py
27:1:_sentinel = object()  <--- line occurs several times
^ token? no.

Lib/functools.py
_NOT_FOUND = object()
val = cache.get(self.attrname, _NOT_FOUND)

File: Lib/configparser.py
357:1:_UNSET = object()

only for efficiency if used in only one routine

http://www.ianbicking.org/blog/2008/12/the-magic-sentinel.html
for optional argument, noting Python 3 thing

http://effbot.org/zone/default-values.htm
for optional argument

https://www.revsys.com/tidbits/sentinel-values-python/
for optional argument
