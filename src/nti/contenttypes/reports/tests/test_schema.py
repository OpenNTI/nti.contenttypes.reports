#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.contenttypes.reports.interfaces import IReportContext

from nti.contenttypes.reports.schema import ValidInterface

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest


class TestSchema(ContentTypesReportsLayerTest):

    def test_from_unicode(self):
        schema = ValidInterface(IReportContext)
        schema.fromUnicode("nti.contenttypes.reports.tests.ITestReportContext")
