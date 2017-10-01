#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from zope import component
from zope import interface

from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.contenttypes.reports.reports import BaseReport
from nti.contenttypes.reports.reports import ReportContext

from nti.contenttypes.reports.reports import evaluate_predicate

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest

from nti.contenttypes.reports.tests import ITestReportContext
from nti.contenttypes.reports.tests import ITestSecondReportContext


@interface.implementer(ITestReportContext)
class TestReportContext(ReportContext):
    pass


@interface.implementer(IReportAvailablePredicate)
class ReportAvailablePredicate(object):

    def __init__(self, *args):
        pass

    def evaluate(self, *unused_args):
        return False


class TestReports(ContentTypesReportsLayerTest):

    def test_predicates(self):
        report = BaseReport(name=u"TestBasic",
                            title=u"Test Report",
                            description=u"TestBasicDescription",
                            contexts=(ITestReportContext,
                                      ITestSecondReportContext),
                            permission=u"TestPermission",
                            supported_types=[u"csv", u"pdf"])
        assert_that(evaluate_predicate(report, None, None),
                    is_(True))

        sm = component.getGlobalSiteManager()
        sm.registerSubscriptionAdapter(ReportAvailablePredicate,
                                       (ITestReportContext,),
                                       IReportAvailablePredicate)
        assert_that(evaluate_predicate(report, TestReportContext(), None),
                    is_(False))

        sm.unregisterSubscriptionAdapter(ReportAvailablePredicate,
                                         (ITestReportContext,),
                                         IReportAvailablePredicate)
