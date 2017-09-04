

=======================
 The Decorator Pattern
=======================



The Python core developers made the terminology
surrounding this design pattern more confusing than necessary
by using the *decorator* for an entirely unrelated language feature.
The timeline went something like this:

* The design pattern was developed and named in the early 1990s
  by participants in the “Architecture Handbook” series of workshops
  that were kicked off at OOPSLA ’90,
  a conference for researchers of object-oriented programming languages.

* The design pattern became famous
  under the name “the Decorator Pattern”
  with the 1994 publication
  of the Gang of Four’s *Design Patterns* book.

* In 2003, the Python core developers
  decided to re-used the term *decorator*
  for a completely unrelated feature they were adding to Python 2.4.
  Partly to blame may be the fact that Python’s open and dynamic design
  allowed many programmers be productive
  without any conscious use of design patterns,
  making a collision with object-oriented design terminology
  seem irrelevant.



is confusing terminology
because the Python core developers in 



Note that this pattern
is not related to Python function decorators or class decorators!
It is merely a coincidence
that the Gang of Four happened to use the same word *decorator*
for this design pattern
that the Python community used for its concept.


In static languages,
using the decorator pattern can be arduous:
your wrapper has to implement every single method
of the target class,
with exactly the same arguments and defaults,
and each method has to turn around and call the real method
on the target object.

The pattern can be easier in Python:

* You can implement `__getattr__()`.
* You can build a class with wrappers.
  (Is this what `patch` does?)


first, full wrapper


`verbose_static_wrapper.py <verbose_static_wrapper.py>`_


would be mitigated by interface


.. literalinclude:: verbose_static_wrapper.py

then, wrapper that does dynamic getattr
(explain why you would use getattribute?)

then, wrapper that does copy-across of method in __init__

? then, wrapper that does caching? ?

then, wrapper that does copy-across based on loop

then, superclass that does copy-across?


