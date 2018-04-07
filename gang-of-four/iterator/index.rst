
==================
 Iterator Pattern
==================

Verdict

Python has embraced the Iterator Pattern
at the most fundamental level available to a programming language:
it’s built into Python’s syntax.


The least expressive computer languages
make no attempt to hide the inner workings of their data structures.
In those languages,
if you want to visit every element in an array,
you have to generate the integer indexes yourself.

Code in such languages struggles to stay at the high level
of describing programmer intent.
Instead, the flow of each thought
gets interrupted with low-level details about data structures.
When code can’t abstract away the mechanics of iteration,
it becomes more difficult to read;
it’s more liable to errors,
because the same iteration logic needs to be repeated over and over;
and no improvements can be made to a data structure
that change its iteration strategy
without finding and changing every place in the code
where that data structure is iterated across.

The remedy is encapsulation.
The Iterator Pattern explains that you should move
the details about how a data structure is traversed
into an “iterator” object that,
from the outside,
simply yields one item after another
without exposing the internals of how the data structure is traversed.

Iterating with the “for” loop
=============================

Python’s ``for`` loop
abstracts the Iterator Pattern so thoroughly
that most Python programmers are never aware
of the object design pattern that it enacts beneath the surface.
The loop performs repeated assignment,
repeating its indented block of code
once for each item in the sequence it is iterating over.

.. testcode::

   some_primes = [2, 3, 5]
   for prime in some_primes:
       print(prime)

.. testoutput::

   2
   3
   5

The loop above has performed a series of three assignment statements
``prime = 2``, ``prime = 3``, and ``prime = 5``,
running the indented block of code after each assignment.
The block can include the C-style loop control statements
``break`` to leave the loop early
and ``continue`` to skip back to the top of the loop
and move on to the next item.

Because ``for`` is a repeated assignment statement,
it has the same flexibility as Python’s normal ``=`` assignment operator:
by listing several names separated by commas,
you can upgrade from assigning a single name to unpacking a tuple.
This lets you skip a separate unpacking step.

.. testcode::

   elements = [('H', 1.008), ('He', 4.003), ('Li', 6.94)]

   # You don’t need to assign to "tup" first
   for tup in elements:
       symbol, weight = tup
       print(symbol, weight)

   # Instead, unpack right inside the "for" statement
   for symbol, weight in elements:
       print(symbol, weight)

.. testoutput::
   :hide:

   H 1.008
   He 4.003
   Li 6.94
   H 1.008
   He 4.003
   Li 6.94

Famously, this can be coupled with the Python dictionary’s ``item()`` method
to easily visit each key along with its value
without the expense of any key lookups.

.. testcode::

   d = {'H': 1.008, 'He': 4.003, 'Li': 6.94}

   # You don’t need to:
   for symbol in d.keys():
       weight = d[symbol]
       print(symbol, weight)

   # Instead, you can:
   for symbol, weight in d.items():
       print(symbol, weight)

.. testoutput::
   :hide:

   H 1.008
   He 4.003
   Li 6.94
   H 1.008
   He 4.003
   Li 6.94

The ``for`` loop combines such admirable concision and expressiveness
that Python not only supports it as a stand-alone statement,
but has incorporated it into four different expressions —
Python’s famous “comprehensions” that build lists, sets, dictionaries,
and iterators directly from inline loops:

.. testcode::

   [symbol for symbol, weight in d.items() if weight > 5]
   {symbol for symbol, weight in d.items() if weight > 5}
   {symbol: weight for symbol, weight in d.items() if weight > 5}
   list(symbol for symbol, weight in d.items() if weight > 5)

Python’s choice to re-use the ``for`` statement syntax
for iteration inside of expressions
instead of inventing a separate iteration expression syntax
makes the language simpler, easier to learn, and easier to remember.

The pattern: the iterable and its iterator
==========================================

The traditional Iterator Pattern involves three kinds of object.

First, there’s a *container* object.

Second, the container’s internal logic
lets it corral and organize a number of *item* objects.

Finally, there’s the key to the pattern:
instead of the container supplying its users
with special container-specific instructions
for how to access its items —
which would force the programmer to learn
a different approach for every container their code uses —
it offers access to its items
through a generic mechanism
that works the same across many different kinds of container.

Python provides a pair of builtins
that let you step behind the ``for`` loop
and pull the levers of iteration yourself.

* ``iter()`` asks the container object
  to build and return a new iterator object.
  (If the argument you pass isn’t actually a container,
  a ``TypeError`` is raised: ``object is not iterable``.)

* ``next()`` takes the iterator as its argument and,
  when called repeatedly,
  returns each of the item objects
  that would be visited by a ``for`` loop over the container.
  Each call to ``next()`` returns one object.
  Once the container is exhausted and there are no more objects to return,
  a special exception ``StopIteration`` is raised.

To reenact the first ``for`` loop
that we studied in the previous section,
we would make a single call to ``iter()``
followed by four calls to ``next()``:

.. testcode::

   >>> it = iter(some_primes)
   >>> it
   >>> print(next(it))
   >>> print(next(it))
   >>> print(next(it))
   >>> print(next(it))

