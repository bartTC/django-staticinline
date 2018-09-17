import mimetypes
import base64
import hashlib

from django.apps import AppConfig
from django.utils.safestring import mark_safe


class StaticInlineAppConfig(AppConfig):
    name = 'staticinline'
    verbose_name = 'Static Inline Files'
    encoder_response_format = 'utf-8'

    # Default cache timeout if not specified individually in the template tag
    # with the ``cache_timeout`` argument.
    cache_timeout = 60 * 60

    def build_cache_key(self, path, encode=None):
        s = '{0}{1}'.format(path, encode or '')
        return 'staticinline-{0}'.format(hashlib.sha1(s.encode()).hexdigest())

    def data_response(self, data):
        """
        This method transforms the data right before its written in the
        template. This is applied to all files, while 'encoder' are set
        individually per file.

        :param str data: The [optionally encoded] file content.
        :return: The [optionally encoded] file content.
        :rtype: str:
        """
        return mark_safe(data)

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
        h = hashlib.sha256(data).digest()
        h_base64 = base64.b64encode(h).decode()
        return 'sha256-{}'.format(h_base64)
