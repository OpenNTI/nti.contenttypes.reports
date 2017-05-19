#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
from _codecs import register
__docformat__ = "restructuredtext en"

from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import not_none
from hamcrest import contains_inanyorder

from zope import component

from zope.configuration import config
from zope.configuration import xmlconfig 

from nti.contenttypes.reports.tests import _ITestInterface
from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest

from nti.contenttypes.reports.zcml import registerReport

from nti.contenttypes.reports.interfaces import IReport

#Example ZCML file that would call the registerReport directive
HEAD_ZCML_STRING = """
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
                            interface_context=".tests._ITestInterface"
                            permission="TestPermission"
                            supported_types="csv, 
                                             pdf" />
    </configure>
</configure>

"""

class TestZcml(ContentTypesReportsLayerTest):
    """
    Reponsible for testing the ZCML processing of registerReport-involved directives
    """
    def setUp(self):
        """
        Set up test cases
        """
        self.layer.setUp()
    
    def test_register_report(self):
        """
        Responsible for testing that registering a report results in the proper utilities
        """
        
        #Using the above ZCML string, set up the temporary configuration and run the string
        #through ZCML processor
        context=config.ConfigurationMachine()
        context.package = self.get_configuration_package()
        xmlconfig.registerCommonDirectives(context)
        xmlconfig.string(HEAD_ZCML_STRING, context)
       
        #Get all utilities that are registered to an IReport object
        uti=component.getUtility(IReport)
        
        #Be sure that the utilitiy we ended up with matches the test registration in the
        #sample ZCML
        assert_that(uti, not_none())
        assert_that(uti, has_property('name', u'TestReport'))
        assert_that(uti, has_property("description", u"TestDescription"))
        assert_that(uti, has_property("interface_context", _ITestInterface))
        assert_that(uti, has_property("supported_types", contains_inanyorder(u"pdf", u"csv")))
        assert_that(uti, has_property("permission", u"TestPermission"))
        
        
