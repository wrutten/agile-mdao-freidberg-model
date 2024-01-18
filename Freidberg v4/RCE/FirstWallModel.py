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

import numpy as np
from lxml import etree

from kadmos.utilities.xml_utils_openlego import xml_safe_create_element

from config import root_tag, x_R0, x_a, x_En, x_n, x_sigmav, x_PW

from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline
from ssbjkadmos.utils.execution import run_tool


class FirstWallModel(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'First wall model of the Freidberg test case.'

    @property
    def supplies_partials(self):
        return False

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_R0, 5) #m
        xml_safe_create_element(doc, x_a, 2) #m
        xml_safe_create_element(doc, x_En, 14.1) #MeV
        xml_safe_create_element(doc, x_n, 1.5e20) #m-3
        xml_safe_create_element(doc, x_sigmav, 3e-22) #m3/s

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_PW, 4)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        R0 = float(doc.xpath(x_R0)[0].text)
        a = float(doc.xpath(x_a)[0].text)
        En = float(doc.xpath(x_En)[0].text)
        n = float(doc.xpath(x_n)[0].text)
        sigmav = float(doc.xpath(x_sigmav)[0].text)


        PW = firstwallmodel(a, En, n, sigmav, R0)

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_PW, PW)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

def firstwallmodel(a, En, n, sigmav, R0):
    # First wall radiation load equation as derived from Freidberg (2007), eq. 5.19. This equation is solved for PW
    # R0 is not used in this equation, but is added as input since to match the CMDOWS file.

    PW = En*n**2*sigmav*a/8/(6.241509*10**18) #MW/m2

    return PW


if __name__ == "__main__":

    analysis = FirstWallModel()
    run_tool(analysis, sys.argv)
