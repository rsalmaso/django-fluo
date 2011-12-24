#!/usr/bin/env python
import os, sys

# PATH is the absolute path leading to parent directory
PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
LIB_DIR = os.path.join(PATH, 'lib')

for path in os.listdir(LIB_DIR):
    pkg = os.path.join(LIB_DIR, path)
    if os.path.isdir(pkg) and pkg not in sys.path:
        sys.path.insert(0, pkg)
if PATH not in sys.path:
    sys.path.insert(0, PATH)

# remove current path
PROJECT_PATH = os.path.split(os.path.realpath(__file__))[0]
try:
    sys.path.remove(PROJECT_PATH)
except ValueError:
    pass

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ project_name }}.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
