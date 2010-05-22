""" Configuration for content providers."""

from zope.interface import Interface
from zope.interface import implementedBy
from zope.interface.interfaces import IInterface

from repoze.bfg.registry import Registry

from contentlet.interfaces import IContentProvider

__all__ = ["Configuration"]


class Configuration(object):

    def __init__(self, registry=None):
        if registry is None:
            registry = Registry()
        self.registry = registry

    def add_content_provider(self, provider, name, context=None):
        """ Add content provider."""
        if context is None:
            context = Interface
        if not IInterface.providedBy(context):
            context = implementedBy(context)
        self.registry.registerAdapter(
            provider, (context,), IContentProvider, name=name)