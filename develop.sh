#!/bin/bash

,simplehttpserver &
,watch make dirhtml doctest -- gang-of-four/**
