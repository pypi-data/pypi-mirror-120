# -*- coding: utf-8 -*- vim: sw=4 sts=4 si et ts=8 tw=79 cc=+1
"""
collective.metadataversion: utilities

We don't provide browser views to get and set our metadata_version;
we don't need to, since we use the standard Plone registry.

However, we like some comfort using our unintrusive little metadata column,
and for this reason we provide a little utility here;
see the ../../../README.rst file for a short usage description.
"""

# Python compatibility:
from __future__ import absolute_import

__all__ = [
    'make_metadata_updater',
    ]

try:
    # Zope:
    from Products.CMFCore.utils import getToolByName
    from ZODB.POSException import ConflictError
    from zope.component import getUtility

    # Plone:
    from plone.registry.interfaces import IRegistry

    # 3rd party:
    from Missing import Value as Missing_Value

    # Local imports:
    from .config import FULL_VERSION_KEY, VERSION_KEY
    from .exceptions import (
        ObjectNotFound,
        ReindexingError,
        UsageTypeError,
        UsageValueError,
        )
except ImportError as e:
    if __name__ == '__main__':  # doctest
        VERSION_KEY = 'metadata_version'
        FULL_VERSION_KEY = ('collective.metadataversion.interfaces'
                            '.IMetadataSettings.metadata_version')
        IRegistry = None  # good enough for our doctest
        fake_registry = {FULL_VERSION_KEY: 42}
        def getUtility(*args, **kw):
            return fake_registry
        HAVE_MISSING = 0
        Missing_Value = ''
        class ReindexingError(Exception):
            def __init__(self, message, cause=None):
                self.message = message
                self.cause = cause
            def __str__(self):
                return self.message
        class ObjectNotFound(ReindexingError): pass
        UsageTypeError = TypeError
        UsageValueError = ValueError
        ConflictError = Exception
    else:
        raise
else:
    HAVE_MISSING = 1


def _update_mmu_kwargs(context, logger, metadata_version, kwargs):
    """
    Update a kwargs dict, injecting 'new_version' and 'minimum_version' keys.

    NOTE: This function is for internal use, and both the signature and
          the functionality may change without notice!

    For our test, the registry will be a simple dict object containing our key:

    >>> FULL_VERSION_KEY = 'metadata_version'
    >>> def getUtility(*args, **kw):
    ...     return {FULL_VERSION_KEY: 42}

    The context argument is needed only to get the portal_catalog,
    so None is sufficient for this function:

    >>> def ummu(metadata_version, kwargs):
    ...     _update_mmu_kwargs(None, None, metadata_version, kwargs)
    ...     return sorted(kwargs.items())

    We can specify a smaller than the recorded version, which will be used for
    comparisons as intended; but it won't be stored by default:
    >>> kw = {}
    >>> ummu(41, kw)                          # doctest: +NORMALIZE_WHITESPACE
    [('idxs', ['getId']),
     ('minimum_version', 41),
     ('new_version',   None),
     ('old_version',     42)]

    ... unless we force it to be accepted:
    >>> kw = dict(force_version=1)
    >>> ummu(41, kw)                          # doctest: +NORMALIZE_WHITESPACE
    [('idxs', ['getId']),
     ('minimum_version', 41),
     ('new_version',     41),
     ('old_version',     42)]

    This has updated our registry value; thus, a call without a new version
    will result in:
    >>> kw = {}
    >>> ummu(None, kw)                        # doctest: +NORMALIZE_WHITESPACE
    [('idxs', ['getId']),
     ('minimum_version', 41),
     ('new_version',   None),
     ('old_version',     41)]

    While we don't necessarily handle *all* legal options here,
    we still reject unknown options, raising the usual TypeError:

    >>> ummu(None, dict(minimum_version=40))
    Traceback (most recent call last):
      ...
    TypeError: Illegal argument(s): minimum_version

    """
    force_version = kwargs.pop('force_version', False)
    strict = kwargs.pop('strict', True)
    if metadata_version is not None:
        if not isinstance(metadata_version, int):
            raise UsageValueError('integer number expected;'
                                  ' found %(metadata_version)r'
                                  % locals())
        if metadata_version < 0:
            raise UsageValueError('integer number >=0 expected;'
                                  ' found %(metadata_version)r'
                                  % locals())
    elif force_version:
        raise UsageValueError('With force_version given, '
                              'we expect a non-None metadata_version!')
    unused = set(kwargs) - set(['idxs', 'force_indexes',
                                'update_metadata',
                                'debug',
                                ])
    if unused:
        unused = sorted(unused)
        if strict:
            raise UsageTypeError('Illegal argument(s): %s'
                                 % ', '.join(unused))
        else:
            for key in unused:
                val = kwargs.pop(key)
                logger.warn('IGNORING unknown option %(key)s=%(val)r', locals())

    registry = getUtility(IRegistry)
    old_version = registry.get(FULL_VERSION_KEY)
    new_version = None
    if metadata_version > old_version:
        registry[FULL_VERSION_KEY] = minimum_version = new_version = metadata_version
    elif force_version:
        assert isinstance(metadata_version, int)  # see above: not None
        registry[FULL_VERSION_KEY] = minimum_version = new_version = metadata_version
    elif metadata_version is None:
        minimum_version = old_version or 0
    else:
        assert metadata_version <= old_version
        assert isinstance(metadata_version, int)
        minimum_version = metadata_version

    if 'idxs' not in kwargs:
        if kwargs.get('force_indexes'):
            idxs = None  # refresh all indexes
        else:
            idxs = ['getId']  # default: a cheap subset
        kwargs['idxs'] = idxs

    kwargs.update({
        # metadata_version value, stored in the registry:
        'new_version':     new_version,  # if not None, written to registry
        'old_version':     old_version,  # ... from registry
        # the metadata_version (always a number >= 0)
        # the brain objects are compared to:
        'minimum_version': minimum_version,
        })


