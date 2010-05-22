""" Interfaces."""

from zope.interface import Interface

__all__ = ["IContentProvider"]


class IContentProvider(Interface):
    """ Content provider.

    Component of this type provides a piece of content or UI.
    """

    def __call__(context, request):
        """ Provide content."""
