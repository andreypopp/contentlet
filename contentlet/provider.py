""" Content provider infrastructure."""

from zope.interface import providedBy
from zope.component import getGlobalSiteManager

from contentlet.interfaces import IContentProvider

__all__ = ["query_provider",
           "get_provider"]


def query_provider(name, context=None, registry=None):
    """ Query content provider by `name` or by `name` and `context`.

    By default, for lookup global registry will be used, but you can
    provide your own registry you want to lookup from via `registry` keyword
    argument.
    """
    if registry is None:
        registry = getGlobalSiteManager()
    provider = registry.adapters.lookup(
         (providedBy(context),), IContentProvider, name=name, default=None)
    return provider


def get_provider(name, context=None, registry=None):
    """ Get content provider by `name` or by `name` and `context`.
    If no providers was registered -- it will raise LookupError.

    By default, for provider lookup global registry will be used, but you can
    provide your own registry you want to lookup from via `registry` keyword
    argument.
    """
    provider = query_provider(name, context=context, registry=registry)
    if provider is None:
        raise LookupError("No provider was found for name '%s'" % name)
    return provider
