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

from config import root_tag, x_a, x_R0, x_Ealpha, x_En, x_ELi, x_etat, x_n, x_sigmav, x_PE

from ssbjkadmos.tools.SsbjDiscipline import SsbjDiscipline
from ssbjkadmos.utils.execution import run_tool


class PlasmaModel(SsbjDiscipline):  # AbstractDiscipline

    @property
    def description(self):
        return u'Plasma model of the Freidberg test case.'

    @property
    def supplies_partials(self):
        return False

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_a, 2) #m
        xml_safe_create_element(doc, x_R0, 5) #m
        xml_safe_create_element(doc, x_Ealpha, 3.5) #MeV
        xml_safe_create_element(doc, x_En, 14.1) #MeV
        xml_safe_create_element(doc, x_ELi, 2.5) #MeV
        xml_safe_create_element(doc, x_etat, 0.4) # -
        xml_safe_create_element(doc, x_n, 1.5e20) #m-3
        xml_safe_create_element(doc, x_sigmav, 3e-22) #m3 s-1

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_PE, 1000) # MW

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        a = float(doc.xpath(x_a)[0].text)
        R0 = float(doc.xpath(x_R0)[0].text)
        Ealpha = float(doc.xpath(x_Ealpha)[0].text)
        En = float(doc.xpath(x_En)[0].text)
        ELi = float(doc.xpath(x_ELi)[0].text)
        etat = float(doc.xpath(x_etat)[0].text)
        n = float(doc.xpath(x_n)[0].text)
        sigmav = float(doc.xpath(x_sigmav)[0].text)

        PE = plasmamodel(a, R0, Ealpha, En, ELi, etat, n, sigmav)

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_PE, PE)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

def plasmamodel(a, R0, Ealpha, En, ELi, etat, n, sigmav):
    # Plasma power output equation as derived in Freidberg (2007), eq. 5.18,

    e = 1.602176634e-19 # elementary charge
    PE = 0.25*etat*(Ealpha+En+ELi)*n**2*sigmav*(2*np.pi**2*R0*a**2)*e # MW

    return PE


if __name__ == "__main__":

    analysis = PlasmaModel()
    run_tool(analysis, sys.argv)
