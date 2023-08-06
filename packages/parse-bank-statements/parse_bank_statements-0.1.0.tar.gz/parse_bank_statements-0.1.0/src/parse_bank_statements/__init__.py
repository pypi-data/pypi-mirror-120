#!/usr/bin/env python


"""Shotfile reading with pure python
"""

__author__  = 'Giovanni Tardini'
__version__ = '0.1.0'
__date__    = '21.09.2021'

import sys

from .parse_bank_statements import *

# Backward compatibility.

# On Windows, we encode and decode deep enough that something goes wrong and
# the encodings.utf_8 module is loaded and then unloaded, I don't know why.
# Adding a reference here prevents it from being unloaded.  Yuk.
import encodings.utf_8      # pylint: disable=wrong-import-position, wrong-import-order
