
=================
 Sentinel Object
=================

*A Python variation on a “Creational Pattern” inspired by Modula-2 and Modula-3*

.. admonition:: Verdict

   The Sentinel Object pattern is a standard Pythonic approach
   that’s used both in the Standard Library and beyond.
   The pattern usually uses the built-in ``None`` object,
   but in situations where ``None`` might be a useful value
   a unique sentinel ``object()`` can be used instead
   to indicate missing or unspecified data.

.. contents:: Contents:
   :backlinks: none

Programming is easiest
in problem domains where values are always specified:
where everyone in the database is guaranteed to have a name,
where we know the age of every employee,
and where a datum was collected successfully
for every second of the experiment.

But the world is rarely that simple,
and so patterns are needed for those cases
where object attributes or whole objects are going to be missing.
What simple mechanisms are available
to distinguish useful data
from placeholders that indicate data is absent?

Sentinel Value
==============

The traditional Sentinel Value pattern
will be familiar to Python programmers
from the
`str.find() <https://docs.python.org/3/library/stdtypes.html#str.find>`_
method.
While its sibling
`str.index() <https://docs.python.org/3/library/stdtypes.html#str.index>`_
is more rigorous,
raising an exception if it can’t find the substring you’ve asked about,
``find()`` lets you skip writing an exception handler
by instead returning the sentinel value ``-1``
when the substring is not found.
This often saves a line of code and a bit of indentation:

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
The value ``-1`` is simply an integer,
just like the function’s other possible return values,
but with a special meaning that has been agreed upon ahead of time —
and woe betide the program that receives back ``-1``,
forgets to check, and tries using it to index into the string!
The result is never what the programmer intended.

If ``find()`` had been invented today,
it would instead have used the Sentinel Object pattern
that we will describe below
by simply returning ``None`` for “not found”.
There then would have been no possibility
of the return value being misused as an index.

Sentinel values are particularly common today in the Go language,
which encourages a style of programming
where routines often insist on accepting and returning strings
with no alternative possible.
In such circumstance programmers quickly turn to empty strings
or, more rarely, unique sentinel string values
when they want to communication “there’s no useful data here.”

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
it can, for example, be difficult to design Null Objects
that keep averages and other statistics valid —
Null Objects appear even in the Python Standard Library,
such as the ``logging`` module’s ``NullHandler``
which is a drop-in replacement for its other handlers
but does no actual logging.

Sentinel objects
================

The standard Python sentinel is the built-in ``None`` object,
used wherever some alternative to an integer, float, string,
or other meaningful value needs to be provided.
For most programs it is entirely sufficient
and its presence can be infallibly tested
with::

    if other_object is None:

But there are two interesting circumstances
where programs need an alternative to ``None``.

First,
a general purpose data store
doesn’t have the option of using ``None`` for missing data
if users might themselves try to store the ``None`` object.
Consider, for example, wrapping a function that can return ``None``
with the least-recently-used (LRU)
function cache offered by the Standard Library.
The cache uses a Python dictionary as its data store,
and might have naively attempted to retrieve a cached value with::

   result = cache_get(key)

So the ``lru_cache()`` instead uses the Sentinel Object pattern.
Hidden inside of a closure that surrounds the wrapper that it returns
is an utterly unique object
created specifically for the use of each separate cache. ::

   sentinel = object()  # unique object used to signal cache misses

By providing this sentinel object
as the second argument to ``dict.get()`` —
here aliased to the name ``cache_get``
in a closure-level private example
of the :doc:`prebound-methods` pattern —
the cache can distinguish a function call
whose result is already cached and happened to be ``None``
from a function call that has not yet been cached::

   result = cache_get(key, sentinel)
   if result is not sentinel:
       ...

This pattern occurs several times in the Standard Library.

* As shown above, ``functools.lru_cache()`` uses a sentinel object
  internally.

* The ``bz2`` module has a global ``_sentinel`` object.

* The ``configparser`` module has a sentinal ``_UNSET``
  also defined as a module global.

The second interesting circumstance that calls for a sentinel
is when a function or method wants to know
whether a caller supplied an optional keyword argument or not.
Usually Python programmers give such an argument a default of ``None``,
which is my own experience has always worked fine.
But if your code truly needs to know the difference,
then a sentinel object saves the day.

An early description of using sentinels for parameter defaults
was Fredrik Lundh’s
`“Default Parameter Values in Python” <http://effbot.org/zone/default-values.htm>`_
which was followed over the years
by posts by both Ian Bicking
`“The Magic Sentinel” <http://www.ianbicking.org/blog/2008/12/the-magic-sentinel.html>`_
and Flavio Curella
`“Sentinel values in Python <https://www.revsys.com/tidbits/sentinel-values-python/>`_
who both worried about their sentinel objects’ lack of a readable ``repr()``
and came up with various fixes.

But whatever the application,
the core of the Sentinel Object pattern
is that it is the object’s identity — *not* its value —
that lets the surrounding code recognize its significance.
If you are using an equality operator to detect the sentinel,
then you are merely using the Sentinel Value pattern
described at the top of this page.
The Sentinel Object is defined
by its use of the Python ``is`` operator
to detect when the sentinel is present.
