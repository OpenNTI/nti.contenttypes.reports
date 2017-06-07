#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import equal_to

from nti.contenttypes.reports.interfaces import IReportContext
from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.contenttypes.reports.schema import ValidInterface
from nti.contenttypes.reports.schema import ValidPredicate

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest

class TestSchema(ContentTypesReportsLayerTest):

    def test_valid_function(self):
        schema = ValidInterface(IReportContext)
        schema.fromUnicode("nti.contenttypes.reports.tests.ITestReportContext")
    
    def test_valid_predicate(self):
        schema = ValidPredicate(IReportAvailablePredicate)
        schema.fromUnicode("nti.contenttypes.reports.tests.TestReportPredicate")