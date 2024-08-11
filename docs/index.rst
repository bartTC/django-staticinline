.. _index:

================================================
Welcome to the django-staticinline Documentation
================================================

===================
django-staticinline
===================

Works similar to Django's ``static`` templatetag, but this one includes
the file directly in the template, rather than a link to it.

You can additionally post-process the file content using custom 'encoder'.

Quickstart
==========

1. Put the StaticInlineAppConfig along your apps.

   .. code:: python

       INSTALLED_APPS = [
           # ...
           'staticinline.apps.StaticInlineAppConfig',
       ]

2. Load the template tag and pass a filename as you'd do with a ``static``
   template tag. You can also post-process the file content. In the example
   below we encode the content of the ``mykey.pem`` file with base64. Several
   encoders are already built-in, see the `Encoder docs`_.

   .. code:: django

       {% load staticinline %}

       <style type="text/css">{% staticinline "myfile.css" %}</style>
       My base64 encoded Key: {% staticinline "mykey.pem" encode="base64" cache=True %}


3. Enjoy the result:

   .. code:: html

       <style type="text/css">body{ color: red; }</style>
       My base64 encoded Key: LS0tIFN1cGVyIFByaXZhdGUgS2V5IC0tLQo=

.. _Encoder docs: https://docs.elephant.house/django-staticinline/encoder.html

Further reading:
================

.. toctree::
   :maxdepth: 3

   installation
   encoder
   development
