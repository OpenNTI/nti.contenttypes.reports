#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import has_entry
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import contains_inanyorder

from nti.contenttypes.reports.reports import BaseReport

from nti.externalization.externalization import to_external_object
from nti.externalization.externalization import StandardExternalFields

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest

from nti.contenttypes.reports.tests import ITestReportContext
from nti.contenttypes.reports.tests import ITestSecondReportContext

CLASS = StandardExternalFields.CLASS
ITEMS = StandardExternalFields.ITEMS


class TestExternal(ContentTypesReportsLayerTest):
    """
    Run unit tests on the two derived IReport classes to be sure we can make them
    externally facing
    """

    def test_basic_report_ext(self):
        """
        Test the externalization of BasicReport
        """
        # Create example object and make an external object
        report = BaseReport(name=u"TestBasic",
                            title=u"Test Report",
                            description=u"TestBasicDescription",
                            contexts=(ITestReportContext,
                                      ITestSecondReportContext),
                            permission=u"TestPermission",
                            supported_types=[u"csv", u"pdf"])
        ext_obj = to_external_object(report)

        # Be sure that the external object has the right specs
        assert_that(ext_obj,
                    has_entries(CLASS, "BaseReport",
                                "name", "TestBasic",
                                "title", "Test Report",
                                "description", "TestBasicDescription",
                                "contexts", has_entry(ITEMS,
                                                    contains_inanyorder(ITestReportContext.__name__,
                                                                        ITestSecondReportContext.__name__)),
                                "supported_types", contains_inanyorder("csv", "pdf")))
