#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from zope.interface import Interface

from zope.schema.interfaces import WrongType
from zope.schema.interfaces import InvalidDottedName
from zope.schema.interfaces import SchemaNotProvided

from nti.contenttypes.reports.interfaces import IReportContext

from nti.contenttypes.reports.schema import ValidInterface

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest

class IBasicInterface(Interface):
    pass

class TestSchema(ContentTypesReportsLayerTest):

    module = "nti.contenttypes.reports.tests"

    def test_valid_function(self):
        schema = ValidInterface(IReportContext)
        schema.fromUnicode(self.module + ".ITestReportContext")

        with self.assertRaises(WrongType):
            ValidInterface(object())

        with self.assertRaises(WrongType):
            schema.fromUnicode(self.module)

        with self.assertRaises(SchemaNotProvided):
            schema.fromUnicode(self.module + ".ITest")

        with self.assertRaises(InvalidDottedName):
            schema.fromUnicode("1234")

    def test_any_interface(self):
        schema = ValidInterface()
        schema.fromUnicode(self.module + ".test_schema.IBasicInterface")
