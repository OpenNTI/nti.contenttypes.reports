#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import functools

from zope import interface

from zope.component.zcml import utility
from zope.component.zcml import subscriber

from zope.configuration.fields import Tokens
from zope.configuration.fields import GlobalObject

from zope.interface.interface import InterfaceClass

from nti.base._compat import text_

from nti.contenttypes.reports.interfaces import IReport
from nti.contenttypes.reports.interfaces import IReportContext
from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.contenttypes.reports.reports import BaseReport

from nti.schema.field import TextLine


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

    interface_context = GlobalObject(title=u"The context within which the report operates",
                                     required=True)

    permission = TextLine(title=u"The permission level required to access this report",
                          required=True)

    supported_types = Tokens(value_type=TextLine(title=u"A supported type for this report"),
                             title=u"The list of supported types for this report",
                             unique=True,
                             required=True)
    
    condition = GlobalObject(title=u"A function that must return true for this report to be decorated",
                             required=False)

    registration_name = TextLine(title=u"optional registration name of new report",
                                 required=False)
    
    report_class = GlobalObject(title=u"The type of report the factory should generate",
                                required=False)
    
    report_interface = GlobalObject(title=u"The interface the factory provides",
                                    required=False)


def registerReport(_context, name, title, description, interface_context,
                   permission, supported_types, condition=None, registration_name=None,
                   report_class=BaseReport, report_interface=IReport):
    """
    Take the items from ZCML, turn it into a report object and register it as a
    new utility in the current context
    """

    if registration_name is None:
        registration_name = name

    supported_types = tuple(set(text_(s) for s in supported_types or ()))

    # Create the Report object to be used as a subscriber
    factory = functools.partial(report_class,
                                name=text_(name),
                                title=text_(title),
                                permission=text_(permission),
                                description=text_(description),
                                supported_types=supported_types,
                                condition=condition,
                                interface_context=interface_context,)

    assert type(interface_context) is InterfaceClass, \
           "Invalid interface"

    assert IReportContext in interface_context.__bases__, \
           "Invalid report context interface"

    # Register the object as a subscriber
    subscriber(_context, provides=report_interface,
               factory=factory, for_=(interface_context,))

    # Also register as utility to fetch all
    utility(_context, provides=report_interface,
            factory=factory, name=registration_name)
