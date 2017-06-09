#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.contenttypes.reports.interfaces import IReportContext
from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.contenttypes.reports.schema import ValidInterface
from nti.contenttypes.reports.schema import ValidPredicate

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest


class TestSchema(ContentTypesReportsLayerTest):

    module = "nti.contenttypes.reports.tests"

    def test_valid_function(self):
        schema = ValidInterface(IReportContext)
        schema.fromUnicode(self.module + ".ITestReportContext")

    def test_valid_predicate(self):
        schema = ValidPredicate(IReportAvailablePredicate)
        schema.fromUnicode(self.module + ".TestReportPredicate")
