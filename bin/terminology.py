#!/usr/bin/env python3
"""Count the frequency of various phrases, given the path to the Python PEPs.

In Python PEPs, the opposite of “subclass” is almost always “base class” — just remember that the builtin is named super(), not base()! Stats:

216  base class
  0  child class
 10  derived class
 12  parent class
372  subclass
 10  super class
 44  superclass

"""
import argparse
import os
import re
import sys

TERMS = (
    'superclass',
    'super class',
    'subclass',
    'base class',
    'derived class',
    'parent class',
    'child class',
)

def main(argv):
    parser = argparse.ArgumentParser(description='PEP terminology counts')
    parser.add_argument('pepsdir', help='path to PEPs repo')

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        print('\nTo checkout the PEPs from version control, git clone:'
              '\nhttps://github.com/python/peps.git', file=sys.stderr)
        raise

    peps = []
    for dirpath, dirnames, filenames in os.walk(args.pepsdir):
        for filename in filenames:
            if filename.endswith(('.rst', '.txt')):
                peps.append(os.path.join(dirpath, filename))

    counts = {term: 0 for term in TERMS}

    for pep in peps:
        with open(pep) as f:
            content = f.read()
        text = ' '.join(re.findall('\w+', content.lower()))
        #text = ' '.join(content.lower().replace('.'), ' ').split())
        for term in TERMS:
            n = text.count(' ' + term + ' ')
            m = text.count(' ' + term + 'es ')
            counts[term] += n + m

    for term in sorted(TERMS):
        print('{:5}  {}'.format(counts[term], term))

if __name__ == '__main__':
    main(sys.argv[1:])