def make_metadata_updater(context, logger=None, metadata_version=None,
                          **kwargs):
    """
    Create an updater to conditionally update the metadata of an object.

    Arguments:

    context -- the context (usually the portal)
    logger -- a logger, used to tell e.g. about the set and/or active
              metadata_version; if not given, we'll create one.
    metadata_version -- an integer number, or None.
                   If a number, it should be greater than the previously active
                   version.

    The remaining arguments are "keyword-only":
    force_version -- change the target metadata_version even if smaller than
                   the previously active version. We expect this to be used
                   for development only.

    idxs -- (forwarded to catalog.reindexObject)
            The indexes to be updated in case an object's metadata is to be
            updated.  The default value depends on the value of the
            force_indexes option:

            - If falsy (default), we use a "cheap selection" (['getId']),
              simply to make the metadata refresh happen;
            - otherwise, the default is `None`, causing all indexes to be
              updated (but -- with update_metadata=None (the default) -- not
              necessarily the metadata as well).

            Note that we *do* care if idxs=None is explicitly specified --
            this will be honoured, and no "cheap subset" is used! --
            or not.
    force_indexes -- Refresh the indexes (according to the idxs option above)
            even if the metadata is already up-to-date.

    ... and finally:

    update_metadata -- Refresh the metadata columns?

        We are not sure yet whether the non-default values make any sense.
        However, the possible values are:

            None (the default) -- refresh brains without a current
                                  metadata_version
            True -- refresh even up-to-date brains
            False -- suppress metadata updates.  *Note* that this will cause
                     the metadata_version column not to be updated either!
    """
    if logger is None:
        logger = logging.getLogger('reindex')
    _update_mmu_kwargs(context, logger, metadata_version, kwargs)
    assert 'new_version' in kwargs
    catalog = getToolByName(context, 'portal_catalog')
    catalog_reindex = catalog.reindexObject

    idxs = kwargs['idxs']
    new_version = kwargs['new_version']
    old_version = kwargs['old_version']
    minimum_version = kwargs['minimum_version']
    was = (new_version > old_version) and 'was' or 'is'
    logger.info('metadata_version %(was)s %(old_version)r', locals())
    if new_version is None:
        if metadata_version is not None and minimum_version < old_version:
            logger.warn('metadata_version NOT changed to %(minimum_version)d'
                        ' because smaller than %(old_version)d'
                        ' (perhaps try force_version=True?)', locals())
    else:
        logger.info('metadata_version changed to %(new_version)d', locals())
    logger.info('metadata_version will be set to %d'
                ' for all reindexed objects',
                old_version if new_version is None
                else new_version)
    logger.info('metadata_version will be compared to %(minimum_version)d',
                locals())

    force_indexes = kwargs.get('force_indexes', False)
    update_metadata = kwargs.get('update_metadata', None)
    _info = ['comparing metadata_version to %(minimum_version)d' % locals(),
             idxs and 'indexes: ' + ', '.join(idxs) or 'all indexes',
             ]
    debug = kwargs.pop('debug', False)
    if debug:
        _info.append('DEBUG')

    logger.info('make_metadata_updater: ' + '; '.join(_info))

    def reindex(brain):
        """
        Reindex the object given as brain.
        """
        # if this fails, there is a general problem;
        # e.g., you need to run catalog.xml first
        current_version = brain.metadata_version
        REINDEXED, ERROR = False, None

        # '' > 0 > None; we distinguish between 0 and None
        if HAVE_MISSING:
            if current_version is Missing_Value:
                current_version = None
        else:
            if current_version == Missing_Value:
                current_version = None

        if update_metadata is None:  # the default
            refresh_metadata = current_version < minimum_version
        elif update_metadata:
            refresh_metadata = 1
        else:
            refresh_metadata = 0

        if not refresh_metadata and not force_indexes:
            return False

        try:
            o = brain.getObject()
        except Exception as e:
            logger.exception(e)
            txt = '%(brain)r.getObject() FAILED!' % locals()
            logger.error(txt)
            raise ObjectNotFound(txt, e)
        else:
            if o is None:
                txt = '%(brain)r.getObject() returned None!' % locals()
                logger.error(txt)
                raise ObjectNotFound(txt, e)

        try:
            catalog_reindex(o, idxs=idxs, update_metadata=refresh_metadata)
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception as e:
            logger.error('error reindexing %(o)r: %(e)r', locals())
            raise ReindexingError('Error reindexing %(o)r' % locals(),
                                  e)
        else:
            return True

    return reindex


if __name__ == '__main__':
    # Standard library:
    import doctest
    doctest.testmod()
