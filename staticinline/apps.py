from base64 import b64encode

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
        }

    def encode_base64(self, data):
        """
        Encodes a given string with standard Base64.
        :param bytes data: Input file to encode.
        :return: Base64 encoded input string.
        :rtype: str
        :raises Exception: if the file is not suitable to be Base64 encoded.
        """
        return b64encode(data).decode(self.encoder_response_format)
