#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Freidberg unconverged optimization test case developed by W.J. Rutten
Software adapted from openLEGO Sellar_competences test.
Models taken from Freidberg, Jeffrey P. Plasma Physics and Fusion Energy. Cambridge University Press, 2007.
"""
from __future__ import absolute_import, division, print_function

import numpy as np
from lxml import etree

from openlego.api import AbstractDiscipline
from openlego.utils.xml_utils import xml_safe_create_element
from openlego.partials.partials import Partials

from KB.config import root_tag, x_a, x_b, x_c, x_R0, x_PE, x_VIPE

class Objective(AbstractDiscipline):  # AbstractDiscipline

    @property
    def creator(self):
        return u'W.J. Rutten'
    
    @property
    def description(self):
        return u'Objective function of the Freidberg test case.'

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
    
    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_VIPE, [x_a, x_b, x_c, x_R0, x_PE])
        return partials.get_string()
    
    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        a = float(doc.xpath(x_a)[0].text)
        b = float(doc.xpath(x_b)[0].text)
        c = float(doc.xpath(x_c)[0].text)
        R0 = float(doc.xpath(x_R0)[0].text)
        PE = float(doc.xpath(x_PE)[0].text)

    # Volume over electric power objective function adapted from as derived in Freidberg (2007), eq. 5.17. P_W has been substituted for PE.
        w1 = 0.0001
        w2 = 0.9999
        # VIPE = 2*np.pi**2*R0*((a+b+c)**2-a**2)/PE
        O1 = 2*np.pi**2*R0*((a+b+c)**2-a**2)/PE
        O2 = 1/(PE/1000)

        print(O1,O2)

        VIPE = np.sqrt(w1*O1**2 + w2*O2**2)
# w1*(2*np.pi**2*R0*((a+b+c)**2-a**2)/PE)**2 
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_VIPE, VIPE)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def linearize(in_file, partials_file):
        doc = etree.parse(in_file)
        a = float(doc.xpath(x_a)[0].text)
        b = float(doc.xpath(x_b)[0].text)
        c = float(doc.xpath(x_c)[0].text)
        R0 = float(doc.xpath(x_R0)[0].text)
        PE = float(doc.xpath(x_PE)[0].text)

        dVIPEda = 2*np.pi**2*R0*2*(b+c)/PE
        dVIPEdb = 2*np.pi**2*R0*2*(a+b+c)/PE
        dVIPEdc = 2*np.pi**2*R0*2*(a+b+c)/PE
        dVIPEdR0 = 2*np.pi**2*((a+b+c)**2-a**2)/PE
        dVIPEdPE = -2*np.pi**2*R0*((a+b+c)**2-a**2)/PE**2

        partials = Partials()
        partials.declare_partials(x_VIPE, [x_a, x_b, x_c, x_R0, x_PE],
                                  [dVIPEda, dVIPEdb, dVIPEdc, dVIPEdR0, dVIPEdPE])
        partials.write(partials_file)
