""" ZCML directives."""

from zope.component import getSiteManager
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.schema import TextLine

from contentlet.configuration import Configurator

__all__ = ["IContentProviderDirective",
           "contentprovider"]


class IContentProviderDirective(Interface):

    provider = GlobalObject(
        title=u"Content provider to be registered.",
        required=True)

    name = TextLine(
        title=u"The name of the content provider.",
        required=True)

    context = GlobalObject(
        title=u"Context type or interface for which content provider register.",
        required=False)


def contentprovider(_context, provider=None, name=None, context=None):
    registry = getSiteManager()

    def register():
        config = Configurator(registry)
        config.add_content_provider(provider, name, context=context)

    _context.action(
        discriminator=(name,),
        callable=register
    )
