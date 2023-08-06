# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Kevin De Bruycker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

__version__ = '0.3.2'

import sys
import struct
from .relaxation import *
from .gui import GUI

if struct.calcsize("P") * 8 == 64:
    print('Warning!\n'
          'Because of an interaction between two packages (numpy and matplotlib), \n'
          'a LinAlgError might occur when fitting a generalised Maxwell model \n'
          'on certain configurations in comibation with a 64-bit python.\n'
          'The issue is traced to the dashed 1/e line in the stress relaxation overview plot.\n'
          'Fixes include switching to a 32-bit version of python, only plotting normalised curves\n'
          'when not using the generalised Maxwell model, changing the source file to show an \n'
          'aesthetically less pleasing solid line instead, or waiting for numpy to be updated.', file=sys.stderr)
