
=======================
 The Decorator Pattern
=======================

.. TODO
   talk about editing the class of objects that are returned
   simpler than subclassing: you are not in between obj and its own methods
     classes are perilous things
     and subclasses, doubly perilous

The Python core developers made the terminology
surrounding this design pattern more confusing than necessary
by using the *decorator* for an entirely unrelated language feature.
The timeline went something like this:

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
It may simply be that Python’s dynamic design
kept its programmers so separate
from the world of design-pattern literature for heavyweight languages
that they imagined that confusion would never arise.

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

* Log method calls that would normally succeed or fail silently
* Perform extra setup or cleanup around a method
* Pre-process method arguments or post-process return values
* Forbid actions that the wrapped object would normally allow

These purposes might remind you
of situations in which you would think of subclassing something.
But the Decorator Pattern has a crucial difference:
you can only solve a problem with a subclass
when your own code is in charge
of creating the objects in the first place.
For example, it isn’t helpful
to subclass the Python file object
if a library you’re using
is going ahead and creating Python file objects
without asking you what class you wanted them to be —
your new ``MyBetterFile`` subclass would sit there unused.
But a ``FileDecorator`` wrapper class does not have that limitation.
It can be wrapped around a plain old file object any time you want,
without the need for you be in control
at the moment the file is first opened.

Example 1: static methods and properties
========================================

First, let’s learn the drudgery
of creating the kind of decorator you would write in C++ or Java.
To be complete —
to provide a real guarantee that every action on the decorator object
will be backed by the real behavior of the adapted object —
the decorator class will need to implement:

* Every method of the adapted class
* A getter for every attribute
* A setter for every attribute
* A deleter for every attribute

This is conceptually simple but, wow, it involves a lot of code!

Imagine that a library is giving you open Python file objects
that you need to pass to another routine or library —
but you want all of the output


`verbose_static_wrapper.py <verbose_static_wrapper.py>`_




would be mitigated by interface


.. literalinclude:: verbose_static_wrapper.py

then, wrapper that does dynamic getattr
(explain why you would use getattribute?)

then, wrapper that does copy-across of method in __init__

? then, wrapper that does caching? ?

then, wrapper that does copy-across based on loop

then, superclass that does copy-across?


