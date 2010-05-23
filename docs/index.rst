.. Contentlet documentation master file, created by
   sphinx-quickstart on Sun May 23 13:14:37 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Contentlet — UI framework for web
=================================

Contentlet is a framework for creating composable and reusable UI for web. It
is designed by looking at `zope.contentprovider
<http://pypi.python.org/pypi/zope.contentprovider>`_ and `zope.viewlet
<http://pypi.python.org/pypi/zope.viewlet>`_ and for using with `repoze.bfg
<http://bfg.repoze.org>`_ web framework.

Introduction
============

Contentlet operates with content providers. Content provider is a piece of code
that provides some logically complete part of UI, for example twitter stream or
toolbar.

So, the template writer provides template with point, where content providers
will be invoked. This looks like a macros system, but it isn't.  Content
provider invokation and configuration are decoupled, so one can write where he
want to see any specific content provider and other — what content provider
will be seen there.

Content providers
=================

So, what is the content provider? It is function of two arguments::

    def my_contentprovider(context, request):
        return "A piece of UI."

or any callable object, for example::

    class MyContentProvider(object):

        def __call__(self, context, request):
            return "A piece of UI."

Content providers look like a simple views (in MTV frameworks, like repoze.bfg)
and they are even can be registered as views and vice-versa. So content
provider can be rendered as separate page and can be embedded in another page.

Configuring content providers
=============================

Content providers can be registered by name and for specific request's context. There are two ways for registering content providers for application:

* Imperative, via ``contentlet.Configurator``.

* Declarative, with ZCML directive ``contentprovider``.

Imperative configuration
------------------------

For configuring you application imperatively, you should use ``contentlet.Configurator`` object::

    ...
    import contentlet

    config = contentlet.Configurator(registry=you_application_registry)
    config.add_content_provider(my_contentprovider, "name")
    ...

or if you want to register content provider for specific context::

    ...
    import contentlet

    config = contentlet.Configurator(registry=you_application_registry)
    config.add_content_provider(my_contentprovider, "name", context=MyContext)
    ...

But where ``you_application_registry`` comes from? Often it is registry, that
was created by ``repoze.bfg.configuration.Configurator`` object, so the more
full piece of configuration code looks like this::


    ...
    import repoze.bfg
    import contentlet

    bfg_config = repoze.bfg.configuration.Configurator()
    bfg_config.add_view(my_view)
    config = contentlet.Configurator(registry=bfg_config.registry)
    config.add_content_provider(my_contentprovider, "name", context=MyContext)
    ...

We need to create to objects for configuring our application, sometimes it is
better to cook own configurator. There is ``ContentletConfiguratorMixin`` comes
to mind::

    ...
    from repoze.bfg.configuration import Configurator as BFGConfigurator
    from contentlet import Configurator as ContentletConfigurator

    class Configurator(BFGConfigurator, ContentletConfigurator):
        pass

    config = Configurator()
    config.add_view(my_view)
    config.add_content_provider(my_contentprovider, "name", context=MyContext)
    ...

So our custom ``Configurator`` object now suitable to configure both BFG and
contentlet aspects of application configuration.

Declarative configuration
-------------------------

Declarative configuration can be made with ``contentprovider`` ZCML directive::

    <configure>
        <include package="contentlet" />

        <contentprovider
            provider="mypackage.myprovider"
            name="name"
            />
    </configure>

or for registering content provider for specific context::

    <configure>
        <include package="contentlet" />

        <contentprovider
            provider="mypackage.myprovider"
            name="name"
            context="mypackage.models.MyContext"
            />
    </configure>

Note, that you should include ZCML configuration from ``contentlet`` package in
order to use ``contentprovider`` ZCML directive.

Using content providers
=======================

After registering some content providers, it is always good to query and use
them later in view or template code.

Using content providers inside views
------------------------------------

For using content providers inside views, you should use
``contentlet.get_provider`` or ``contentlet.query_provider`` function. The
difference between them is the only handling of failure of content provider
lookup. The ``contentlet.get_provider`` will raise ``LookupError`` while
``contentlet.query_provider`` will just return ``None`` value.

For query content provider by name and then render it in variable::

    ...
    from contentlet import query_provider
    provider = query_provider("provider_name")
    rendered = provider(request, context)
    ...

You can also query provider that is specific to context::

    ...
    from contentlet import query_provider
    provider = query_provider("provider_name", context=context)
    rendered = provider(request, context)
    ...

By default, ``contentlet.query_provider`` and ``contentlet.get_provider`` will
use global ZCA registry for lookups. This is not desired behaviour while using
repoze.bfg web-framework, cause it uses per-application registry. View code can
get it via request's ``registry`` attribiute, so querying content providers in
repoze.bfg's view usually done in following way::

    ...
    from contentlet import query_provider
    provider = query_provider("provider_name", registry=request.registry)
    rendered = provider(request, context)
    ...

So, ``registry`` keyword argument specify what component registry to use for
content provider lookup.

Using content providers inside Chameleon templates
--------------------------------------------------

Usually it is better to use content providers from inside templates than from
views. Repoze.bfg comes with `Chameleon <http://chameleon.repoze.org/>`_
templating engine and Contentlet provides custom TALES expression translator
for rendering content providers::

    <div tal:replace="contentprovider:name"></div>

This ``div`` element will be replace with piece of markup, returned by content
provider with name ``name``.
