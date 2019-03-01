
===================
 Singleton Pattern
===================

*A “Creational Pattern” from the* :doc:`/gang-of-four/index`

.. admonition:: Verdict

   Code that needs repeated access to a single unique object
   should consider simply instantiating the object
   and passing it to each routine that needs it.
   It is always a compromise

   avoid side effects
   It is best to avoid the Singleton pattern in Python
   #can be accomplished more simply in Python
   and instead provide a module global
   
   by providing a 
   The Singleton pattern subverts the usual semantics class invocation
   by returning the same object instance each time the class is called.
   It is an awkward attempt to disguise the use of a global
   

.. contents:: Contents:
   :backlinks: none

The Builder pattern has a most interesting history.
Its primary intent,

if someone does a singleton
just subclass

>>> type(NotImplemented)()
NotImplemented


Modules are singletons!



what singleton means

“one-item tuple”

A flyweight object (... “that is returned by constructor”?)

A singleton object accessed by name

The one unique object that is ever returned
from a class that implements the Gang of Four’s Singleton Pattern.



Lib/pydoc_data/topics.py

technically
you can test for object identity

even where used, discouraged: singleton *object* used instead
we say “None” not “NoneType()”  <--- wait, it's not even possible!

ellipsis
None
NotImplemented
(X,) x
UTC
singleton SearchDialog” etc in IDLE, turtle, distutil
string ('') are singletons and cannot be cloned.
Make sure response tuple is a singleton
“CPython's empty tuple is a singleton and cached in” - NO, that’s a flyweight
Python/Python-ast.c:928:    Del_singleton = PyType_GenericNew(Del_type, NULL, NULL); etc
/* call frozenset() to get the empty frozenset singleton */
Objects/unicodeobject.c:1803:unicode_is_singleton(PyObject *unicode)
Objects/bytesobject.c:92:    /* empty byte string singleton */
Objects/codeobject.c:504:    /* Py_None and Py_Ellipsis are singletons. */
Objects/codeobject.c:541:        /* use True, False and None singleton as tags for the real and imag
Objects/setobject.c:1063:/* The empty frozenset is a singleton */
Include/datetime.h:158:    /* singletons */
Doc/faq/programming.rst:283:Note that using a module is also the basis for implementing the Singleton design
Doc/reference/datamodel.rst:310:            pair: singleton; tuple
Doc/c-api/module.rst:258:singletons: if the *sys.modules* entry is removed and the module is re-imported,
Doc/c-api/module.rst:452:Single-phase initialization creates singleton modules that can be looked up
Doc/library/turtle.rst:63:   The function :func:`Screen` returns a singleton object of a
Doc/library/stdtypes.rst:4646:``None`` (a built-in name).  ``type(None)()`` produces the same singleton.
Doc/library/stdtypes.rst:4673:``type(NotImplemented)()`` produces the singleton instance.
Doc/library/enum.rst:1026:The most interesting thing about Enum members is that they are singletons.
Doc/library/unittest.mock.rst:549:        mock and unless the function returns the :data:`DEFAULT` singleton the
Doc/library/marshal.rst:46:singletons :const:`None`, :const:`Ellipsis` and :exc:`StopIteration` can also be
Doc/whatsnew/3.6.rst:2405:The ``PyExc_RecursionErrorInst`` singleton that was part of the public API
