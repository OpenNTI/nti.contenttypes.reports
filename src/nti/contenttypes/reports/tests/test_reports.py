#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that

from zope import component
from zope import interface

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportPredicate
from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.contenttypes.reports.reports import BaseReport
from nti.contenttypes.reports.reports import ReportContext

from nti.contenttypes.reports.reports import evaluate_predicate
from nti.contenttypes.reports.reports import evaluate_permission

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

    def evaluate(self, *unused_args):  # pylint: disable=unused-argument
        return False


@interface.implementer(IReportPredicate)
class ReportPredicate(object):

    def __init__(self, *args):
        pass

    def evaluate(self, *unused_args):  # pylint: disable=unused-argument
        return True


class IUser(interface.Interface):  # pylint: disable=inherit-non-class
    pass


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

    def test_evaluate_permission(self):
        report = BaseReport(name=u"TestBasic",
                            title=u"Test Report",
                            description=u"TestBasicDescription",
                            contexts=(ITestReportContext,
                                      ITestSecondReportContext),
                            permission=u"TestPermission",
                            supported_types=[u"csv", u"pdf"])
        assert_that(evaluate_permission(report, None, None),
                    is_(False))

        @interface.implementer(IUser)
        class User(object):
            pass

        sm = component.getGlobalSiteManager()
        sm.registerSubscriptionAdapter(ReportPredicate,
                                       (IReport, interface.Interface),
                                       IReportPredicate)
        assert_that(evaluate_permission(report, TestReportContext(), User()),
                    is_(True))

        sm.unregisterSubscriptionAdapter(ReportPredicate,
                                         (IReport, interface.Interface),
                                         IReportPredicate)
