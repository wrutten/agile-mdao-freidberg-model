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

from database.config import root_tag, x_a, x_b, x_c, x_Bc, x_mu0, x_sigma

from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline


class CoilsModel(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'Coils model of the Freidberg test case.'

    @property
    def supplies_partials(self):
        return False

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_a, 2) #m
        xml_safe_create_element(doc, x_b, 1) #m
        xml_safe_create_element(doc, x_c, 1) #m
        xml_safe_create_element(doc, x_Bc, 13) #T
        xml_safe_create_element(doc, x_mu0, 1.24552706212e-6) #kg m s-2 A-2

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_sigma, 300) # MPa

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        a = float(doc.xpath(x_a)[0].text)
        b = float(doc.xpath(x_b)[0].text)
        c = float(doc.xpath(x_c)[0].text)
        Bc = float(doc.xpath(x_Bc)[0].text)
        mu0 = float(doc.xpath(x_mu0)[0].text)


        sigma = coilsmodel(a, b, c, Bc, mu0)

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_sigma, sigma)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

def coilsmodel(a, b, c, Bc, mu0):
    # First wall radiation load equation as derived from Freidberg (2007), eq. 5.27, rewritten to solve for sigma

    ksi = c/(c+2*(a+b))
    sigma = Bc**2/(4*mu0*ksi)/10**6 # MPa

    return sigma


if __name__ == "__main__":
    CoilsModel().run_tool(sys.argv)
