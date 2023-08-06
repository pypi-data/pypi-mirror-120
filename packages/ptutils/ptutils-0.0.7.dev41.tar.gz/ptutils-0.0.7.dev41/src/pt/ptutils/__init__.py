#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Module
===========
This is the main module for the package.
"""
import os

from pt.ptutils.time import *

def version():
    """ Return the module version information. """
    from pt.ptutils.version import version as __version__
    return __version__


# Import protection
if __name__ == '__main__':
    raise Exception(
        "This module is not executable. To use it, add 'from pt import ptutils' to your python source code. Refer to the API documentation for more information."
    )
