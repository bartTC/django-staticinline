.. _encoder:

====================================
Encoder: Transform files on the fly
====================================

You can automatically convert the file with the ``encode`` argument.
django-staticinline ships with a couple of encoders:

List of build-in encoders:
==========================

``base64``
----------

Transforms the file content to a base64 encoded string.

.. code:: django

    {% load staticinline %}
    {% staticinline "mykey.pem" encode="base64" %}'

Becomes:

.. code:: text

    LS0tIFN1cGVyIFByaXZhdGUgS2V5IC0tLQo=

-----

``data``
--------

Transforms the content into a data URI for use in
CSS ``url()`` and HTML ``src=""`` attributes.

.. code:: css+django

    {% load staticinline %}
    ul.checklist li.complete {
        background: url('{% staticinline "icons/check.png" encode="data" %}');
    }

Becomes:

.. code:: css

    ul.checklist li.complete {
        background: url('data:image/png;base64,iVBORw0KG\
    goAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD//\
    /+l2Z/dAAAAM0lEQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83ND\
    DeNGe4Ug9C9zwz3gVLMDA/A6P9/AFGGFyjOXZtQAAAAAElFTkSuQ\
    mCC');
    }

-----

``sri``
-------

Generates a sha256 hash of the file content, suitable for `Subresource Integrity`_
verifications.

.. _Subresource Integrity: https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity

.. code:: css+django

    {% load staticfiles %}
    {% load staticinline %}

    <link rel="stylesheet"
          href="{% static "base.css" %}"
          integrity="{% staticinline "base.css" encode="sri" %}"
          crossorigin="anonymous"/>

Becomes:

.. code:: css

    <link rel="stylesheet"
          href="/static/base.css"
          integrity="sha256-aeB9jNF0zyjK656631roQQOsKgRocLazJdr6fmleg4I"
          crossorigin="anonymous"/>


Add a custom Encoder
====================

You can add custom encoder by extending the AppConfig. See the `Django docs`_
for further information about AppConfig applications.

.. _Django docs: https://docs.djangoproject.com/el/2.1/ref/applications/

.. code:: python

    # myproject/apps.py
    from staticinline.apps import StaticInlineAppConfig

    # Add the custom 'upper' encoder to the list of build-in encoders.
    class CustomStaticInlineAppConfig(StaticInlineAppConfig):
        def get_encoder(self):
            encoder = super().get_encoder()
            encoder.update({
                'upper': self.encode_upper,
            })
            return encoder

        # Define the encoder itself. `data` contains the file content
        # and we transform all characters to uppercase here.
        def encode_upper(self, data, path):
            return data.upper()


In your ``INSTALLED_APPS`` setting you now point to your custom AppConfig:

.. code:: python

    # settings.py
    INSTALLED_APPS = [
        # 'staticinline.apps.StaticInlineAppConfig',
        'myproject.apps.CustomStaticInlineAppConfig',
    ]

In a template you call it with the respective name:

.. code:: css+django

    {% load staticinline %}

    {% staticinline "my-poem.txt" encode="upper" %}