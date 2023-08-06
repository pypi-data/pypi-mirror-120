#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Module
===========
This is the main module for the package.
"""
import os


def version():
    """ Return the module version information. """
    from pt.ptutils.version import version as __version__
    return __version__


# =============================================================================
# = Main
# =============================================================================
if __name__ == '__main__':
    __SCRIPT_DIR_PATH__ = os.path.dirname(os.path.abspath(__file__))
    __XMOD_NAME__ = os.path.basename(__SCRIPT_DIR_PATH__.rstrip(os.sep))
    print(
        "This module is not executable. To use it, add 'import " +
        __XMOD_NAME__ +
        "' to your python source code. Refer to the API documentation for " +
        "more information"
    )
