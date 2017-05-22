#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import not_none
from hamcrest import contains_inanyorder

from zope import component

from zope.configuration import config
from zope.configuration import xmlconfig

from nti.contenttypes.reports.interfaces import IReport

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest


#Example ZCML file that would call the registerReport directive
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
                            description="TestDescription"
                            interface_context=".tests.ITestReportContext"
                            permission="TestPermission"
                            supported_types="csv pdf" />
    </configure>
</configure>

"""


class TestZcml(ContentTypesReportsLayerTest):
    """
    Reponsible for testing the ZCML processing of registerReport-involved directives
    """

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

        # Get all utilities that are registered to an IReport object
        uti = component.getUtility(IReport)
        
        # Be sure that the utilitiy we ended up with matches the test registration in the
        # sample ZCML
        assert_that(uti, not_none())
        assert_that(uti, has_property("name", "TestReport"))
        assert_that(uti, has_property("description", "TestDescription"))
        assert_that(uti, has_property("interface_context", not_none()))
        assert_that(uti, has_property("supported_types",
                                      contains_inanyorder("pdf", "csv")))
        assert_that(uti, has_property("permission", "TestPermission"))
