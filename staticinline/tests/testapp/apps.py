"""
Custom app config for staticinline to demonstrate and test
the 'custom encoder' functionality.
"""
from __future__ import annotations

from staticinline.apps import StaticInlineAppConfig


class CustomizedStaticInlineAppConfig(StaticInlineAppConfig):
    """
    Add a custom encoder to the list to test that behavior
    """

    def get_encoder(self) -> dict[str, any]:
        encoder = super().get_encoder()
        encoder.update({"uppercase": self.uppercase, "broken": self.broken})
        return encoder

    def uppercase(self, data: bytes, path: str) -> str:
        """
        Sample encoder that turns the incoming text data uppercase.
        """
        return data.decode(self.encoder_response_format).upper()

    def broken(self, data: bytes, path: str) -> float:
        """
        This intentionally raises an Exception to test error reporting.
        """
        return 1 / 0
