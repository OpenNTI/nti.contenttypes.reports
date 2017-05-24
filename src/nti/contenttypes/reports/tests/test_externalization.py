#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import has_entry
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import contains_inanyorder

from nti.contenttypes.reports.reports import BaseReport

from nti.externalization.externalization import to_external_object
from nti.externalization.externalization import StandardExternalFields

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest

from nti.contenttypes.reports.tests import ITestReportContext

CLASS = StandardExternalFields.CLASS


class TestExternal(ContentTypesReportsLayerTest):
    """
    Run unit tests on the two derived IReport clases to be sure we can make them
    externally facing
    """

    def test_basic_report_ext(self):
        """
        Test the externalization of BasicReport
        """
        # Create example object and make an external object
        report = BaseReport(u"TestBasic", u"TestBasicDescription",
                            ITestReportContext, u"TestPermission", 
                            [u"csv", u"pdf"])
        ext_obj = to_external_object(report)

        # Be sure that the external object has the right specs
        assert_that(ext_obj, 
                    has_entries(CLASS, "BaseReport",
                                "name", "TestBasic",
                                "description", "TestBasicDescription",
                                "interface_context", has_entry(CLASS,
                                                               ITestReportContext.__name__),
                                "permission", "TestPermission",
                                "supported_types", contains_inanyorder("csv", "pdf")))
