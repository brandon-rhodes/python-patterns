
=================
 Sentinel Object
=================

*A Python variation on the “Creational Pattern” inspired by Modula-2 and Modula-3*

.. admonition:: Verdict

   python’s


.. contents:: Contents:
   :backlinks: none



Sentinel *value*
-------------------

*within* domain

Nan?

Empty string

An older pattern dictating
 still coming in statically typed languages
Is the idea of designating a sentinel value
 that lies within
 not outside of
 the range of values that can form 2-a functions type

 the python programmer
 will be familiar with this pattern
 from their experience with the string. Find method
 it's sibling the string. Index method
 is more rigorous
 it promises 2 + true index a real and true index
 or to never return at all
 how can a method never return
 returned why while still allowing its calling program to proceed
 only by raising an exception

E

 but exceptions carry a slight expense
 and an additional level of indentation and expense must be paid
 in order to intercept them
 both are inconvenient for the collar looking for a string substring
 but they often expect not to find
 that they often expect will not be present
 the solution is the find method
 which instead of raising an exception
 returns of value
 Within the integer domain
 type typical return type

E

 while string. Find chooses
 find have been implemented
 later in pythons history
 it is quite possible that it would have returned none as its result
 it is not unheard of for a Python program to make the mistake
 of using Vines return value as a string index
 without first checking whether it's values -1
 if only it had returned none
 an attempt to use it as a string index with raised an exception
 or if python it Chozen not to recognize negative indexes
 the use of its return value with simile have warned everyone away that exception
 would immediately have signaled a problem by causing an exception

 but the combination of the use of -1
 did it come from see I will look up an example
 with a language that recognizes -1 as the index of the last character in a string
 combine to become a stumbling block
 combined become a source of frequent xxx and regrettable error in the Python language

 values are not always so dangerous
 an floating point operation that goes out of range
 or that is missing data
 can return the official IEEE floating point value not a number
 without the risk of its being confused for a real floating Point number
 indeed the pandas Library
 if faced with an integer operation
 that has holes in its input data
 will switch to floating point so that it can use not a number

and even among types that lack enata number value
 like the integer and string
 recent languages like ago
 which don't make it convenient to return none if you are required to return an integer
 the less you to clear up whatever go calls an optional type
 are convincing many programmers
 that they can go much farther than they had expected without substantial confusion
 using 0 and the empty string
 where they have no more specific data to contribute
 all the python programmer will often value
 the semantic Clarity that comes with the use of none
probably do it in situations
 where oh with in tight Sentinel value
 would satisfy as well

Null pointer
------------------

Exceptions implemented sentinal value
.

Each python name
 each name that you define the python names face
 is a reference
 yields an object when you D reference it
 there are no exceptions
 unless the name is undefined
 it is guaranteed to lead to an object

 the object to what your name leads needs not be a very useful 1
 it might be none
 it might be an object
 which lacks any of the methods you would need
 to interact with the object you expect under that name
 but if a name exists
 then it must refer to some existing object
 python does not allow names
 to refer
 to nothing

 pythons approach in this instance
 Here
 is different than that of languages
 which make the concept of a pointer
 an integer that stores the location of some other object in memory
 more explicit
 in many languages where developers are invited to create and manipulate pointers
 it is explicit that a pointer
 that there is an alternative
 that for a pointer there is an alternative
 to providing the address of an object
 instead the pointer value might itself be invalid
 to represent the fact that at the moment it does not want 2 reference an object at all

wow such language is tend to hide the official value
 meaning this does not reference an object
 this pointer
 behind a definition like null
 it is very common for the special pointer address
 which means this is not pointing at anything
 to be the address 0
 even if in a particular language model
 language and in a particular operating systems memory model
 the address 0 could name a valid memory location
 it is easy enough for the language implementation to never create an object that exactly that bite
 or even to find other another useful purpose for the data add that address
 to Forever Exempted from being used for an object

 python opted to avoid this complexity
 how do I explain this without repeating everything above
 figure it out

 while all the Python language itself does not allow names
 to assume an invalid value
 which in fact prefers to No Object
 Refers
 at the sea level see python makes continuous use of the distinction
many languages which Implement exceptions
 have to return to values at a low level from every routine
 the return value in case the routine completed successfully
 and the value of any exception that it raised instead

 python avoids the need for every low level C function to return two return values
 by designating the special return value know null
 again normally a 0 pointer
 as an indication that the routine has returned no useful python value
 but has instead raised an exception
 the exception
 since the return value does not specify the exception
 it must be returned out of band
 some variables set
 look it up

E

 yeah

Null object
----------------

Fowler; woolf

 unimportant observation is made
 by Martin Fowler in his book x

 do the actual quote

 Choosing
 adopting the convention that a name might either refer to a useful value
 or else might bear a special value which means nothing is here
 imposes a burden upon every subsequent piece of code that must handle that value

 to take an example

E

 all of the code Downstream from here
is going to have to test whether the value is none

E

 Martin describes an interesting alternative mentions an interesting all turn
 described by wolf

 Quote

 before designating a value
 that might either be a useful object or none
 if you are in a domain
 double check weather you might be in a domain
 where a functioning user object might be provided instead
 yeah

Sentinel object
----------------------

You will need a sentinel object
in the special circumstance

1 youre one year in Python none see not in C

2 

 the Sentinel you will want a sentinel object
 The Sentinel object 

File: Lib/bz2.py
27:1:_sentinel = object()  <--- line occurs several times
^ token? no.

Lib/functools.py
_NOT_FOUND = object()
val = cache.get(self.attrname, _NOT_FOUND)

File: Lib/configparser.py
357:1:_UNSET = object()

only for efficiency if used in only one routine

http://www.ianbicking.org/blog/2008/12/the-magic-sentinel.html
for optional argument, noting Python 3 thing

http://effbot.org/zone/default-values.htm
for optional argument

https://www.revsys.com/tidbits/sentinel-values-python/
for optional argument
