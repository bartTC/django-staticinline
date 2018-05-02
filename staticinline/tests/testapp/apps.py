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
        default_encoder = super(CustomizedStaticInlineAppConfig, self).get_encoder()

        return default_encoder.update({
            'uppercase': self.uppercase,
            'broken': self.broken,
        })

    def uppercase(self, data):
        """
        Sample enocder that turns the incoming text data uppercase.
        """
        return data.decode(self.encoder_response_format).upper()

    def broken(self, data):
        """
        This intentionally raises an Exception to test error reporting.
        """
        return 1/0
