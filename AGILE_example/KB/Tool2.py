#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Trivial example to show how to wrap tools for the AGILE framework
"""
from __future__ import absolute_import, division, print_function

import numpy as np
from lxml import etree

from openlego.api import AbstractDiscipline
from openlego.utils.xml_utils import xml_safe_create_element
from openlego.partials.partials import Partials

## Change the import statement to import the right parameter names.
from config import root_tag, x_par1, x_par2

## Change the name to match the file name
class Tool2(AbstractDiscipline):

## These properties can be changed if necessary
    @property
    def creator(self):
        return u'W.J. Rutten'

    @property
    def description(self):
        return u'Example tool 2'

    @property
    def supplies_partials(self):
        return False

## This should be changed to match the I/O .xml files
    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_par2, 0.)


        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_par1, 0.)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)


## This method executes the tool itself. Adapt it to take the right parameters as defined before.
    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        par2 = float(doc.xpath(x_par2)[0].text)


        # The actual equation
        par1 = par2

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_par1, par1)

        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)
