
==================
 Prebound Methods
==================


.. to find examples:
   ag --ignore site-packages '^[a-z_]+ = [a-z_]+\.[a-z_]+$' /usr/lib/python3.6

There are occasions on which a Python module
wants to offer a collection of routines
in the module’s global namespace
which will need to share state with each other at runtime.

Probably the most famous example
is the `random`_ module from the Python Standard Library.
It does provide advanced users
with the option of creating their own
random number generator instances.
But everyone else can simply call
a slate of routines at the top level of the module —
`randrange <https://docs.python.org/3/library/random.html#random.randrange>`_,
`randint <https://docs.python.org/3/library/random.html#random.randint>`_,
`choice <https://docs.python.org/3/library/random.html#random.choice>`_,
and so forth —
that mirror the methods of a ``Random`` object.

How do these top-level routines share state?
Behind the scenes these callables are, in fact, methods
that have all been prebound
to a single instance of ``Random``
that the module constructs ahead of time.

.. _random: https://docs.python.org/3/library/random.html

After investigating a few other alternatives to this problem,
we will see how this pattern looks in Python code.

Alternatives
============

The most primitive approach
to sharing state between a pair of module-level callables
is to write a pair of functions
that manipulate data that is also stored at the top level of the module.

Imagine that we want to offer a simple random number generator.
It returns, in an endless loop,
the numbers between 1 and 255 in a fixed pseudo-random order.
We also want to offer a simple routine
for resetting the state of the generator —
which is important both for writing tests that use random numbers
as well as reproducing simulation output
that’s driven by pseudo-randomness.
If Python only allowed us to write plain functions,
then we might store the shared seed
as a module global name
that our functions would directly access and modify:

.. literalinclude:: random8_with_globals.py
   :lines: 1-14

There are several problems with this approach.

First, it is impossible to ever instantiate
a second copy of this random number generator.
If two threads each wanted their own copy of the generator
to avoid needing to protect it with locks,
then they are out of luck.

(By “out of luck” I don’t mean “impossible” —
this, after all, is Python, the famous dynamic language.
Think of the possibilities.
You could import the module,
rename it in ``sys.modules``,
and then import it again to get a second copy.
Or you could manually instantiate a second module object
and copy all three names across.
I simply mean that you would be out of luck
if you have any sense of Pythonic decorum.)

Second, it is more difficult to decouple
your random number generator tests from each other
if its state is global.
Instead of each test creating its own instance,
the tests will all have to share the single pair of global functions
and hope that they are correctly resetting its state
to achieve isolation for the next test.

Third, this approach abandons encapsulation.
This will sound like a fuzzier complaint
then the previous two,
but it can offend readability
(“readability counts”)
for a tight small system of two functions and a ``seed``
to be splayed out as three separate names
in a module which might contain dozens of other objects.

To solve the above problems, we create a Python class,
and thereby exercise that greatest and most magnificent of all design patterns:
the Facade.
The two routines and their state
will live happily bundled together:

.. literalinclude:: random8_with_globals.py
   :lines: 1-14

The software engineer would do well to stop at this moment,
pause for breath,
and to think quite seriously
about the fact that in the vast majority of cases
simply defining the class is enough.

Is the convenience to your users of instantiating the class for them —
saving them one line of code, in this example —
really going to be such a profound convenience
that it is worth doing?
You are creating an object without asking their permission
and without any possibility of knowing their particular circumstances.
You are going to do it on their behalf
on the mere chance that they will use it.
TODO
Remember that if your user does need does require
that there be only one instance of your class in play
they can instantiated them self at the top level of one of their own modules
it only after all takes a single line of color
you will be saved the inconvenience of having to build the object
and users who need to create and control their own object instances
won't be charged the expense
of the global object you instantiate and that they must ignore

if i a clear wint is clear as in the case of the random module
for your users to be able to share a single common instance of your class
thenThe next alternative 
Would be to instantiate sing-along picked for them a single object for them
end store it under a well-documented
at left in the global namespace of your module
the few users who might still need to instantiate one of the objects of Their Own
will be free to do so by instantiating class
but everyone else will be able to import your module
and the the default instance that you provide

