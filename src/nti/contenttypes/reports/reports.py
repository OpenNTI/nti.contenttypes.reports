#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportContext

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

from nti.dataserver.authorization_acl import has_permission


@interface.implementer(IReportContext)
class ReportContext(SchemaConfigured):
    """
    Concrete class representing a report context
    """
    createDirectFieldProperties(IReportContext)


@interface.implementer(IReport)
class BaseReport(SchemaConfigured):
    """
    The concrete representation of a Report object.
    """
    createDirectFieldProperties(IReport)

    def __init__(self, *args, **kwargs):
        SchemaConfigured.__init__(self, **kwargs)

    def predicate(self, context, user):
        return has_permission(self.permission, context, user)