.. testoutput::

   foof

These are precisely the actions
taken by Python’s ``for`` loop,
though it works a bit differently.
The ``for`` loop doesn’t check ahead of time
how many items there are in the container —
because some iterables simply don’t know ahead of time
how many items they’ll yield,
as when you are iterating over the lines of a file.
So it can’t plan ahead,
as I did when writing the above example code,
and call ``next()`` exactly four times.

Instead, ``for`` is implemented as a ``while`` loop — something like:

.. testcode::

   it = iter(some_primes)
   while True:
       try:
           print(next(it))
       except StopIteration:
           break

.. testoutput::

   foof

My big question when first encountering the Iterator Pattern was:
why does the iterator need to be a separate object
from the iterable container object itself?
Why can’t each container simply include a counter inside
that reminds it which object to yield next?

The answer is that,
while a single internal counter would work fine
as long as only one ``for`` loop at a time
were ever iterating over a container,
there are many situations where several ``for`` loops
are working on the same container at once.
To generate all combinations of two coin flips, for example,
the programmer might quite naturally write concentric loops:

.. testcode::

   sides = [‘heads’, ‘tails’]
   for coin1 in sides:
       for coin2 in sides:
           print(coin1, coin2)

.. testoutput::

   foof

If the Python list object ``sides``
had tried to support iteration using only a single internal counter,
then the inner ``for`` loop would have used up all of the items
and left the outer ``for`` loop without any further items to visit.

And multiple threads of control,
whether operating system threads or coroutines,
also offer plenty of circumstances
under which an object might be operated on
by several ``for`` loops at the same time.

>>> iter(some_primes)
>>> iter(elements)

We have now seen the behavior of an iterable and its iterator.
But what’s the object protocol behind the scenes
that lets objects support Pythonic iteration,
whether it’s enacted with ``for`` or with ``iter()`` and ``next()``?
We’ll tackle it soon — but first,
let’s study a variation of the traditional Iterator Pattern
that will help us understand the full set of requirements
placed on iterator objects.

Python’s twist: objects which are their own iterator
====================================================


which wasn’t possible because of no inheritance?

wasn’t possible because of combination of:

no interfaces, can only interchange objects if they inherit from a common
implementation.

no multiple inheritance.

(is that true? or does C++ support multiple inheritance?)

Iterator objects and “iter()”
=============================

To understand the Iterator Pattern behind the ``for`` loop,
we need to distinguish between two different kinds of object:
an *iterable* whose items can be visited,
and an *iterator* that keeps track of where we’re at
as we visit those items.
To see the difference,
we’ll compare iteration over a file object
with iteration over a Python list.
Let’s consider the file object first.

The Python file object is designed to yield lines
when you iterate across it with a ``for`` loop.
If you stop iterating early,
the remaining lines will still be waiting
for the next time you loop over the file.
This feature can be used
to loop over a file in phases.

We can motivate a simple example
by considering a traditional UNIX mailbox file:

.. literalinclude:: email.txt

This file needs to be parsed in three phases
because each section is delimited by its own rules.
The initial “envelope line” that starts with the word ``From``
is guaranteed to be a single standalone line.
Each line of the header that follows
contains a name, ``:``, and a value,
with the header itself finishing with a single blank line.
The body, which comes last,
ends at either the next envelope ``From`` line
or else the end of the file.
Here’s how we might parse the first message from a mailbox file:

.. testsetup::

   import os
   os.chdir('gang-of-four/iterator')

.. testcode::

   def parse_email(f):
       for line in f:
           envelope = line
           break
       headers = {}
       for line in f:
           if line == '\n':
               break
           name, value = line.rstrip('\n').split(':', 1)
           headers[name.strip()] = value.lstrip()
       body = []
       for line in f:
           if line.startswith('From'):
               break
           body.append(line)
       return envelope, headers, body

This convenient pattern —
in which we tackle each section of the file with its own ``for`` loop —
is possible because each time we start up another loop,
the file object continues reading from right where we left off.
The above function works perfectly when passed a Python file object:

.. testcode::

   with open('email.txt') as f:
       envelope, headers, body = parse_email(f)

   print(headers['To'])
   print(len(body), 'lines')

.. testoutput::

   Mary Smith <mary@example.net>
   2 lines

Python programmers whose early experiences with iteration
all involve file objects
might expect every Python iterable to behave in the same way —
they might expect iteration to always pick up
exactly where it left off,
if a previous ``for`` loop ended early with ``break``.

But, alas, this pattern shatters
the very first time the programmer
tries iterating over a native Python container.
Let’s run the same code over the same mailbox file,
but this time read the lines of the file into a Python list first:

.. testcode::

   with open('email.txt') as f:
       lines = list(f)

   envelope, headers, body = parse_email(lines)
   print(headers['To'])
   print(len(body), 'lines')

.. testoutput::

   Mary Smith <mary@example.net>
   0 lines

Wait — zero lines?
The body of the message is now empty?

.. testcode::

   print(body)

.. testoutput::

   []

The body is empty!
What’s gone wrong?