but many programmers but
cannot resist the Apex of convenience
providing module level color apples
that are is easy to call as functions
but that share State like the methods of a class
you can have heartedly provide rapper functions
that each turn around and invoke a method of the same name
All

on your default object

Exit

cut that approach but that approach
is both for both and more expensive
then it's more pythonic alternative prebound methods

The pattern
===========

To offer your users Prebound Methods,
instantiate your class
and assign that instance to a name in the global namespace of your module —
usually to a private name
that does not invite users to meddle with the object directly.

Then,
assign each of the object’s methods
to the same name out in the module’s global namespace
For the random number generator that we used as an illustration above,
the entire module might look like this:

.. literalinclude:: random8_with_globals.py
   :lines: 1-19

Users will now be able to invoke each method
as though it were a stand-alone function.
But the methods will all be secretly sharing state
thanks to the common instance that they are bound to,
without requiring the user to instantiate the class
and keep up with an explicit instance of their own.

When exercising this pattern,
please be responsible about the dangers
of instantiating an object at import time.
This pattern is usually not appropriate
for a classes that create files, read database configurations,
open sockets,
or in general that inflict side effects on the program importing them.
In that case you will need a more complicated scheme:
defer any actual setup
until the first of your methods is called.
You could even provide a ``setup()`` method
and require application programmers to invoke it
before they can expect any of the other routines to work.

But for lightweight objects
that need no prior configuration before being instantiated,
and that make sense to build once,
Prebound Methods are a very elegant way
to make the stateful behavior of a class instance
available up at a global module level.

The result can have great benefit.
Think of the expense if every module that used the `random`_ module
had to create its own ``Random`` instance,
each of which might have to go pull bits
from all across the operating system
to seed their generator.

cut examples here

One final hint:
it is almost always better
to assign methods to global names explicitly.
Even if there are a 12 methods,
I recommend going ahead and writing
a quick stack of 12 assignment statements
aligned against the left-hand column of your module.
Python is a dynamic language,
which might tempt you to automate the series of assignments instead
using attribute introspection and a ``for`` loop.
I advise against it.
Python programmers believe that “Explicit is better than implicit” —
and materializing the stack of names as real code
supports readers, debuggers, and that essential tool ``grep``.





problem
module wants to offer routines which share state

random module
takes a little effort to set up

no problem sharing state
more efficient to

“mirror”

.. Decoys

   this is NOT open = TarFile.open
   because that’s not an instance

   nor offering configurability by 63:default_timer = time.perf_counter
   in timeit

   note that this is not object creation like in dumps/loads


Alternatives

functions that manipulate global state

show example

terrible, can’t test, can’t have several

so create object

you can just offer object as a facade and let user instantiate it
but, cost: have to keep initializing and doing random seed

or have object sitting at top level / so create an object at the top level
but adds an extra level of verbosity

pass-through functions

    def random():
        return _instance.random()

more expensive

The Pattern

show the whole module

the class

then create a method

finally bind each method and assign it a global name

And always be explicit! Not implicit or loops. If you can help it.

random


calendar.py:
c = TextCalendar()
...
week = c.formatweek
weekheader = c.formatweekheader
...

distutils/log.py:
_global_log = Log()
log = _global_log.log
debug = _global_log.debug
info = _global_log.info
warn = _global_log.warn
error = _global_log.error
fatal = _global_log.fatal

_forkserver = ForkServer()
ensure_running = _forkserver.ensure_running
get_inherited_fds = _forkserver.get_inherited_fds
connect_to_new_process = _forkserver.connect_to_new_process
set_forkserver_preload = _forkserver.set_forkserver_preload

secrets.py
_sysrand = SystemRandom()
randbits = _sysrand.getrandbits
choice = _sysrand.choice

reprlib.py:
aRepr = Repr()
repr = aRepr.repr

multiprocessing/semaphore_tracker.py
_semaphore_tracker = SemaphoreTracker()
ensure_running = _semaphore_tracker.ensure_running
register = _semaphore_tracker.register
unregister = _semaphore_tracker.unregister
getfd = _semaphore_tracker.getfd


hint: keep names the same


