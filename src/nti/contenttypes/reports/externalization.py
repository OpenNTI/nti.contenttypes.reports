#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

from nti.contenttypes.reports.interfaces import IReport

from nti.externalization.interfaces import IExternalObject
from nti.externalization.interfaces import LocatedExternalDict

from nti.externalization.externalization import StandardExternalFields

from zope import component
from zope import interface

CLASS=StandardExternalFields.CLASS

@component.adapter(IReport)
@interface.implementer(IExternalObject)
class _ReportExternalizer(object):
    
    __slots__=('obj', )
    
    def __init__(self, IReportObj):
        self.obj=IReportObj
    
    def toExternalObject(self,  *args, **kwargs):
        result=LocatedExternalDict()
        result[CLASS]=self.obj.__class__.__name__
        result["name"]=self.obj.name
        result["description"]=self.obj.description
        result["interface_context"]=self.obj.interface_context.__name__
        result["permission"]=self.obj.permission
        result["supported_types"]=self.obj.supported_types
        return result
        