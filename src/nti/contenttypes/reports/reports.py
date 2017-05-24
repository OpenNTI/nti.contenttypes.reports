#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportContext

from nti.contenttypes.reports.interfaces import get_report_predicate

from nti.schema.fieldproperty import createDirectFieldProperties


@interface.implementer(IReportContext)
class ReportContext(object):
    """
    Concrete class representing a report context
    """
    createDirectFieldProperties(IReportContext)


@interface.implementer(IReport)
class BasicReport(object):
    """
    The concrete representation of a Report object.
    """
    createDirectFieldProperties(IReport)

    def __init__(self, name, description, interface_context, 
                 permission, supported_types):
        self.name = name
        self.permission = permission
        self.description = description
        self.interface_context = interface_context
        self.supported_types = tuple(s for s in supported_types)

    def predicate(self, context, user):
        uber_filter = get_report_predicate(self)
        return uber_filter(context, user)
