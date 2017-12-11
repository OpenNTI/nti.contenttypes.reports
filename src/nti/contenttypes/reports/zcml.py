#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import functools

from zope import interface

from zope.component.zcml import utility
from zope.component.zcml import subscriber

from zope.configuration.fields import Tokens
from zope.configuration.fields import GlobalObject

from zope.interface.interface import InterfaceClass

from zope.security.zcml import Permission

from nti.contenttypes.reports._compat import text_

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportContext

from nti.contenttypes.reports.reports import BaseReport

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
                            required=True)

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


def registerReport(_context, name, title, description, contexts,
                   permission, supported_types, registration_name=None,
                   report_class=BaseReport, report_interface=IReport, rel=None):
    """
    Take the items from ZCML, turn it into a report object and register it as a
    new utility in the current context
    """

    if registration_name is None:
        registration_name = name

    contexts = tuple(contexts)
    supported_types = tuple(set(text_(s) for s in supported_types or ()))

    # Create the Report object to be used as a subscriber
    factory = functools.partial(report_class,
                                name=text_(name),
                                title=text_(title),
                                rel=text_(rel),
                                permission=text_(permission),
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
