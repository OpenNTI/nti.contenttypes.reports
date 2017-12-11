#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportContext
from nti.contenttypes.reports.interfaces import IReportPredicate
from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

logger = __import__('logging').getLogger(__name__)


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

    # pylint: disable=unused-argument
    def __init__(self, *unused_args, **kwargs):  # specify args
        SchemaConfigured.__init__(self, **kwargs)


def evaluate_permission(report, context, user):
    """
    Evaluate whether a user has permissions on this report. Aggregate all
    permissions from all permissions providers. All must be true to grant
    permission.
    """
    # Grab the permission providers
    predicates = list(component.subscribers((report, user), IReportPredicate))
    # If there are none, don't grant permission
    if not predicates:
        return False
    return all((p.evaluate(report, context, user) for p in predicates))


def evaluate_predicate(report, context, user):
    """
    Evaluate if in this context, this user should  be provided with a link to a
    report.
    """
    predicates = list(component.subscribers((context,), IReportAvailablePredicate))
    if not predicates:
        return True
    return all(p.evaluate(report, context, user) for p in predicates)
