#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Freidberg unconverged optimization test case developed by Willem Rutten
Software adapted from SSBJ test case implementation
SSBJ test case - http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19980234657.pdf
Original Python implementation for OpenMDAO integration developed by
Sylvain Dubreuil and Remi Lafage of ONERA, the French Aerospace Lab.
Original files taken from: https://github.com/OneraHub/SSBJ-OpenMDAO
The files were adjusted for optimal use in KADMOS by Imco van Gent.
"""
from __future__ import absolute_import, division, print_function

import sys

from database.BlanketModel import BlanketModel

class Blanket(BlanketModel):  # AbstractDiscipline
    pass


if __name__ == "__main__":
    Blanket().run_tool(sys.argv)
