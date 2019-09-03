
====================
 The Bridge Pattern
====================

*A “Structural Pattern” from the* :doc:`/gang-of-four/index`

.. admonition:: Verdict

   The Bridge Pattern solves the problem
   :
   instead of coupling

Uncooperative Subclasses
========================

Some early experiments in object orientation
imagined that a primary purpose of software libraries
would be to provide useful superclasses,
whose code we would re-use
by subclassing them.

An overly simplistic example can drive our discussion.
Imagine a logging library
that provides a ``Logger`` superclass
and invites programmers to specialize it:

.. testcode::

    class Logger(object):
        def log(self, level, message):
            print(level, message, file=sys.stderr)

A large software project might accumulate several subclasses.

.. testcode::

    class FilteredLogger(Logger):
        def __init__(self, threshold):
            self.threshold = threshold

        def log(self, level, message):
            if level >= threshold:
                super().log(level, message)
                # , file=sys.stderr)

    class FileLogger(Logger):
        def __init__(self, file):
            self.file = file

        def log(self, level, message):
            print(level, message, file=self.file)

The two subclasses might live in different parts of the codebase
without either programmer knowing about the other’s work.
But they raise the obvious question:
can the two subclasses be composed together
so as to combine their features?

No, in the general case they cannot.

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
The author of the ``FilteredLogger``
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

    class FilteredFileLogger(FilteredLogger, FileLogger):
        def __init__(self, level, file):
            # Cheat, since __init__() does not compose:
            self.level = level
            self.file = file

Calling the ``log()`` method of the combined class
will first call the ``FilteredLogger`` version of the routine,
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

    class FilteredFileLogger(FileLogger):
        def __init__(self, level, file):
            self.level = level
            super().__init__(file)

        def log(self, level, message):
            if level >= threshold:
                super().log(level, message)

note the naming order
put filtered first to remember both the order of operations
and also the order of parameters during instantiation

in general code reuse is difficult
we have had to re-implement filtering
in a new subclass

Cooperative Subclasses
======================



    class FilteredLogger2(Logger):
        def __init__(self, threshold):
            self.threshold = threshold

        def log(self, level, message):
            if level >= threshold:
                super().log(level, message)

here subclass has anticipated composition

    class 

note that this would have been a disaster
if either subclass __init__ had called super().__init__()
because they would have tried calling their fellow subclass

so in general you have to stop using init
and instead have a separate method
to initialize each attribute

Cooperative Subclasses
======================

you can design a class
with specialization in mind
like

.. testcode::

    class BaseLogger(object):
        def log(self, level, message):
            level, message = self.filter(message)
            self.emit(level, message)

        def emit(self, level, message):
            print(level, message, file=sys.stderr)

we could now do stuff without as much problem
we wouldn’t have to worry about order of subclasses?
hmm

you would have to create, ahead of time,
each combination of classes
because you can’t define new subclasses at runtime

2^n

except that you can, because this is Python

creating classes dynamically
============================

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



the Bridge Pattern
==================


.. testcode::

    class Logger(object):
        def __init__(self, handler):
            self.handler = handler

        def log(self, level, message):
            self.handler(level, message)

    class Handler(object):
        def log(self, level, message):
            self.handler(level, message)

now subclass independently

.. testcode::

    class FilteredLogger(object):
        def __init__(self, handler, level):
            self.level = level
            super().__init__(level)

        def log(self, level, message):
            if level >= foo:
                super().log(level, message)

    class FileHandler(object):
        def __init__(self, file):
            self.file = file
            super().__init__()

        def log(self, level, message):
            super considered super

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

.. testcode::

    from logging import getLogger
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


