#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import contains_inanyorder

from nti.contenttypes.reports.reports import BasicReport
from nti.contenttypes.reports.reports import InstructorReport 

from nti.externalization.externalization import to_external_object
from nti.externalization.externalization import StandardExternalFields

from nti.contenttypes.reports.tests import ContentTypesReportsLayerTest
from nti.contenttypes.reports.tests import _ITestInterface

from zope import interface

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
        #Create example object and make an external object
        report=BasicReport(u"TestBasic", u"TestBasicDescription", _ITestInterface, u"TestPermission", [u"csv", u"pdf"])
        ext_obj=to_external_object(report)
        
        #Be sure that the external object has the right specs
        assert_that(ext_obj, has_entries(CLASS, BasicReport.__name__, 
                                         u"name", u"TestBasic", 
                                         u"description", u"TestBasicDescription", 
                                         u"interface_context", _ITestInterface.__name__,
                                         u"permission", u"TestPermission",
                                         u"supported_types",contains_inanyorder(u"csv", u"pdf")))
    
    def test_instructor_report_ext(self):
        """
        Test the externalization of InstructorReport
        """
        #Create example object and make an external object
        ins_report=InstructorReport(u"TestBasic", u"TestBasicDescription", _ITestInterface, u"TestPermission", [u"csv", u"pdf"])
        ext_obj=to_external_object(ins_report)
        
        #Be sure that the external object has all the right specs
        assert_that(ext_obj, has_entries(CLASS, InstructorReport.__name__, 
                                        u"name", u"TestBasic", 
                                        u"description", u"TestBasicDescription", 
                                        u"interface_context", _ITestInterface.__name__,
                                        u"permission", u"TestPermission",
                                        u"supported_types",contains_inanyorder(u"csv", u"pdf")))