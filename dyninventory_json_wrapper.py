#!/usr/bin/env python
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, "dyninventory.json")) as f:
    print f.read()
