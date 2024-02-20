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

from KB.config import root_tag, x_a, x_R0, x_Ealpha, x_En, x_ELi, x_etat, x_n, x_sigmav, x_PE

class Plasma(AbstractDiscipline):  # AbstractDiscipline

    @property
    def creator(self):
        return u'W.J. Rutten'
    
    @property
    def description(self):
        return u'Plasma model of the Freidberg test case.'

    @property
    def supplies_partials(self):
        return True

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
    
    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_PE, [x_a, x_R0])
        return partials.get_string()
    
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

        # Plasma power output equation as derived in Freidberg (2007), eq. 5.18,
        e = 1.602176634e-19 # elementary charge
        PE = 0.25*etat*(Ealpha+En+ELi)*n**2*sigmav*(2*np.pi**2*R0*a**2)*e # MW

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_PE, PE)
        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

    @staticmethod
    def linearize(in_file, partials_file):
        doc = etree.parse(in_file)
        a = float(doc.xpath(x_a)[0].text)
        R0 = float(doc.xpath(x_R0)[0].text)
        Ealpha = float(doc.xpath(x_Ealpha)[0].text)
        En = float(doc.xpath(x_En)[0].text)
        ELi = float(doc.xpath(x_ELi)[0].text)
        etat = float(doc.xpath(x_etat)[0].text)
        n = float(doc.xpath(x_n)[0].text)
        sigmav = float(doc.xpath(x_sigmav)[0].text)

        e = 1.602176634e-19 # elementary charge
        dPEda = 0.25*etat*(Ealpha+En+ELi)*n**2*sigmav*(2*np.pi**2*R0*2*a)*e
        dPEdR0 = 0.25*etat*(Ealpha+En+ELi)*n**2*sigmav*(2*np.pi**2*a**2)*e


        partials = Partials()
        partials.declare_partials(x_PE, [x_a, x_R0],
                                  [dPEda, dPEdR0])
        partials.write(partials_file)
