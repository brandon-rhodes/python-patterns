#!/bin/bash

,simplehttpserver &
,watch make dirhtml doctest -- $(find -name '*.rst') */*.css _templates/*.html
