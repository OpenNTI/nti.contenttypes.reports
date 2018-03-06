#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: interfaces.py 111853 2017-05-01 22:57:24Z carlos.sanchez $
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface

from nti.contenttypes.reports.schema import ValidInterface
from nti.contenttypes.reports.schema import rfc2047MimeTypeConstraint

from nti.schema.field import Choice
from nti.schema.field import ListOrTuple
from nti.schema.field import DecodingValidTextLine as TextLine


class IReportContext(interface.Interface):
    """
    Wraps the context of an IReport around a class to externalize
    specially
    """


class IReportPredicate(interface.Interface):
    """
    Subscriber for report objects has the correct permissions for this context
    """

    def evaluate(report, context, user):
        """
        Evaluate if the user has the correct permissions for this context
        """


class IReportAvailablePredicate(IReportPredicate):
    """
    Evaluate whether a report should be decorated onto
    a context.
    """


class IReport(interface.Interface):
    """
    The base interface for a report object. This contains all the basic metadata
    of reports that all report objects implement.
    """

    name = TextLine(title=u"The name of the report",
                    required=True)

    title = TextLine(title=u"The title of the report",
                     required=True)

    description = TextLine(title=u"The client-visible description of the report.",
                           required=True)

    rel = TextLine(title=u"The href rel this report can be found on.",
                   required=False)

    contexts = ListOrTuple(title=u"Contexts for this report",
                           value_type=ValidInterface(IReportContext,
                                                     title=u"The context within which the report operates"),
                           unique=True,
                           required=True)
    contexts.setTaggedValue('_ext_excluded_out', True)

    permission = Choice(vocabulary='Permission Ids',
                        title=u"The permission level required to access this report",
                        required=False)
    permission.setTaggedValue('_ext_excluded_out', True)

    supported_types = ListOrTuple(title=u"The supported file types that this report can be output to",
                                  unique=True,
                                  value_type=TextLine(title=u"A mimetype supported by this report",
                                                      constraint=rfc2047MimeTypeConstraint),
                                  required=True)
