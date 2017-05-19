#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin

from zope import interface

import zope.testing.cleanup


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

class _ITestInterface(interface.Interface):
    """
    Test interface to be used in place of other interfaces in unit tests
    """
