#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import equal_to

from nti.contenttypes.reports.interfaces import IReportContext

from nti.contenttypes.reports.schema import ValidInterface
from nti.contenttypes.reports.schema import ValidCondition

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest


def test_condition():
    return True

class TestSchema(ContentTypesReportsLayerTest):

    def test_valid_function(self):
        schema = ValidInterface(IReportContext)
        schema.fromUnicode("nti.contenttypes.reports.tests.ITestReportContext")

    def test_valid_condition(self):
        condition = ValidCondition()
        f = condition.fromUnicode("nti.contenttypes.reports.tests.test_schema.test_condition")
        assert_that(f(), equal_to(True))