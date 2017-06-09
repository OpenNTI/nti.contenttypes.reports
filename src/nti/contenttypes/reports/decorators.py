#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import component
from zope import interface

from nti.contenttypes.reports.interfaces import IReport

from nti.externalization.externalization import StandardExternalFields

from nti.externalization.interfaces import IExternalObjectDecorator

from nti.externalization.singleton import SingletonDecorator

CLASS = StandardExternalFields.CLASS
ITEMS = StandardExternalFields.ITEMS


@component.adapter(IReport)
@interface.implementer(IExternalObjectDecorator)
class _ReportDecorator(object):

    __metaclass__ = SingletonDecorator

    def decorateExternalObject(self, original, external):
        contexts = []
        for context in original.contexts:
            contexts.append(context.__name__)
        external['contexts'] = {
            ITEMS: contexts
        }
        if original.condition is not None:
            external['condition'] = {
                CLASS: original.condition.__name__
            }
