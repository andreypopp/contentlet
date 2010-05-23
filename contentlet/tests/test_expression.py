""" Tests for contentlet.expressions."""

import unittest

from repoze.bfg.registry import Registry
from repoze.bfg import testing

__all__ = ["TestProviderExpression"]


class DummyProvider(object):

    def __init__(self, content):
        self.content = content

    def __call__(self, context, request):
        return self.content


class TestProviderExpression(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        request = testing.DummyRequest()
        request.registry = self.registry
        request.context = None
        testing.setUp(registry=self.registry, request=request)

    def _registerTranslator(self, translator):
        from chameleon.zpt.interfaces import IExpressionTranslator
        self.registry.registerUtility(translator, IExpressionTranslator,
                                      name="contentprovider")

    def _registerProvider(self, provider, name, context_iface=None):
        from zope.interface import Interface
        from contentlet.interfaces import IContentProvider
        if context_iface is None:
            context_iface = Interface
        self.registry.registerAdapter(
            provider, (context_iface,), IContentProvider, name=name)

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        from contentlet.expression import ProviderExpression
        self._registerTranslator(ProviderExpression())
        self._registerProvider(DummyProvider("content"), "name")
        from chameleon.zpt.template import PageTemplate
        template = PageTemplate("""\
        <div tal:replace="contentprovider:name">
          Hello World!
        </div>""", None)
        rendered = template()
        self.assertEqual(rendered, "content")

    def test_no_provider(self):
        from contentlet.expression import ProviderExpression
        self._registerTranslator(ProviderExpression())
        from chameleon.zpt.template import PageTemplate
        template = PageTemplate("""\
        <div tal:replace="contentprovider:name">
          Hello World!
        </div>""", None)
        rendered = template()
        self.assertEqual(rendered, "")
