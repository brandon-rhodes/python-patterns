
=================
 Builder Pattern
=================

.. admonition:: Verdict

   The Builder Pattern is so convenient
   that it seems to turn up everywhere in Python libraries,
   whether the author knew it was a design pattern or not.
   Happily, Python lacks several constraints
   that in other languages lead to almost every complex class
   needing its own builder.

.. contents:: Contents:
   :backlinks: none

The Pattern
facade
open
file
_io.TextIOWrapper
plt
multiplxing
originally to multiplex
but now just because it’s convenient
Data
h?

Elsewhere: mutable builders for immutable objects


The Builder pattern is second nature to the Python programmer,
many of whom see it every way without ever giving it thought.
Its original purposes were:

* Allowing a single routine
  to drive the creation of several different kinds of object
  depending on which builder it is passed,
  without needing to know their differences or details behind the scenes.

* For the sake of convenience;
  even a routine that only needs to create a single kind of object
  might be able to do so more easily
  if it’s given a builder that automates much of the work.

It turns out that it is this latter purpose
which has taken off in the Python world.
We provide builders to make it convenient to use libraries.
Only rarely do we implement the Builder pattern
so that a single routine can be used to build
more than one system of objects from the same set of builder calls —
a problem for which a better pattern exists,
which will be discussed below.

Beyond the above two uses
for which the Builder pattern was originally proposed,
a novel use has sprung up and become popular
to escape the limits of languages that lack optional keyword arguments.
For the sake of completeness I’ll demonstrate that approach
in the last section of this document.

The Pattern
===========

The Builder pattern recommends
that when a library needs to build
a whole constellation of objects and subordinate objects
whose construction could be described more simply
through a series of method calls,
that the library should avoid sending its users
through the tedium of creating the objects one by one
and instead provide an API taking those parameters
and performing the construction behind the scenes.

A classic example is the `matplotlib <https://matplotlib.org/>`_ library’s
``pyplot`` interface.
Constructing a very simple plot with ``pyplot``
can be accomplished in a single line of code,
and it can be saved to a file with just one line more:

.. testsetup::

   import os
   os.chdir('gang-of-four/builder')

.. testcleanup::

   os.chdir('../..')

.. testcode::

   import numpy as np
   x = np.arange(-6.2, 6.2, 0.1)

   import matplotlib.pyplot as plt
   plt.plot(x, np.sin(x))
   plt.plot(x, np.cos(x))
   plt.savefig('sine.png')

.. image:: sine.png

What the pyplot interface
has happily — very, very happily —
hidden from the user here
is that a dozen or more objects had to be created
for matplotlib to represent and manage
all of the components of this plot in Python.
Here, for example, are eight of them:

>>> plt.gcf()
<Figure size 640x480 with 1 Axes>
>>> plt.gcf().subplots()
<matplotlib.axes._subplots.AxesSubplot object at 0x7ff910917a20>
>>> plt.gcf().subplots().bbox
TransformedBbox(
    Bbox(x0=0.125, y0=0.10999999999999999, x1=0.9, y1=0.88),
    BboxTransformTo(
        TransformedBbox(
            Bbox(x0=0.0, y0=0.0, x1=6.4, y1=4.8),
            Affine2D(
                [[100.   0.   0.]
                 [  0. 100.   0.]
                 [  0.   0.   1.]]))))

The creation of this entire cascade of objects
was accomplished by our calls to `plot()`.
While we had the option of providing more keyword arguments
or making additional calls to customize the objects further,
``pyplot`` is happy to insulate us from most of the details
of plots are represented as objects.

The Builder pattern is now deeply ingrained in Python culture,
thanks in part to the pressure that library authors feel
to make the sample code on their front page
as impressively short and convenient as possible.
But there do exist libraries that expect you,
their user, to build the entire object hierarchy above
one object at a time in your own code.

The fact that some libraries
rely on their callers to tediously instantiate objects
is even used as advertisement by their competitors.
For example,
the `Requests library <http://docs.python-requests.org/en/master/>`_
famously introduces itself to users
by comparing its one-liner for making an HTTP request with authentication
with the same maneuver performed with the old
`urllib2 <https://docs.python.org/2/library/urllib2.html>`_
Standard Library module —
which does, in fairness, seem to require the caller
to build a small pile of objects
any time they want to do anything interesting.
The “Examples” section of its documentation provides an illustration::

    import urllib2
    # Create an OpenerDirector with support for Basic HTTP Authentication...
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='PDQ Application',
                              uri='https://mahler:8092/site-updates.py',
                              user='klem',
                              passwd='kadidd!ehopper')
    opener = urllib2.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    urllib2.install_opener(opener)
    urllib2.urlopen('http://www.example.com/login.html')

Had the Builder pattern been used here,
the library would instead have offered constructors or methods
that concealed from client code
the actual names of the classes being built.

building different things

