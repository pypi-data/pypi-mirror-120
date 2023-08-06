#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
# Imports
########################################################################
from pt import ptutils
import pytest

def test_import_version():
    """ Test theat the package version is defined and that imports are working. """
    from pt.ptutils.version import version