
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

1. Literal wrappers
===================

First, let’s learn the drudgery
of creating the kind of decorator class you would write in C++ or Java.
We will not take advantage of the fact
that Python is a dynamic language,
but will give the wrapper a simple static definition
of every method and attribute that exists on a Python file object.

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

.. literalinclude:: verbose_static_wrapper.py

So for the sake of the half-dozen lines of code at the bottom
that supplement the behavior of ``write()`` and ``writelines()``,
another hundred or so lines of code are necessary in this case.

You will notice that each Python object attribute
goads us into being even more verbose than Java!
A typical Java attribute is implemented as exactly two methods,
like ``getEncoding()`` and ``setEncoding()``.
A Python attribute, on the other hand,
will in the general case need to be backed by *three* actions —
get, set, and delete —
because Python’s object model is dynamic
and supports the idea that an attribute might disappear from an instance.

Of course,
if the class you are decorating
does not have as many methods and attributes
as the Python file object we took as our example,
then your wrapper will be shorter.
But in the general case,
writing out a full wrapper class will be tedious
unless you have a tool like an IDE that can automate the process.
Also, the wrapper will need to be updated in the future
if the underlying object gains (or loses)
any methods, arguments, or attributes.

1.1. Tactical wrappers
======================

The wrapper in the previous section
might have struck you as ridiculous.
It tackled the Python file object as a general example
of a class that needed to be wrapped,
instead of studying the how file objects work to look for shortcuts:

* File objects are implemented in the C language and do not,
  in fact, permit deletion of any of their attributes.
  So our wrapper could have omitted all 6 deleter methods
  without any consequence, since the default behavior of a property
  in the absence of a deleter is to disallow deletion anyway.
  This would have saved 18 lines of code.

* All file attributes except ``mode`` are read-only
  and raise an ``AttributeError`` if assigned to —
  which is the behavior if a property lacks a setter method.
  So 5 of our 6 setters can be omitted, saving 15 more lines of code
  and bringing our wrapper to ⅓ its original length
  without sacrificing correctness.

It might also have occurred to you
that the code to which you are passing the wrapper
is unlikely call every single file method that exists.
What if it only calls two methods?
Or only one?
In many cases a programmer has found
that a trivial wrapper like this
will perfectly satisfy real-world code
that just wants to write to a file!

.. literalinclude:: tactical_wrapper.py

Yes, this can admittedly be a bit dangerous.
A routine that seems so happy with a minimal wrapper like this
can suddenly fail later
if rare circumstances
make it dig into class features
that you never happened to observe it using.
Even if you audit the library’s code
and are sure it can never call any method besides ``write()``,
that could change
the next time you upgrade the library to a new version.

In a more formal programming language,
a duck typing requirement like “this function requires a file object”
would likely be replaced with an exact specification like
“this argument needs to support a ``writelines()`` method”
or “pass an object
that offers every methods in the interface ``IWritableFile``.”
But most Python code lacks this precision
and will force you, as the author of a wrapper class,
to decide where to draw the line
between the magnificent pedantry of wrapping every possible method
and the danger of not wrapping enough.

1.2. Note that wrapping doesn’t actually work
=============================================



Approach 2: A dynamic wrapper
=============================



then, wrapper that does dynamic getattr
(explain why you would use getattribute?)

Trick 2a: 

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



