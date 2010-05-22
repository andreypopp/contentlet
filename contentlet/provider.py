""" Implementations of IContentProvider."""

from zope.interface import providedBy

from repoze.bfg.threadlocal import get_current_request

from contentlet.interfaces import IContentProvider

__all__ = ["get_provider"]


def get_provider(name, request=None):
    """ Return content provider by its name."""
    if request is None:
        request = get_current_request()
    adapters = request.registry.adapters
    context = request.context
    provider = adapters.lookup(
         (providedBy(context),), IContentProvider, name=name, default=None)
    if provider is None:
        raise LookupError("No provider was found for name '%s'" % name)
    return provider
