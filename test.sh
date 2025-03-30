#!/bin/bash

python3 -m unittest "$@" gang-of-four/*/test*.py && make doctest