When a gang of four formally described the Builder pattern it is notable they did not consider convenience to be its most important result property instead they opened their own description of the pattern by emphasizing how it decouples code from Individual classes And therefore can let the same code Drive the creation of several different forests of objects

 in the examples above the calling code is certainly decoupled through the Builder pattern from the specific classes that it is instantiating you call plot or requestand thereforecan old support. Get and you usually don't even know which exact classes are being created behind the scenes

 maybe add to that previous paragraph a little flourish like how does it take apple decouple

 but the gang of four was excited not nearly at decoupling code from specific classes with all of the simplification and elimination of import statements that that happily entails but with the fact that it enables multiplexing the same code can be passed different builders on different occasions in order to drive the construction of different kinds of objects

 indeed vein name this as the primary intent of their Builder pattern

 quote intent separate the construction of a complex object from its representation so that the same construction process can create different representations

At least in Python code this seems to be by far the less common of the two main uses of the Builder pattern the gang of four use as their example a text converter that needs to be able to produce plain asking and also populate an interactive text widget they imagine code that calls methods like convert character and convert paragraph That each Builder implements anyway appropriate to its medium

 examples of this sort could have course easily be multiplied you might want to write only once the code for producing a certain drawing and have the draw line method that it is calling on one occasion produce the SVG description for that line but on another occasion to actually paint pixels in a PNG that you were about to save out

 this pattern proves far more rare in Python code then I think the gang of four riding in the 1990s might have expected the reason Maybe the growing and happy popularity of intermediate representations as the coupling between the different phases of a Python program we today are far more likely to  write code that builds an intermediate representation that an output routine can mend reverse then we are likely 2 have our drawing code directly and immediately invoke output routines you can see this pattern in our first example matplotlib all of your plotting commands merely create an intermediate representation all of those objects insert example here that is only turned into real lines on a page when you have finished manipulating it and pass it to the output routine

 nevertheless examples of the Builder pattern as multiplexer can be discovered if you look hard enough here is one very modest example from the python standard Library

even though most applications today are likely to use a small relational database for local configuration storage think of the way that both Chrome and Firefox use sequel light three also built into python standard Library. but there was an era in which small key value stores were very popular and the python standard Library recalls this Legacy and its various flavors of DDM module all inheriting in some way or other from the famous Berkeley database C library

 as implementations of the simple key Value Store proliferated list them here>  the standard Library grew more modules this presented programmers with a problem how can they detect which Berkeley database implementations are available on the platform that python was compiled on and select which one to use

 the standard Library provides a simple Builder pattern as the solution the any dbm module programmer makes a single call and receives an instance of whatever the best supported Berkeley database key value library is on the current system given the way the python was compiled the calling code gets too then use the key value API of the day store from the question of which exact class has been returned to it and does not even need to import the correct module itself in miniature this is the Builder pattern as originally envisioned by the gang of four

 the Builder pattern as boilerplate

For the sake of completeness I should mention a most bizarre use to which the Builder pattern back a most bizarre use to which the Builder pattern back the most unexpected use to which the Builder pattern has been put in certain underpowered languages--  especiallyto help readers who might have run across who might have run across the pattern and have been confused by it

 for the sake of completeness I should describe a surprising use to which the Builder pattern has recently been put in other less convenient languages than python in particular I hope to help readers who might have seen examples of this practice and thereby been confused about how the Builder pattern usually books in Python code

 looks in Python code

The problem arises like this

 a programmer designs an designs of class object intended to hold data and wishes it's fields to be immutable

  the class has several attributes imagine that it has a dozen

 but they are writing in a programming language that wax pythons support 4 optional arguments neither position Lee nor through keywords can they select which attributes back can they select which arguments to pass to the initialization function method of the class and which attributes to leave at their default values

 you will see immediately the unhappy consequence of writing such a classin such a language everytime you instantiate one of the objects you will have to supply a value for every one of the Dozen attributes 

 to escape their  dilemma and to support the same kind of brevity that python programmers take for granted programmers facing the situation supplement each class they are writing with a separate second class that serves only as a builder for the first and this is the key the Builder object is not immutable it can therefore quietly set all of its attributes to default values then offer methods by which users can manipulate only the attributes they need to set manually and then finally have a method where all of the attributes both those with their default values and those that were manually set all get used together to construct the immutable object that's the ultimate goal at the expense of a good deal of boilerplate this allows programmers in more deeply compromised languages to enjoy some of the same Freedom that we python programmers get through optional arguments to an initialization method

 hopefully you will never see code like this in Python especially since an excellent stack Overflow answer has provided the secret to allowing even named tuples to have defaults 4 initialization arguments but you should now be forearmed against blog posts that present the above pattern as though it is the essence of the gang of fours Builder pattern when in fact gang of four originally wrote blah when in fact the gang of fours original chapter on the Builder pattern does not even mention or consider the case of an immutable object and the difficulties that might involve constructing it the original Builder pattern looks nothing like the above code it is simply the construction of an object hierarchy on behalf of calling code that is there by relieved of needing to construct the objects it's itself 



