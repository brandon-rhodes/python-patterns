
=================
 Sentinel Object
=================

*A Python variation on the “Creational Pattern” inspired by Modula-2 and Modula-3*

.. admonition:: Verdict

   python’s


.. contents:: Contents:
   :backlinks: none



Sentinel value
--------------

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

Null pointer
------------

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

Null object
----------------

Fowler; woolf

 unimportant observation is made
 by Martin Fowler in his book x

 do the actual quote

 Choosing
 adopting the convention that a name might either refer to a useful value
 or else might bear a special value which means nothing is here
 imposes a burden upon every subsequent piece of code that must handle that value

 to take an example

E

 all of the code Downstream from here
is going to have to test whether the value is none

E

 Martin describes an interesting alternative mentions an interesting all turn
 described by wolf

 Quote

 before designating a value
 that might either be a useful object or none
 if you are in a domain
 double check weather you might be in a domain
 where a functioning user object might be provided instead
 yeah

Sentinel object
----------------------

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
