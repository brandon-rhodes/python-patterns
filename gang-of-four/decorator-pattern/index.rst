
=======================
 The Decorator Pattern
=======================

.. TODO
   talk about editing the class of objects that are returned
   simpler than subclassing: you are not in between obj and its own methods
     classes are perilous things
     and subclasses, doubly perilous

.. admonition:: Verdict

   The Decorator Pattern can be useful in Python code!
   Happily, the pattern can be easier to implement
   in a dynamic language like Python
   than in the static languages where it was first practiced.
   Use it on the rare occasion
   when you need to adjust the behavior of an object
   that you can’t subclass but can only wrap at runtime.

The Python core developers made the terminology
surrounding this design pattern more confusing than necessary
by using the *decorator* for an entirely unrelated language feature.
The timeline:

* The design pattern was developed and named in the early 1990s
  by participants in the “Architecture Handbook” series of workshops
  that were kicked off at OOPSLA ’90,
  a conference for researchers of object-oriented programming languages.

* The design pattern became famous as the “Decorator Pattern”
  with the 1994 publication
  of the Gang of Four’s *Design Patterns* book.

* In 2003, the Python core developers
  decided to re-use the term *decorator*
  for a completely unrelated feature they were adding to Python 2.4.

Why were the Python core developers
not more concerned about the name collision?
It may simply be that Python’s dynamic features
kept its programming community so separate
from the world of design-pattern literature for heavyweight languages
that the core developers never imagined that confusion could arise.

To try to keep the two concepts straight,
I will use the term *decorator class*
instead of just *decorator*
when referring to a class that implements the Decorator Pattern.

Definition
==========

A *decorator* class:

* Is an *adapter* (see the *Adapter Pattern*)
* That implements the same interface as the object it wraps
* That delegates method calls to the object it wraps

The decorator class’s purpose
is to add to, remove from, or adjust the behaviors
that the wrapped object would normally implement
when its methods are called.
With a decorator class, you might:

* Log method calls that would normally work silently
* Perform extra setup or cleanup around a method
* Pre-process method arguments
* Post-process return values
* Forbid actions that the wrapped object would normally allow

These purposes might remind you of situations
in which you would also think of subclassing something.
But the Decorator Pattern has a crucial difference:
you can only solve a problem with a subclass
when your own code is in charge
of creating the objects in the first place.
For example, it isn’t helpful
to subclass the Python file object
if a library you’re using is returning normal file objects
and you have no way to intercept their construction —
your new ``MyBetterFile`` subclass would sit unused.
But a decorator class does not have that limitation.
It can be wrapped around a plain old file object any time you want,
without the need for you be in control
when the wrapped object was created.

Approach 1: static methods and properties
=========================================

First, let’s learn the drudgery
of creating the kind of decorator class you would write in C++ or Java.
We will not take advantage of the fact
that Python is a dynamic language,
but will give the wrapper a simple static definition
of every method and property that exists on a Python file object.

To be complete —
to provide a real guarantee
that every method called and attribute manipulated
on the decorator object
will be backed by the real behavior of the adapted object —
the decorator class will need to implement:

* Every method of the adapted class
* A getter for every attribute
* A setter for every attribute
* A deleter for every attribute

This approach is conceptually simple
but, wow, it involves a lot of code!

Imagine that one library is giving you open Python file objects,
and you need to pass them to another routine or library —
but to debug some product issues with latency,
you want to log each time that data is written to the file.

Python file objects often seem quite simple.
We usually ``read()`` from them,
``write()`` to them,
and not much else.
But in fact the file object supports more than a dozen methods
and offers five different attributes!
A wrapper class that really wants to implement that full behavior
runs to nearly 100 lines of code —
as shown here, in our first working example of the Decorator Pattern:

`verbose_static_wrapper.py <verbose_static_wrapper.py>`_

.. literalinclude:: verbose_static_wrapper.py

So for the sake of the half-dozen lines of code at the bottom
that supplement the behavior of ``write()`` and ``writelines()``,
another hundred or so lines of code are necessary in this case.

If the class you are decorating
does not have as many methods and attributes as a Python file,
then wrapping it will be simpler and less verbose.
But in the general case,
writing out the full wrapper will be tedious
unless you have a tool like an IDE that can automate the process.
Also, the wrapper will need to be updated in the future
if the underlying object gains (or loses)
any methods, arguments, or attributes.

Trick 1a: Tactical wrappers
===========================



then, wrapper that does dynamic getattr
(explain why you would use getattribute?)

then, wrapper that does copy-across of method in __init__

? then, wrapper that does caching? ?

then, wrapper that does copy-across based on loop

then, superclass that does copy-across?

would be mitigated by interface


Caveat: Decorator classes aren’t perfect
========================================




Dodge 1: Monkey-patch each object
=================================


Dodge 2: Monkey-patch the class?
================================



