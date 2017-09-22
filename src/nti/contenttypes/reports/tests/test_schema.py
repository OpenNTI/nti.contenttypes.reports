#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.contenttypes.reports.interfaces import IReportContext

from nti.contenttypes.reports.schema import ValidInterface

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest


class TestSchema(ContentTypesReportsLayerTest):

    module = "nti.contenttypes.reports.tests"

    def test_valid_function(self):
        schema = ValidInterface(IReportContext)
        schema.fromUnicode(self.module + ".ITestReportContext")
