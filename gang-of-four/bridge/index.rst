
====================
 The Bridge Pattern
====================

.. todo make sure I say complicated not complex

*A “Structural Pattern” from the* :doc:`/gang-of-four/index`

.. admonition:: Verdict

   The Bridge Pattern helps improve the design of Python classes
   that might otherwise need tricks like multiple inheritance and mixins.
   Instead of a single complicated class
   that couples several behaviors together,
   the Bridge Pattern recommends
   that simpler classes be composed together
   to perform the same task.

A class that was intended to be simple can, in practice,
wind up getting extended in several different directions
over the course of its career.
If the class varies in _m_ different ways along one axis of design
and _n_ ways along another,
then in the worst case a system might need _m×n_ variants of the class.

The Gang of Four offer the example of a ``Window`` class
that has been extended to support two different operating systems —
imagine that there are subclasses ``MSWindow`` and ``MacWindow``.
What happens when a designer now wants to create a special window
for supporting a grid of icons?
They will need to create both an ``MSIconWindow`` and a ``MacIconWindow``.
The _m_=2 possible operating systems (Microsoft and Windows)
have combined with _n_=2 possible behaviors (“plain” and “icon”)
to produce 2×2=4 classes.

The Bridge Pattern recommends splitting a complicated class
into several simple classes,
each of which implements one of the possible axes of design.
In their example,
an outer ``Window`` or ``IconWindow`` class
that is purely concerned with layout
can wrap an inner ``MSWindowDriver`` or ``MacWindowDriver`` class
that’s concerned with operating under a specific operating system.
The system winds up with _m+n_ instead of _m×n_ separate classes.

As we will see,
this Bridge Pattern not only works well in Python,
but can replace two Python habits
that were not widespread in the Gang of Four’s original languages:
multiple inheritance, and mixins.






object oriented folks will have seen situations
where a single class needs to be specialized
along many different axes at once
symptom: classes with long names
in example below, ``FilteredFileLogger``

the bridge pattern
recommends decomposing a complicated class
into several classes,
with a more abstract outer class
holding a reference to an implementation in an inner class

Unwitting Superclasses
======================

An overly simplistic example can drive our discussion.
Imagine a naive ``Logger`` class
that provides a basic interface for issuing log messages
and invites the programmer to specialize it:

.. testcode::

    import sys

    class Logger(object):
        def log(self, level, message):
            print(level, message, file=sys.stderr)

A large software project might accumulate several subclasses.

The two subclasses might live in different parts of the codebase
without either programmer knowing about the other’s work.
But they raise the obvious question:
can the two subclasses be composed together
so as to combine their features?

No; in the general case, they cannot.

One problem is that Python initialization methods


But the initialization problem could conceivably be eliminated
if we stopped competing for control
of the ``__init__()`` method’s parameters
and devolved configuration on to a more flexible mechanism,
like a dictionary.

Much more serious is the problem
that the application logic itself —
the filtering and presentation of logging messages —
cannot compose.
The author of the ``FilterLogger``
did their best to cooperate with the superclass,
dutifully calling ``super()`` to have the superclass
do the actual printing.
But the author of the ``FileLogger``,
whatever their good intentions might have been,
had to re-implement the output step
because the superclass failed to anticipate
that someone might want to customize the file passed to ``print()``.

While this particular oversight does look silly,
our small example is demonstrating a very common problem
in more complex libraries:
it is surprising how often the original library author
will not have anticipated the direction
in which you —
working on a problem they had not even imagined —
need to specialize their class.

By accident,
it turns out
that these two subclasses will compose just fine
if we reverse their order!

INSTEAD

.. testcode::

    # One developer specialized the idea of a Logger:

    class FilterLogger(Logger):
        """Configure with log.threshold = <value>."""
        threshold = 30

        def log(self, level, message):
            if level >= threshold:
                super().log(level, message)

    # Somewhere else, another developer defined:

    class FileLogger(Logger):
        """Configure with log.file = <file object>."""
        file = sys.stderr

        def log(self, level, message):
            print(level, message, file=self.file)

this is the very best case

1. configuration not through __init__()

2. remembered to call super()

3. because order is important, it’s happy that Python MROs have order

Calling the ``log()`` method of the combined class
will first call the ``FilterLogger`` version of the routine,
which performs the filtering.
Then its call to ``super()``
will find the ``FileLogger`` next in the method resolution order,
whose behavior will properly override that of the superclass.

But our ability here
to pull out a success is both unlikely in the general case,
and fragile.
Software should in general not depend on something as fragile
as the order in which subclasses have been listed.

(In a language without multiple inheritance,
these subclasses would obviously not compose in any case.)


can we do both?
no!
neither subclass defers to parent
if we want a FilteredFileLogger
there is no way to get there from FileLogger
because it hard-codes sys.stderr

we will have to build it atop the FileLogger
by copying the threshold test

.. testcode::

    class FilteredFileLogger(FilterLogger, FileLogger):
        """Subclass that combines superclass abilities."""

note the naming order
put filtered first to remember both the order of operations
and also the order of parameters during instantiation

in general code reuse is difficult
we have had to re-implement filtering
in a new subclass

Anticipated subclasses
======================

