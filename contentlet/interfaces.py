""" Interfaces."""

from zope.interface import Interface
from zope.interface.common.mapping import IReadMapping

__all__ = ["IContentProvider",
           "IViewlet",
           "IViewletManager"]


class IContentProvider(Interface):
    """ Content provider.

    Component of this type provides a piece of content or UI.
    """

    def __call__(context, request):
        """ Provide content."""


class IViewlet(IContentProvider):
    """ Viewlet.

    Viewlet is a content provider that is managed by viewlet manager.
    """


class IViewletManager(IContentProvider, IReadMapping):
    """ Viewlet manager.

    Viewlet is a content provider that can manage other content providers that
    are called viewlets.
    """
