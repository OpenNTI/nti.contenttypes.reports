#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
from distutils.tests import support
__docformat__ = "restructuredtext en"

import functools
import importlib
import os

from zope import component
from zope import interface

from zope.dottedname.resolve import resolve

from zope.component.zcml import utility

from zope.configuration.fields import Tokens
from zope.configuration.fields import GlobalObject

from nti.contenttypes.reports.interfaces import IReport

from nti.contenttypes.reports.reports import BasicReport

from nti.schema.field import TextLine


class IRegisterReport(interface.Interface):
    """
    Interface representing a registration of a new report, defining behavior of
    the various fields
    """
    name = TextLine(title=u"The name of the report",
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
    registration_name = TextLine(
        title=u"optional registration name of new report", required=False)


def registerReport(_context, name, description, interface_context, permission, supported_types, registration_name=""):
    """
    Take the items from ZCML, turn it into a report object and register it as a 
    new utility in the current context
    """
    # Create the Report object to be used as a utility
    factory = functools.partial(BasicReport,
                                name=name,
                                description=description,
                                interface_context=interface_context,
                                permission=permission,
                                supported_types=supported_types)

    # Register the object has a utility
    utility(_context, provides=IReport,
            factory=factory, name=registration_name)
