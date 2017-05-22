#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: interfaces.py 111853 2017-05-01 22:57:24Z carlos.sanchez $
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.schema.field import TextLine
from nti.schema.field import ListOrTuple


class IReportContext(interface.Interface):
    """
    Wraps the context of an IReport around a class to externalize
    specially
    """


class IReport(interface.Interface):
    """
    The base interface for a report object. This contains all the basic metadata
    of reports that all report objects implement.
    """

    name = TextLine(title=u"The name of the report",
                    required=True)

    description = TextLine(title=u"The client-visible description of the report.",
                           required=True)

    interface_context = interface.Attribute(u"The context within which the report operates")
    interface_context.setTaggedValue('_ext_excluded_out', True)
    
    permission = TextLine(title=u"The permission level required to access this report",
                          required=True)

    supported_types = ListOrTuple(title=u"The supported file types that this report can be output to",
                                  unique=True,
                                  value_type=TextLine(title=u"A file type (csv,pdf,etc)"),
                                  required=True)

    def predicate(context, user):
        """
        Evaluate if the user has the correct permissions for this context
        """
