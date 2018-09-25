
==================
 Prebound Methods
==================


.. to find examples:
   ag --ignore site-packages '^[a-z_]+ = [a-z_]+\.[a-z_]+$' /usr/lib/python3.6




Prebound Methods

There are occasions on which
 a python module
 there are python modules
 which wants to offer
 a collection of routines for their users to invoke
 which will need at runtime to share state

The most flexible and pythonic way
 for two routines to share state
 is for them both to be bound methods
 of a single background object

probably the most famous example of this pattern
 is the python standard libraries random module
 while it provides its users with a flexibility
 to instantiate random number generators of Their Own
 it provides convenience for its most common users
 by offering a slate of column balls at the top level of the module
 which are in fact methods bound to a single background random number generator object

 after investigating a few other alternatives
 we will see how this pattern looks in Python code 

Alternatives
==

The most primitive approach
 available 2 a pair of column balls
 at the in a modules
 to share State between
 for a pair of column apples in a modules global namespace
 is to write a pair of functions
 which manipulate common Global state
 share directly at the top level of the module

 imagine that we want to offer a simple random number generator
 it returns in an English Loop  endless loop
 The numbers between 1 and255
we also want to offer a simple routine
 for using those random numbers
 to choose an integer between 0 and maximum value
 If it were only possible to write plane functions
 then we might store the seed
 the random number generators current state
 as a module global
 and have our functions directly access and modify it
 as their shared state

EXAMPLE

 there are several problems with this approach

it is impossible to ever instantiate
 a second copy of this random number generator.
 if two threads each want their own copy of the generator
 So so they don't have to protect it with locks
 then they are out of luck
( of course I'm lying
 you could rename the module insist. Modules
 Andre imported to get a second copy
 or you could manually instantiate II module
 and copy all three names across
 what I actually mean is that it's impossible to instantiate a second random number generator
 without being ridiculous)

it is more difficult 2D couple the test
 that you will want to write for your random number generator
 instead of each test getting its own instance
 the tests will all have to share the single pair of global functions
 and reach inside of their implementation
 will have to reach in to set the seed back to a known value
 if the tests wish to be orthogonal

there is no encapsulation
this will sound like a fuzzy your complaint
 then the previous 2
 but it can offend readability
 for a tight small system like this of two functions in common state
 to be splayed out as three separate names
 in a module which might contain dozens of other objects

 to solve the above problems
 we create a class
 we in fact exercise that greatest and most magnificent of all design patterns
 the facade
 the shared  State between the two routines
 will now be stored on the same object
 on which the user accesses the functions as methods
 Blah
 Example

the software engineer would do well to stop at this moment
 and pause for breath
 to look at this example class and to think quite seriously
 about the fact that in the vast majority of cases
 defining simply to finding the class is enough

 is the convenience to your users of instantiating the class for them
really going to be so profound
without asking their permission
 or knowing or even or knowing their exact circumstances
 you are going to do it on their behalf
 on the chance the mirror chance that they will use it
 remember that if your user does need does require
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

 the pattern itself

  in the global namespace of your module

 instantiate your class  and assign it a private name usually the pattern is carried out without inviting users to directly ever name the object in their code
 assign each of the objects methods to the same name in the modules global namespace

 4 the random class that we used as an illustration above
 the entire module might look like this

 Example

 users will now be able to invoke each method
 as though it is a stand-alone function
 the methods will all share State automatically thanks to their common instance
 without the user having to instantiate name and keep up with
 an explicit instance of Their Own

 when exercising this pattern
 please be responsible but the fact
 that you are instantiating an object at import time
 this pattern is not appropriate
 if it's tan she a Ting the class will perform any Ohio
 or inflict any side effects on other parts of the runtime
 in that case you will need a more complicated scheme
 where any side effects are deferred
 until the 1st of your methods is called

 but for lightweight objects
 that need no prior configuration before being instantiated
 and that are cheaper to build & use once
 prebound methods are a very elegant way
 to make the behaviors of a class
 of available at level module level
 think of the expense if every module that used the random module
 had to create its own instance
 that went and built the seed number

 cut examples here

 one final hint
 it is  almost always better
 to assign methods to names explicitly
 if there are 12 methods
 then there should be a stack of 12 assignment statements
 align against the left hand column of your module
python is a dynamic language
 which might tempt you 2 automate the series of assignments
 using attribute introspection and a for Loop
 I advise against it
 python programmers prefer explicit rather than implicit
 if the random module has a routine Rand and
 I want to be able to find it like rapping
 Gripping





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


