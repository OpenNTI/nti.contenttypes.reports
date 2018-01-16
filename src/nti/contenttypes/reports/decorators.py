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

from nti.externalization.externalization import StandardExternalFields

from nti.externalization.interfaces import IExternalObjectDecorator

from nti.externalization.singleton import Singleton

ITEMS = StandardExternalFields.ITEMS


@component.adapter(IReport)
@interface.implementer(IExternalObjectDecorator)
class _ReportDecorator(Singleton):

    def decorateExternalObject(self, original, external):
        if 'rel' not in external:
            external['rel'] = original.rel or "report-%s" % original.name
        external['contexts'] = {
            ITEMS: [x.__name__ for x in original.contexts or ()]
        }
