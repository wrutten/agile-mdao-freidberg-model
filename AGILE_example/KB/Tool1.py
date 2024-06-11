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
from config import root_tag, x_par1, x_par2, x_O1

## Change the name to match the file name
class Tool1(AbstractDiscipline):

## These properties can be changed if necessary
    @property
    def creator(self):
        return u'W.J. Rutten'

    @property
    def description(self):
        return u'Example tool 1'

    @property
    def supplies_partials(self):
        return True

## This should be changed to match the I/O .xml files
    def generate_input_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_par1, 0.)


        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def generate_output_xml(self):
        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)

        xml_safe_create_element(doc, x_par2, 0.)
        xml_safe_create_element(doc, x_O1, 0.)

        return etree.tostring(doc, encoding='utf-8', pretty_print=True, xml_declaration=True)

## Declare partials for all input->output combinations
    def generate_partials_xml(self):
        partials = Partials()
        partials.declare_partials(x_O1, [x_par1]) # dO1/dpar1
        partials.declare_partials(x_par2, [x_par1]) # dpar2/dpar1
        return partials.get_string()

## This method executes the tool itself. Adapt it to take the right parameters as defined before.
    @staticmethod
    def execute(in_file, out_file):
        doc = etree.parse(in_file)
        par1 = float(doc.xpath(x_par1)[0].text)


        # The actual equation
        par2 = par1
        obj = par1+par2

        root = etree.Element(root_tag)
        doc = etree.ElementTree(root)
        xml_safe_create_element(doc, x_O1, obj)
        xml_safe_create_element(doc, x_par2, par2)

        doc.write(out_file, encoding='utf-8', pretty_print=True, xml_declaration=True)

## This method executes the gradient computation over the tool. Also adapt as necessary
    def linearize(in_file, partials_file):
        doc = etree.parse(in_file)

        # Trivial gradients in this example of course
        dO1dpar1 = 1
        dpar2dpar1 = 1

        partials = Partials()
        partials.declare_partials(x_O1, [x_par1],
                                  [dO1dpar1])
        partials.declare_partials(x_par2, [x_par1],
                                  [dpar2dpar1])
        partials.write(partials_file)
