#!/bin/bash

python3.6 -m unittest "$@" gang-of-four/*/test*.py && make doctest
