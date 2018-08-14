import mimetypes
import base64
import hashlib

from django.apps import AppConfig


class StaticInlineAppConfig(AppConfig):
    name = 'staticinline'
    verbose_name = 'Static Inline Files'
    encoder_response_format = 'utf-8'

    def get_encoder(self):
        """
        List of all registered encoders which can be used in the staticinline
        template tag. Example::

            {% staticinline "myfile.gif" encode="base64" %}

        This can be manually extended by providing a custom AppConfig.
        """
        return {
            'base64': self.encode_base64,
            'data': self.encode_data_uri,
            'sri': self.encode_sri,
        }

    def encode_base64(self, data, path):
        """
        Encodes with standard Base64.

        :param bytes data: Input data to encode.
        :return: Base64 encoded input string.
        :rtype: str
        :raises Exception: if the file is not suitable to be Base64 encoded.
        """
        return base64.b64encode(data).decode(self.encoder_response_format)

    def encode_data_uri(self, data, path):
        """
        Convert to the data URI scheme.

        :param bytes data: Input data to encode.
        :return: data URI string.
        :rtype: str
        """
        mimetype = mimetypes.guess_type(path)[0]
        if mimetype is None:
            prefix = 'data:;base64,'
        else:
            prefix = 'data:{0};base64,'.format(mimetype)
        return prefix + self.encode_base64(data, data)

    def encode_sri(self, data, path):
        """
        Adds Subresource Integrity encoder to staticinline. Read more:

        https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity

        Example Usage::

          {% load staticfiles %}
          {% load staticinline %}

          <link
            rel="stylesheet"
            href="{% static "base.css" %}"
            integrity="{% staticinline "base.css" encode="sri" %}"
            crossorigin="anonymous"/>

        :param bytes data: File content to build the SRI hash of.
        :return: sha256 hash
        :rtype: str
        """
        hash = hashlib.sha256(data).digest()
        hash_base64 = base64.b64encode(hash).decode()
        return 'sha256-{}'.format(hash_base64)
