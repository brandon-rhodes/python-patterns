#!/bin/bash

,simplehttpserver &
,watch make dirhtml doctest -- **/*.rst **/*.css
