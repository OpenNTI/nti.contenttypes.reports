#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six

from zope import component
from zope import interface

from nti.contenttypes.reports.interfaces import IReport

from nti.externalization.externalization import StandardExternalFields

from nti.externalization.interfaces import IExternalObjectDecorator

from nti.externalization.singleton import SingletonMetaclass

ITEMS = StandardExternalFields.ITEMS


@six.add_metaclass(SingletonMetaclass)
@component.adapter(IReport)
@interface.implementer(IExternalObjectDecorator)
class _ReportDecorator(object):

    def __init__(self, *args):
        pass

    def decorateExternalObject(self, original, external):
        external['contexts'] = {
            ITEMS: [x.__name__ for x in original.contexts or ()]
        }
