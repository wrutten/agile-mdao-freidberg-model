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

from KB.config import root_tag, x_a, x_b, x_c, x_Bc, x_mu0, x_sigma

class Coils(AbstractDiscipline):  # AbstractDiscipline

    @property
    def creator(self):
        return u'W.J. Rutten'

    @property
    def description(self):
        return u'Coils model of the Freidberg test case.'

    @property
    def supplies_partials(self):
        return True

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

    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_sigma, [x_a, x_b, x_c])
        return partials.get_string()
    
    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        a = float(doc.xpath(x_a)[0].text)
        b = float(doc.xpath(x_b)[0].text)
        c = float(doc.xpath(x_c)[0].text)
        Bc = float(doc.xpath(x_Bc)[0].text)
        mu0 = float(doc.xpath(x_mu0)[0].text)

        # The actual equations
        ksi = c/(c+2*(a+b))
        sigma = Bc**2/(4*mu0*ksi)/10**6 # MPa

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_sigma, sigma)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def linearize(in_file, partials_file):
        doc = etree.parse(in_file)
        a = float(doc.xpath(x_a)[0].text)
        b = float(doc.xpath(x_b)[0].text)
        c = float(doc.xpath(x_c)[0].text)
        Bc = float(doc.xpath(x_Bc)[0].text)
        mu0 = float(doc.xpath(x_mu0)[0].text)

        A = Bc**2/4/mu0/10**6

        dsigmada = 2*A/c
        dsigmadb = 2*A/c
        dsigmadc = -2*A*(a+b)/c**2

        partials = Partials()
        partials.declare_partials(x_sigma, [x_a, x_b, x_c],
                                  [dsigmada, dsigmadb, dsigmadc])
        partials.write(partials_file)
