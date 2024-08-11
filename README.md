[![](https://badge.fury.io/py/django-staticinline.svg)](https://badge.fury.io/py/django-staticinline)
[![](https://github.com/bartTC/django-staticinline/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/bartTC/django-staticinline/actions)

-----

📖 Full documentation: https://django-staticinline.readthedocs.io<br/>
🐱 GitHub Repository: https://github.com/bartTC/django-staticinline


# django-staticinline

Works similar to Django's ``static`` templatetag, but this one includes
the file directly in the template, rather than a link to it.

You can additionally post-process the file content using custom 'encoder'.

## Compatibility Matrix:

| Py/Dj     | 3.9 | 3.10 | 3.11 | 3.12 |
|-----------|-----|------|------|------|
| 3.2 (LTS) | ✓   | ✓    | ✓    | ✓    |
| 4.0       | ✓   | ✓    | ✓    | ✓    |
| 4.1       | ✓   | ✓    | ✓    | ✓    |
| 4.2 (LTS) | —   | ✓    | ✓    | ✓    |
| 5.0       | —   | ✓    | ✓    | ✓    |
| 5.1       | —   | ✓    | ✓    | ✓    |

## Quickstart


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