To see the problem,
let’s write a pair of ``for`` loops
that print exactly which strings they see as they iterate across a list.

.. testcode::

   states = ['Alabama', 'Alaska', 'Arizona']

   # First, we consume a single line.
   print('Loop #1:')
   for s in states:
       print(s)
       break

   # Then we do a complete loop across the items.
   print('Loop #2:')
   for s in states:
       print(s)

.. testoutput::

    Loop #1:
    Alabama
    Loop #2:
    Alabama
    Alaska
    Arizona

You can see that once the first ``for`` loop exited with ``break``,
we lost our place in the list —
the second ``for`` loop started all over again with the first string ``"one"``.
How can the Python list object choose
to make each iteration across it independent of the last,
and the file object choose iterations to be linked?

The answer is that the ``for`` loop
relies entirely on each iterable object’s class
to define what iteration means.
Each time ``for`` starts up,
it asks the object for  —
through a mechanism we'll learn later —


Each class makes its own decision
about whether several different ``for`` loops over the same object
will share state,
or else each start over with the iterable's first item.

The Python list 

.. testcode::

   i1 = iter(states)
   i2 = iter(states)
   print(i1)
   print(i2)

.. testoutput::
    :hide:

    <list_iterator object at 0x...>
    <list_iterator object at 0x...>

::

    <list_iterator object at 0x7f09ced444a8>
    <list_iterator object at 0x7f09ced343c8>



Implementing an Iterable and Iterator
=====================================

The Iterator Pattern dictates
that a loop visiting successive items in a container
must vow to never touch the actual container object —
must never get involved with the details, whether simple or intricate,
of how the container enumerates or addresses or arranges its contents.
Instead, the container should offer consumers
an “iterator” object that knows all the secrets
of how to address items in the container and traverse across them.

Python requires that a uniform protocol be implemented by all objects
that want to participate in Python iteration.

* Containers must offer an ``__iter__()`` method.
  It should return an iterator.
  Supporting this method makes a container “able to be iterated over”
  = “iterable.”

* So, what’s an iterator?
  It’s any object that offers a ``__next__()`` method
  that returns another item from the container each time it’s called.
  It raises ``StopIterator`` when there are no further items.
  (In old Python 2 code, the spelling is ``next()`` without the dunder.)

There’s another requirement of iterators,
but we’ll reveal it later
(scroll down looking for a lone bullet point if you’re in a hurry)
once we’ve provided a motivation.

There is no requirement that the items yielded by ``__next__()``
be stored as persistent values inside the container.
This lets us offer a very simple Iterator Pattern example
without even implementing storage in the container:

.. testcode::

   class OddNumbers(object):
       "An iterable object."

       def __init__(self, maximum):
           self.maximum = maximum

       def __iter__(self):
           return OddIterator(self)

   class OddIterator(object):
       "Very nearly an iterator (see next example)."

       def __init__(self, container):
           self.container = container
           self.n = -1

       def __next__(self):
           self.n += 2
           if self.n >= self.container.maximum:
               raise StopIteration
           return self.n

With these simple methods,
these objects are now eligible for full membership
in Python’s rich iteration ecosystem.

.. testcode::

   numbers = OddNumbers(7)

   for n in numbers:
       print(n)

These objects can even dance with the comprehensions.

.. testcode::

   print(list(numbers))
   print(set(n for n in numbers if n > 5))

Since these ``for`` loops have elegantly hidden the underlying mechanics,
let’s repeat the operation,
but this time invoke the underlying methods manually
as though we were ourselves a Python ``for`` loop.

.. testcode::

   # What the “for” loop does behind the scenes.

   it = numbers.__iter__()
   n = it.__next__()
   print(n)
   n = it.__next__()
   print(n)
   n = it.__next__()
   print(n)
   n = it.__next__()
   print(n)
   n = it.__next__()

.. testoutput::

   TODO





Making an object its own iterable



It might surprise you at first
that two objects are involved here —
why can’t ``OddNumbers`` itself maintain the counter
that gets incremented as the ``for`` loop makes progress?

The reason a container might need to spin up several iterators
is that Python code might simultaneously
make several iterations across the same object.
To see the problem,
let’s imagine that we had only implemented the ``OddIterator`` —
a single object, with a single loop counter inside —
and two concentric ``for`` loops tried to make use of it
to produce pairs of odd numbers::

.. testcode::


.. testoutput::

   TODO

The output ended earlier than we expected
because the two ``for`` loops had to share

For example,
here’s a pair of ``for`` loops which each needs its own ``OddIterator``


these concentric ``for`` loops across the same list
would interfere with each other
break if the list had only a single counter inside of it


why? because loop in another loop
also because of threads

but maybe just need one

The builtins “iter()” and “next()”

that would put dunders into your code, which would be terrible

> Dunders are for defining, not for calling

but what if you need to do several
iter()

subtlety
don’t actually need a container

Iterating with “next()”

what if you just want one element
next()

Writing a generator

yield

Writing a raw iterator

class

thrown out:

   i = OddIterator(OddNumbers(5))
   for a in i:
       for b in i:
           if b > a:
               print(a, b)
