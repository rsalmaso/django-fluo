# -*- coding: utf-8 -*-

import os, sys

# PATH is the absolute path leading to parent directory
PATH, _ = os.path.split(os.path.dirname(os.path.realpath(__file__)))
SITE_PACKAGES = os.path.join(PATH, 'site-packages')

# insert every package listed in site-packages directory
for pkg in os.listdir(SITE_PACKAGES):
    sys.path.insert(0, os.path.join(SITE_PACKAGES, pkg))

sys.path.insert(0, PATH)
