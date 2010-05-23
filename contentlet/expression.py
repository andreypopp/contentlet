""" TALES expression."""

from zope.interface import providedBy

from chameleon.core import types
from chameleon.zpt import expressions

from repoze.bfg.threadlocal import get_current_request

from contentlet.provider import query_provider

__all__ = ["ProviderExpression"]


def render_contentprovider(name):
    request = get_current_request()
    attrs = request.__dict__
    context = attrs.get("context")
    registry = attrs.get("registry")
    provider = query_provider(name, context=context, registry=registry)
    if provider is None:
        return ""
    return provider(context, request)


class ProviderExpression(expressions.ExpressionTranslator):
    """ TALES translator for executing content providers."""

    symbol = "_render_contentprovider"

    def translate(self, string, escape=None):
        value = types.value("%s('%s')" % (self.symbol, string))
        value.symbol_mapping[self.symbol] = render_contentprovider
        return value
