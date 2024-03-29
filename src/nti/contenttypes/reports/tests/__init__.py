#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

import zope.testing.cleanup

from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin


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


from nti.contenttypes.reports.interfaces import IReportContext


class ITestReportContext(IReportContext):
    """
    Test interface to be used in place of other interfaces in unit tests
    """


class ITestSecondReportContext(IReportContext):
    """
    Test interface to test reports with multiple interface contexts
    """


from zope import interface


class ITest(interface.Interface):  # pylint: disable=inherit-non-class
    pass