you can design a class
with specialization in mind
like

.. testcode::

    class BaseLogger(object):
        def log(self, level, message):
            if self.filter(level, message):
                self.emit(level, message)

        def filter(self, level, message):
            return True

        def emit(self, level, message):
            print(level, message, file=sys.stderr)

we could now do stuff without as much problem
we wouldn’t have to worry about order of subclasses?
hmm

    class FilterLogger(BaseLogger):
        """Configure with log.threshold = <value>."""
        threshold = 30

        def filter(self, level, message):
            return level >= threshold

    class FileLogger(BaseLogger):
        """Configure with log.file = <file object>."""
        file = sys.stderr

        def emit(self, level, message):
            print(level, message, file=self.file)

Thanks to the superclass’s careful design,
these subclasses are clean and orthogonal,
each customizing a different method of the parent class.
Multiple inheritance can safely mix them together in any order.

    class FilterFileLogger(FileLogger, FilterLogger):
        """Subclass that combines superclass abilities."""

But this success is fragile.
how?

mixins
======

how to discuss?

why have

instead

    class FilterMixin(object):
        threshold = 30

        def filter(self, level, message):
            return level >= threshold

    class FileMixin(object):
        file = sys.stderr

        def emit(self, level, message):
            print(level, message, file=self.file)



    class FilterFileLogger(FileMixin, FilterMixin, BaseLogger):
        """Subclass that combines superclass abilities."""

in general a mixin is a symptom of the same thing:
multiple axes of design
have been coupled into a single class

the Bridge Pattern
==================

instead of coupling two different kinds of behavior in the same class,
the bridge pattern
splits each behavior into a separate class.
callers are expected to interact with
abstraction and implementation

in g4 did something else:
prevented client code from... really?

.. testcode::

    class Logger(object):
        def __init__(self, handler):
            self.handler = handler

        def log(self, level, message):
            self.handler(level, message)

    class Handler(object):
        def log(self, level, message):
            print(level, message, file=sys.stderr)

The two axes along which we want to customize class behavior —
whether a particular message is logged at all,
and where the message is written —
are now independent.
so two subclasses

.. testcode::

    class FilterLogger(object):
        def __init__(self, handler, level):
            self.level = level
            super().__init__()

        def log(self, level, message):
            if level >= foo:
                super().log(level, message)

    class FileHandler(object):
        def __init__(self, file):
            self.file = file
            super().__init__()

        def log(self, level, message):
            print(level, message, file=self.file)

first we have only simple subclassing
so super() you know which class it calls

second we have avoided __init__ problem
because each class builds atop a single base class,
(hmm, am I right? is this so much better?)

another in C++: not binding abstr to impl

.. testcode::

    logfile = open('/tmp/app.log', 'a')
    log = FilterLogger(FileHandler(logfile), 30)

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

== multiple inheritance works poorly
if the stack of methods have different arguments

== we can think of ways around: instead of __init__ methods,
have set_file() and set_level() methods
that are called after instantiation

all the problems are solved

- no multiple inheritance

- therefore, init becomes safe again
  each class knows its superclass
  it can declare init that extends the superclass’s list of arguments
  with the additional arguments it needs
  and safely call super() init



no longer have to build new classes
can just plug things together at runtime



actual logging module more complicated

- expects subclasses, in fact requires it
  because handler offers but does not implement emit()
  several pre-made Handler classes

- makes the Handler complicated
  because not only does each Logger have its own stack of filters
  but each Handler can have a second stack of filters
  that get applied before it calls its own emit()
  so the logging module Handler
  is more like the Logger we defined above

- in another application of the Builder,
  separates out formatting into its own class as well



vvvvv keep this example of using actual?

..  from logging import getLogger
    import logging

    log = getLogger('example')

    class FileHandler(logging.Handler):
        def __init__(self, file):
            self.file = file
            super().__init__()

        def emit(self, record):
            print(self.file)
            print(repr(record))
            print(repr(record), file=self.file)

    fh = FileHandler(open('/tmp/log.txt', 'w'))
    log.addHandler(fh)
    log.error('Warning!')



not using classes
=================

would it be simpler not to use classes

with Thread the original mechanism has all but
very few projects choose to subclass Thread any more
and instead provide a callable

why not do that with logging?

.. testcode::

    def make_filter(threshold):
        def filter(level, message):
            for level, message in messages:
                if level < messages:
                    yield level, message
        return filter



answer: introspection



logging_tree

if logging wanted a less heavyweight approach
could move to duck typing


why not just have a huge class with lots of methods
and lots of abilities and configure it for each situation?

creating classes dynamically
============================

“when the implementation must be selected or switched at run-time.”

you would have to create, ahead of time,
each combination of classes
because you can’t define new subclasses at runtime

..
   2^n

   except that you can, because this is Python

   type(classname, superclasses, attributes_dict)

   checkboxes = [
       ('Filter?', FilterMixin),
       ('File?', FileMixin),
   ]

   answers = [True, False]

   superclasses = [BaseLogger]

   for answer, (name, mixin) in zip(answers, checkboxes):
       if answer:
           superclasses.append(mixin)

   new_class = type('DynamicLogger', superclasses, {})
