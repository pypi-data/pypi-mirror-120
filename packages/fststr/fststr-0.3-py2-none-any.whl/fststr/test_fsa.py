#!/usr/bin/env python

import pywrapfst as fst

compiler = fst.Compiler()

print('0 1 1\n1 2 1\n1', file=compiler)