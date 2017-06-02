#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface
from zope import component

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportContext
from nti.contenttypes.reports.interfaces import IReportPredicate

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured


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


def evaluate_permission(report, context, user):
    """
    Evaluate whether a user has permissions on this report.
    Aggregate all permissions from all permissions
    providers. All must be true to grant permission
    """

    # Grab the permission providers
    predicates = list(component.subscribers((report, user), IReportPredicate))

    # If there are none, don't grant permission
    if not predicates:
        return False

    return all((p.evaluate(report, context, user) for p in predicates))
