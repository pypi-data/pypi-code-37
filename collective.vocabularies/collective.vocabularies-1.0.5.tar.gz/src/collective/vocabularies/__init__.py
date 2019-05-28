# -*- coding: utf-8 -*-
"""Init and utils."""
import os
from zope.i18nmessageid import MessageFactory


try:
    from pkg_resources import resource_filename
except ImportError:
    def resource_filename(package_or_requirement, resource_name):
        return os.path.join(os.path.dirname(__file__), resource_name)
        

_ = MessageFactory('collective.vocabularies')
DATABASE_DIR = resource_filename('collective.vocabularies', 'databases')

