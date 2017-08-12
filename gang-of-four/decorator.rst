

=======================
 The Decorator Pattern
=======================



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

then, wrapper that does copy-across of method in __init__

then, wrapper that does dynamic getattr
(explain why you would use getattribute?)

? then, wrapper that does caching? ?


