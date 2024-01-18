#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Freidberg unconverged optimization test case developed by Willem Rutten
Software adapted from SSBJKadmos test case implementation
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

from config import root_tag, x_a, x_b, x_c, x_R0, x_PE, x_VIPE

from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline
from ssbjkadmos.utils.execution import run_tool


class VolumeOverPowerModel(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'VolumeOverPower model of the Freidberg test case.'

    @property
    def supplies_partials(self):
        return False

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_a, 2) #m
        xml_safe_create_element(doc, x_b, 1) #m
        xml_safe_create_element(doc, x_c, 1) #m
        xml_safe_create_element(doc, x_R0, 5) #m
        xml_safe_create_element(doc, x_PE, 1000) #MW

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_VIPE, 1) # m3/MW

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        a = float(doc.xpath(x_a)[0].text)
        b = float(doc.xpath(x_b)[0].text)
        c = float(doc.xpath(x_c)[0].text)
        R0 = float(doc.xpath(x_R0)[0].text)
        PE = float(doc.xpath(x_PE)[0].text)

        VIPE = volumeoverpowermodel(a, b, c, R0, PE)

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_VIPE, VIPE)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

def volumeoverpowermodel(a, b, c, R0, PE):
    # Volume over electric power objective function adapted from as derived in Freidberg (2007), eq. 5.17. P_W has been substituted for PE.


    VIPE = 2*np.pi**2*R0*((a+b+c)**2-a**2)/PE #m3/MW

    return VIPE


if __name__ == "__main__":

    analysis = VolumeOverPowerModel()
    run_tool(analysis, sys.argv)
