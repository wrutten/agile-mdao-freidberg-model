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

from KB.config import root_tag, x_PE, x_CPE

class CPE(AbstractDiscipline):  # AbstractDiscipline

    @property
    def creator(self):
        return u'W.J. Rutten'
    
    @property
    def description(self):
        return u'Electric Power Constraint (CPE) of the Freidberg test case. CPE=PE'

    @property
    def supplies_partials(self):
        return True

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_PE, 1000) #MW


        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_CPE, 1000) # MW

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)
    
    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_CPE, [x_PE])
        return partials.get_string()
    
    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        PE = float(doc.xpath(x_PE)[0].text)

        CPE = PE

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_CPE, CPE)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def linearize(in_file, partials_file):

        partials = Partials()
        partials.declare_partials(x_CPE, [x_PE],
                                  [1])
        partials.write(partials_file)
