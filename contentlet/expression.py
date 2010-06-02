""" TALES expression."""

from chameleon.core import types
from chameleon.zpt import expressions

from contentlet.provider import query_provider

__all__ = ["ProviderExpression"]


def render_contentprovider(request, name):
    """ Helper for rendering content provider by its name."""
    attrs = request.__dict__
    context = attrs.get("context")
    registry = attrs.get("registry")
    provider = query_provider(name, context=context, registry=registry)
    if provider is None:
        return ""
    return provider(context, request)


class ProviderExpression(expressions.ExpressionTranslator):
    """ TALES translator for rendering content providers.

    This TALES translator requires availabiity of current request `request` in
    template scope. Request should provide ZCA registry via attribute
    `registry` and optionally current context via attribute `context` for
    lookup content provider.
    """

    symbol = "_render_contentprovider"

    def translate(self, string, escape=None):
        value = types.value("%s(request, '%s')" % (self.symbol, string))
        value.symbol_mapping[self.symbol] = render_contentprovider
        return value
