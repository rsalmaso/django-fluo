# -*- coding: utf-8 -*-

import os, sys

# PATH is the absolute path leading to parent directory
PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
LIB_DIR = os.path.join(PATH, 'lib')

for path in [ LIB_DIR, PATH, ]:
    if path not in sys.path:
        sys.path.insert(0, path)

sys.path.insert(0, PATH)

