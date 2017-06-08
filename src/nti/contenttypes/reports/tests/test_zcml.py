#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import not_none
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import contains_inanyorder

from zope import component
from zope import interface

from zope.configuration import config
from zope.configuration import xmlconfig

from nti.contenttypes.reports.interfaces import IReport

from nti.contenttypes.reports.reports import ReportContext
from nti.contenttypes.reports.reports import BaseReportAvailablePredicate

from nti.contenttypes.reports.tests import ITestReportContext
from nti.contenttypes.reports.tests import ITestSecondReportContext
from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest
from nti.contenttypes.reports.tests import TestReportPredicate


# Example ZCML file that would call the registerReport directive
HEAD_ZCML_STRING = u"""
<configure  xmlns="http://namespaces.zope.org/zope"
            xmlns:i18n="http://namespaces.zope.org/i18n"
            xmlns:zcml="http://namespaces.zope.org/zcml"
            xmlns:rep="http://nextthought.com/reports">

    <include package="zope.component" file="meta.zcml" />
    <include package="zope.security" file="meta.zcml" />
    <include package="zope.component" />
    <include package="." file="meta.zcml"/>

    <configure>
        <rep:registerReport name="TestReport"
                            title="Test Report"
                            description="TestDescription"
                            interface_context=".tests.ITestReportContext"
                            permission="TestPermission"
                            supported_types="csv pdf" />
        <rep:registerReport name="AnotherTestReport"
                            title="Another Test Report"
                            description="Another Test Description"
                            interface_context=".tests.ITestReportContext
                                               .tests.ITestSecondReportContext"
                            permission="TestPermission"
                            supported_types="csv pdf"
                            condition=".tests.TestReportPredicate" />
    </configure>
</configure>
"""


@interface.implementer(ITestReportContext)
class TestReportContext(ReportContext):
    pass


@interface.implementer(ITestSecondReportContext)
class TestSecondReportContext(ReportContext):
    pass


class TestZcml(ContentTypesReportsLayerTest):
    """
    Responsible for testing the ZCML processing of registerReport-involved directives
    """

    def _test_for_test_report(self, report):
        assert_that(report, has_property("name", "TestReport"))
        assert_that(report, has_property("title", "Test Report"))
        assert_that(report, has_property("description", "TestDescription"))
        assert_that(report, has_property("interface_context", not_none()))
        assert_that(report, has_property("supported_types",
                                         contains_inanyorder("pdf", "csv")))
        assert_that(report, has_property("permission", "TestPermission"))
        assert_that(report, has_property("condition", not_none()))

    def _test_for_another_report(self, report):
        assert_that(report, has_property("name", "AnotherTestReport"))
        assert_that(report, has_property("title", "Another Test Report"))
        assert_that(
            report,
            has_property(
                "description",
                "Another Test Description"))
        assert_that(report, has_property("interface_context", has_length(2)))
        assert_that(report, has_property("supported_types",
                                         contains_inanyorder("pdf", "csv")))
        assert_that(report, has_property("permission", "TestPermission"))
        assert_that(report, has_property("condition", not_none()))

    def test_register_report(self):
        """
        Responsible for testing that registering a report results in the proper utilities
        """

        # Using the above ZCML string, set up the temporary configuration and run the string
        # through ZCML processor
        context = config.ConfigurationMachine()
        context.package = self.get_configuration_package()
        xmlconfig.registerCommonDirectives(context)
        xmlconfig.string(HEAD_ZCML_STRING, context)

        test_context = TestReportContext()
        second_context = TestSecondReportContext()

        # Get all subscribers that are registered to an IReport object
        reports_test_context = component.subscribers((test_context,), IReport)
        assert_that(reports_test_context, has_length(2))
        self._test_for_test_report(reports_test_context[0])
        self._test_for_another_report(reports_test_context[1])

        reports_second_context = component.subscribers(
            (second_context,), IReport)
        assert_that(reports_second_context, has_length(1))
        self._test_for_another_report(reports_second_context[0])

        both_context_reports = component.subscribers(
            (test_context, second_context), IReport)
        assert_that(both_context_reports, has_length(0))
