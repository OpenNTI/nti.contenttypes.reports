#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

import functools
import mimetypes

from six import text_type as text_

from zope import interface

from zope.component.zcml import utility
from zope.component.zcml import subscriber

from zope.configuration.fields import Tokens
from zope.configuration.fields import GlobalObject

from zope.interface.interface import InterfaceClass

from zope.security.zcml import Permission

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportContext

from nti.contenttypes.reports.reports import BaseReport

from nti.mimetype.schema import rfc2047MimeTypeConstraint

from nti.schema.field import TextLine

logger = __import__('logging').getLogger(__name__)


class IRegisterReport(interface.Interface):
    """
    Interface representing a registration of a new report, defining behavior of
    the various fields
    """

    name = TextLine(title=u"The name of the report",
                    required=True)

    title = TextLine(title=u"The title for the report",
                     required=True)

    description = TextLine(title=u"The client-visible description of the report.",
                           required=True)

    rel = TextLine(title=u"The href rel this report can be found on.",
                   required=False)

    contexts = Tokens(title=u"The contexts for this report",
                      value_type=GlobalObject(
                          title=u"The context within which the report operates"),
                      unique=True,
                      required=True)

    permission = Permission(title=u"The permission level required to access this report",
                            required=False)

    supported_types = Tokens(value_type=TextLine(title=u"A supported type for this report"),
                             title=u"The list of supported types for this report",
                             unique=True,
                             required=True)

    registration_name = TextLine(title=u"optional registration name of new report",
                                 required=False)

    report_class = GlobalObject(title=u"The type of report the factory should generate",
                                required=False)

    report_interface = GlobalObject(title=u"The interface the factory provides",
                                    required=False)


def guess_type(url, strict=True):
    return mimetypes.guess_type(url, strict) if url else (None, None)


def ensure_mimetype(report_type):
    mime_type = report_type
    if not rfc2047MimeTypeConstraint(report_type):
        logger.warning(
            'DEPRECATED Please update report registrations to use mimetypes'
        )
        fake_url = report_type if '.' in report_type else 'fake.' + report_type
        mime_type = guess_type(fake_url)[0]
        logger.warning(
            'Guessed mimetype of %s for %s', mime_type, report_type
        )
    assert mime_type, 'Unsupported report type %s' % report_type
    return mime_type


def registerReport(_context, name, title, description, contexts,
                   supported_types, registration_name=None, permission=None,
                   report_class=BaseReport, report_interface=IReport, rel=None):
    """
    Take the items from ZCML, turn it into a report object and register it as a
    new utility in the current context
    """
    contexts = tuple(contexts)
    rel = text_(rel) if rel else None
    permission = text_(permission) if permission else None
    supported_types = tuple(
        {text_(ensure_mimetype(s)) for s in supported_types or ()}
    )
    registration_name = name if registration_name is None else registration_name

    # Create the Report object to be used as a subscriber
    factory = functools.partial(report_class,
                                rel=rel,
                                name=text_(name),
                                title=text_(title),
                                permission=permission,
                                description=text_(description),
                                supported_types=supported_types,
                                contexts=contexts,)

    assert (type(provided) is InterfaceClass for provided in contexts), \
           "Invalid interface"

    assert (IReportContext in provided.__bases__ for provided in contexts), \
           "Invalid report context interface"

    # Register the object as a subscriber
    for provided in contexts:
        subscriber(_context, provides=report_interface,
                   factory=factory, for_=(provided,))

    # Also register as utility to fetch all
    utility(_context, provides=report_interface,
            factory=factory, name=registration_name)
