"""
Custom app config for staticinline to demonstrate and test
the 'custom encoder' functionality.
"""

from staticinline.apps import StaticInlineAppConfig


class CustomizedStaticInlineAppConfig(StaticInlineAppConfig):
    """
    Add a custom encoder to the list to test that behavior
    """

    def get_encoder(self):
        encoder = super().get_encoder()
        encoder.update({"uppercase": self.uppercase, "broken": self.broken})
        return encoder

    def uppercase(self, data, path):
        """
        Sample encoder that turns the incoming text data uppercase.
        """
        return data.decode(self.encoder_response_format).upper()

    def broken(self, data, path):
        """
        This intentionally raises an Exception to test error reporting.
        """
        return 1 / 0
