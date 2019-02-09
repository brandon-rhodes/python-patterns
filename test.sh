#!/bin/bash

# Run this with Ubuntu Python 3.6, since unlike Anaconda Python it seems
# to come with the Python Standard Library test suite built-in.

/usr/bin/python3.6 -m unittest "$@" gang-of-four/*/test*.py && make doctest
