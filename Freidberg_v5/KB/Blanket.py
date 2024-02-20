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

from KB.config import root_tag, x_lambdasd, x_lambdabr, x_En, x_Et, x_gammafrac, x_b

class Blanket(AbstractDiscipline):

    @property
    def creator(self):
        return u'W.J. Rutten'

    @property
    def description(self):
        return u'Blanket model of the Freidberg method'

    @property
    def supplies_partials(self):
        return False

    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_b, 0.)
        xml_safe_create_element(doc, x_Et, 0.)
        xml_safe_create_element(doc, x_En, 0.)
        xml_safe_create_element(doc, x_lambdabr, 0.)
        xml_safe_create_element(doc, x_lambdasd, 0.)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_gammafrac, 0.)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_gammafrac, [x_b])
        return partials.get_string()

    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        b = float(doc.xpath(x_b)[0].text)
        lambdasd = float(doc.xpath(x_lambdasd)[0].text)
        lambdabr = float(doc.xpath(x_lambdabr)[0].text)
        En = float(doc.xpath(x_En)[0].text)
        Et = float(doc.xpath(x_Et)[0].text)

        # The actual equation
        gammafrac = np.exp(-2*np.sqrt(Et/En)*lambdasd/lambdabr*np.exp(0.5*b/lambdasd-1))

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_gammafrac, gammafrac)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def linearize(in_file, partials_file):
        doc = etree.parse(in_file)
        b = float(doc.xpath(x_b)[0].text)
        lambdasd = float(doc.xpath(x_lambdasd)[0].text)
        lambdabr = float(doc.xpath(x_lambdabr)[0].text)
        En = float(doc.xpath(x_En)[0].text)
        Et = float(doc.xpath(x_Et)[0].text)

        # A = -2*np.sqrt(Et/En)*lambdasd/lambdabr
        # dgammafracdb = 0.5*A/lambdasd*np.exp(A*np.exp(0.5*b/lambdasd-1)+0.5*b/lambdasd-1)

        partials = Partials()
        partials.declare_partials(x_gammafrac, [x_b],
                                  [dgammafracdb])
        partials.write(partials_file)
