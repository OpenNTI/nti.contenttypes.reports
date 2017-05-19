#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

import functools

from nti.contenttypes.reports.interfaces import IReport

from nti.contenttypes.reports.reports import BasicReport

from zope.component.zcml import utility

from zope import component
from zope import interface

from nti.schema.field import TextLine

import importlib
import os

class IRegisterReport(interface.Interface):
    """
    Interface representing a registration of a new report.
    Notice the differences form IReport: All items are text lines.
    More complex pieces will need to be parsed out to be used for registration.
    """
    name=TextLine(title=u"The name of the report",
                   required=True)
    description=TextLine(title=u"The client-visible description of the report.",
                          required=True)
    interface_context=TextLine(title=u"The context within which the report operates",
                             required=True)
    permission=TextLine(title=u"The permission level required to access this report",
                        required=True)
    supported_types=TextLine(title=u"The supported file types that this report can be output to",
                         required=True)
    registration_name=TextLine(title=u"optional registration name of new report", required=False)
    
def registerReport(_context, name, description, interface_context, permission, supported_types, registration_name=""):
    """
    Take the items from ZCML, turn it into a report object and register it as a 
    new utility in the current context
    """
    
    #Parse out the interface given as the interface_context into the proper class object
    _interface=getClassFromUnicode(interface_context)
    
    #Parse out the type list into a Python list
    types_list=''.join(supported_types.split()).split(',')
    
    #Create the Report object to be used as a utility
    factory=functools.partial(BasicReport,
                              name=name,
                              description=description,
                              interface_context=_interface,
                              permission=permission,
                              supported_types=types_list)
    
    #Register the object has a utility
    utility(_context, provides=IReport, factory=factory, name=registration_name)

def getClassFromUnicode(unicode_str):
    """
    Turns the string class name/path into the proper class object
    """
    try:
        #If it is an absolute path, just split the class from the 
        #module and we can directly import
        _package, _class_name=unicode_str.rsplit('.', 1)
        _module=importlib.import_module(_package)
        _interface=getattr(_module, _class_name)
    except (ImportError, TypeError):
        #If that didnt work, fetch the parent directory to turn the relative
        #import into an absolute import
        _package, _class_name=unicode_str.rsplit('.', 1)
        _parent=os.path.abspath(os.path.join(os.path.realpath(_package.replace('.', '')), os.pardir)).split('/')[-1]
        _module=importlib.import_module(_package, _parent)
        _interface=getattr(_module, _class_name)
        
    #Result should be in object form
    return _interface
    