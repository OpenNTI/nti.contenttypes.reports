#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.externalization.interfaces import IExternalObject
from nti.externalization.interfaces import LocatedExternalDict

from nti.externalization.externalization import StandardExternalFields

from nti.contenttypes.reports.interfaces import IReportContext

CLASS = StandardExternalFields.CLASS


@component.adapter(IReportContext)
@interface.implementer(IExternalObject)
class _ReportExternalizer(object):
    """
    Defines the externalization of an IReport-based object.
    """

    # Tell Python to hold space for an object
    __slots__ = ('context', )

    def __init__(self, context):
        # Set the object to be externalized
        self.context = context

    def toExternalObject(self,  *args, **kwargs):
        """
        Performs the externalization of an IReport object
        """
        # Create space to hold the items that are front facing
        result = LocatedExternalDict()
        # From the object, get all needed attributes and save them
        result[CLASS] = self.context.context.__name__
        return result
