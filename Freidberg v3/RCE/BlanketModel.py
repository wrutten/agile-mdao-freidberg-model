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

from config import root_tag, x_lambdasd, x_lambdabr, x_En, x_Et, x_gamman, x_gamman0, x_b

from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline
from ssbjkadmos.utils.execution import run_tool


class BlanketModel(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'Blanket model of the Freidberg test case.'

    @property
    def supplies_partials(self):
        return False

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_lambdasd, 0.055) #m
        xml_safe_create_element(doc, x_lambdabr, 0.0031) #m
        xml_safe_create_element(doc, x_En, 14.1) #MeV
        xml_safe_create_element(doc, x_Et, 0.025e-6) #MeV
        xml_safe_create_element(doc, x_gamman0, 1.77e18) #s-1
        xml_safe_create_element(doc, x_b, 1) #s-1

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_b, 1) #m

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        b = float(doc.xpath(x_b)[0].text)
        lambdasd = float(doc.xpath(x_lambdasd)[0].text)
        lambdabr = float(doc.xpath(x_lambdabr)[0].text)
        En = float(doc.xpath(x_En)[0].text)
        Et = float(doc.xpath(x_Et)[0].text)
        gamman0 = float(doc.xpath(x_gamman0)[0].text)


        gamman = blanketmodel(b, lambdasd, lambdabr, En, Et, gamman0)

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_gamman, gamman)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

def blanketmodel(b, lambdasd, lambdabr, En, Et, gamman0):
    # Blanket thickness equation from Freidberg (2007), eq. 5.10.

    gamman = gamman0*np.exp(-2*np.sqrt(Et/En)*lambdasd/lambdabr*np.exp(0.5*b/lambdasd-1))

    return gamman


if __name__ == "__main__":

    analysis = BlanketModel()
    run_tool(analysis, sys.argv)
