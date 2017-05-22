#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.dottedname import resolve as dottedname

from zope.interface.interface import InterfaceClass

from zope.schema import Field

from zope.schema.interfaces import WrongType
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import SchemaNotProvided

from nti.schema.field import Object


@interface.implementer(IFromUnicode)
class ValidInterface(Object):

    _type = InterfaceClass
    
    def __init__(self, schema, **kw):
        if type(schema) is not InterfaceClass:
            raise WrongType(schema, self._type, self.__name__)

        self.schema = schema
        Field.__init__(self, **kw)

    def _validate(self, value):
        if self._type is not None and not isinstance(value, self._type):
            raise WrongType(value, self._type, self.__name__)

        if self.schema not in value.__bases__:
            raise SchemaNotProvided

    def fromUnicode(self, value):
        value = dottedname(value.strip())
        self._validate(value)
        return value