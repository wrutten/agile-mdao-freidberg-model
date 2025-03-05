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

from KB.config import root_tag, x_R0, x_a, x_En, x_n, x_sigmav, x_PW

class FirstWall(AbstractDiscipline):  # AbstractDiscipline

    @property
    def creator(self):
        return u'W.J. Rutten'

    @property
    def description(self):
        return u'First wall model of the Freidberg test case.'

    @property
    def supplies_partials(self):
        return True

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
    
    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_PW, [x_a])
        return partials.get_string()
    
    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        R0 = float(doc.xpath(x_R0)[0].text) #should be removed as this is not used
        a = float(doc.xpath(x_a)[0].text)
        En = float(doc.xpath(x_En)[0].text)
        n = float(doc.xpath(x_n)[0].text)
        sigmav = float(doc.xpath(x_sigmav)[0].text)

        # First wall radiation load equation as derived from Freidberg (2007), eq. 5.19. This equation is solved for PW
        PW = En*n**2*sigmav*a/8/(6.241509*10**18) #MW/m2

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_PW, PW)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def linearize(in_file, partials_file):
        doc = etree.parse(in_file)
        En = float(doc.xpath(x_En)[0].text)
        n = float(doc.xpath(x_n)[0].text)
        sigmav = float(doc.xpath(x_sigmav)[0].text)

        dPWda = En*n**2*sigmav/8/(6.241509*10**18)

        partials = Partials()
        partials.declare_partials(x_PW, [x_a],
                                  [dPWda])
        partials.write(partials_file)
