""" Implementations of IContentProvider."""

from zope.interface import providedBy

from contentlet.interfaces import IContentProvider

__all__ = ["get_provider"]


def get_provider(request, name):
    """ Return content provider by its name."""
    adapters = request.registry.adapters
    context = request.context
    provider = adapters.lookup(
         (providedBy(context),), IContentProvider, name=name, default=None)
    if provider is None:
        raise LookupError("No provider was found for name '%s'" % name)
    return provider
