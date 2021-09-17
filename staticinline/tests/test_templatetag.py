from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.template import Template
from django.template.context import Context
from django.test import override_settings
from django.test.testcases import TestCase

from staticinline.templatetags import staticinline

from unittest import mock


def render(source, **context):
    return Template(source).render(Context(context))


class StaticInlineTests(TestCase):
    template = (
        "{% load staticinline %}" '<script>{% staticinline "somefile" %}</script>'
    )

    def test_found(self):
        """
        Static file is are correctly included inline the template.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = 'alert("hi")'
            rendered = render(self.template)
            self.assertEqual(rendered, '<script>alert("hi")</script>')

    def test_file_missing(self):
        """
        An empty string is returned if the inlined file is missing and
        DEBUG is off.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.side_effect = ValueError("Not found")
            rendered = render(self.template)
            self.assertEqual(rendered, "<script></script>")

    @override_settings(DEBUG=True)
    def test_file_missing_debug(self):
        """
        An error raised from read_static_file if the inlined file is
        missing and DEBUG is on.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.side_effect = ValueError("Not found")
            self.assertRaises(ValueError, render, self.template)


class CachedStaticInlineTests(TestCase):
    template_cached = (
        "{% load staticinline %}"
        '<script>{% staticinline "somefile" cache=True cache_timeout=60 %}</script>'
    )
    template_cached_encoder = (
        "{% load staticinline %}"
        '{% staticinline "some-other-file" encode="base64" cache=True cache_timeout=60 %}'
    )

    def tearDown(self):
        cache.clear()

    def test_cache(self):
        """
        Static file is are correctly included inline the template.
        """
        # Call once to set in cache
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = 'alert("hi")'
            rendered = render(self.template_cached)
            self.assertEqual(rendered, '<script>alert("hi")</script>')

        # Call again to test cache retrieval
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = 'alert("hi")'
            rendered = render(self.template_cached)
            self.assertEqual(rendered, '<script>alert("hi")</script>')

    def test_cache_encoder(self):
        """
        Static file is are correctly included inline the template.
        """
        # Call once to set in cache
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b"it is bytestring data"
            rendered = render(self.template_cached_encoder)
            self.assertEqual(rendered, "aXQgaXMgYnl0ZXN0cmluZyBkYXRh")

        # Call again to test cache retrieval
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b"it is bytestring data"
            rendered = render(self.template_cached_encoder)
            self.assertEqual(rendered, "aXQgaXMgYnl0ZXN0cmluZyBkYXRh")


class EncoderTests(TestCase):
    def test_unregistered(self):
        """
        Using an unregistered encoder will raise ImproperlyConfigured.
        """
        template = (
            "{% load staticinline %}"
            '{% staticinline "somefile" encode="doesnotexist" %}'
        )
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = 'alert("hi")'
            self.assertRaises(ImproperlyConfigured, render, template)

    def test_error(self):
        """
        If the encoder raises any exception, return an empty string when
        DEBUG is off.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b"it is bytestring data"
            rendered = render(
                "{% load staticinline %}"
                'My Key: {% staticinline "somefile" encode="broken" %}'
            )
            self.assertEqual(rendered, "My Key: ")

    @override_settings(DEBUG=True)
    def test_error_debug(self):
        """
        If the encoder raises any exception, the exception is raised
        when DEBUG is on.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b"it is bytestring data"
            template = (
                "{% load staticinline %}"
                'My Key: {% staticinline "somefile" encode="broken" %}'
            )
            self.assertRaises(ZeroDivisionError, render, template)

    def test_custom(self):
        """
        Custom encoders can be used in a separate appconfig.
        In testapp/apps.py, the 'uppercase' encoder is added.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b"shouting"
            rendered = render(
                "{% load staticinline %}"
                '{% staticinline "somefile" encode="uppercase" %}'
            )
            self.assertEqual(rendered, "SHOUTING")

    def test_base64(self):
        """
        The 'base64' encoder is shipped with this application.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b"it is bytestring data"
            rendered = render(
                "{% load staticinline %}"
                'My Key: {% staticinline "somefile" encode="base64" %}'
            )
            self.assertEqual(rendered, "My Key: aXQgaXMgYnl0ZXN0cmluZyBkYXRh")

    @override_settings(DEBUG=True)
    def test_data(self):
        """
        The 'data' URI encoder is shipped with this application.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b"png content"
            rendered = render(
                "{% load staticinline %}"
                '<img src="{% staticinline "a.png" encode="data" %}">'
            )
            self.assertEqual(
                rendered, '<img src="data:image/png;base64,cG5nIGNvbnRlbnQ=">'
            )

    @override_settings(DEBUG=True)
    def test_data_unknown_mimetype(self):
        """
        The data URI still works if no mimetype can be guessed.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b"png content"
            rendered = render(
                "{% load staticinline %}"
                '<img src="{% staticinline "somefile" encode="data" %}">'
            )
            self.assertEqual(rendered, '<img src="data:;base64,cG5nIGNvbnRlbnQ=">')

    def test_sri(self):
        """
        The 'base64' encoder is shipped with this application.
        """
        with mock.patch.object(staticinline, "read_static_file") as reader:
            reader.return_value = b'alert("hi")'
            rendered = render(
                "{% load staticinline %}"
                'integrity="{% staticinline "somefile" encode="sri" %}"'
            )
            self.assertEqual(
                rendered,
                'integrity="sha256-fdu2bQSeIdU5fvNNkRCjiwUEOOb+NLZDyGNVShZ1vCM="',
            )
