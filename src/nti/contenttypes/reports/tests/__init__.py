#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from zope import interface

import zope.testing.cleanup

from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin

from nti.contenttypes.reports.reports import BaseReportAvailablePredicate


class SharedConfiguringTestLayer(ZopeComponentLayer,
                                 ConfiguringLayerMixin):

    set_up_packages = ('nti.contenttypes.reports',)

    @classmethod
    def setUp(cls):
        cls.setUpPackages()

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        zope.testing.cleanup.cleanUp()

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


import unittest

from nti.testing.base import AbstractTestBase


class ContentTypesReportsLayerTest(unittest.TestCase):

    layer = SharedConfiguringTestLayer
    get_configuration_package = AbstractTestBase.get_configuration_package.__func__


from nti.contenttypes.reports.interfaces import IReportContext
from nti.contenttypes.reports.interfaces import IReportAvailablePredicate


class ITestReportContext(IReportContext):
    """
    Test interface to be used in place of other interfaces in unit tests
    """


class ITestSecondReportContext(IReportContext):
    """
    Test interface to test reports with multiple interface contexts
    """


class TestReportPredicate(BaseReportAvailablePredicate):
    """
    Test predicate for if a report should be decorated
    """
