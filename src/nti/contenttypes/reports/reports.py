#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.contenttypes.reports.interfaces import IReport
from nti.schema.fieldproperty import createDirectFieldProperties
from zope import interface

@interface.implementer(IReport)
class BasicReport(object):
    """
    The concrete representation of a Report object.
    """
    createDirectFieldProperties(IReport)
    
    def __init__(self, name, description, interface_context, permission, supported_types):
        self.name=name
        self.description=description
        self.interface_context=interface_context
        self.permission=permission
        self.supported_types=supported_types
    
    def _predicate(self, context, user):
        """
        Evaluate if the user has the correct permissions for this context
        """
        pass

class InstructorReport(BasicReport):
    """
    The concrete report accessible by instructors?
    """
    
    def __init__(self, name, description, interface_context, permission, supported_types):
        super(self.__class__, self).__init__(name, description, interface_context, permission, supported_types)