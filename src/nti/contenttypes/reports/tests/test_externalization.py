#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import contains_inanyorder

from nti.contenttypes.reports.reports import BasicReport

from nti.externalization.externalization import to_external_object
from nti.externalization.externalization import StandardExternalFields

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest
from nti.contenttypes.reports.tests import ITestInterface

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
        report = BasicReport("TestBasic", "TestBasicDescription",
                             ITestInterface, "TestPermission", ["csv", "pdf"])
        ext_obj = to_external_object(report)
        # Be sure that the external object has the right specs
        assert_that(ext_obj, has_entries(CLASS, BasicReport.__name__,
                                         "name", "TestBasic",
                                         "description", "TestBasicDescription",
                                         "interface_context", has_entries(CLASS, ITestInterface.__name__),
                                         "permission", "TestPermission",
                                         "supported_types", contains_inanyorder("csv", "pdf")))
