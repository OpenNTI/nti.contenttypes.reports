#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from zope import interface

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportContext

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.base._compat import text_

@interface.implementer(IReportContext)
class ReportContext(object):
    """
    Concrete class representing a report context
    """
    createDirectFieldProperties(IReportContext)
    
    def __init__(self, interface_context):
        self.context = interface_context

@interface.implementer(IReport)
class BasicReport(object):
    """
    The concrete representation of a Report object.
    """
    createDirectFieldProperties(IReport)

    def __init__(self, name, description, interface_context, permission, supported_types):
        self.name = text_(name)
        self.description = text_(description)
        self.interface_context = ReportContext(interface_context)
        self.permission = text_(permission)
        self.supported_types = [text_(s) for s in supported_types]

    def predicate(self, context, user):
        """
        Evaluate if the user has the correct permissions for this context
        """
        pass
