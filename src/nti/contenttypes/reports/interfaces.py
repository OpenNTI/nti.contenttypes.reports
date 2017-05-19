#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: interfaces.py 111853 2017-05-01 22:57:24Z carlos.sanchez $
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface
from nti.schema.field import TextLine
from nti.schema.field import List
from nti.schema.field import Object
from nti.contenttypes.courses.interfaces import ICourseInstance

class IReport(interface.Interface):
    """
    The base interface for a report object. This contains all the basic metadata
    of reports that all report objects implement.
    """
    name=TextLine(title=u"The name of the report",
                   required=True)
    description=TextLine(title=u"The client-visible description of the report.",
                          required=True)
    interface_context=Object(interface.Interface,
                             title=u"The context within which the report operates",
                             required=True)
    permission=TextLine(title=u"The permission level required to access this report",
                        required=True)
    supported_types=List(title=u"The supported file types that this report can be output to",
                         unique=True,
                         value_type=TextLine(title=u"A file type (csv,pdf,etc)"),
                         required=True)
    
    def _predicate(context, user):
        """
        Evaluate if the user has the correct permissions for this context
        """
    