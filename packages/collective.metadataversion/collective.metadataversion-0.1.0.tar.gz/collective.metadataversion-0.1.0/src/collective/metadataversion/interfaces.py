# -*- coding: utf-8 -*- vim: sw=4 sts=4 si et ts=8 tw=79 cc=+1
"""
collective.metadataversion: interfaces
"""

# Python compatibility:
from __future__ import absolute_import

# Zope:
from zope import schema

# Plone:
from plone.supermodel import model

# Local imports:
from ._i18n import _


class IMetadataSettings(model.Schema):
    metadata_version = schema.Int(
        title=_(u'Metadata version'),
        default=0,
        description=_(
            u'help_metadata_version',
            default=u'This value is set to the metadata_version attribute '
            u'of every brain whenever an object is reindexed with '
            u'update_metadata=True; this helps you to reindex objects only '
            u'when needed, and reindex more later, skipping the already '
            u'reindexed objects.'))
