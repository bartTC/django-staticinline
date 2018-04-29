import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.template import Template
from django.template.context import Context
from django.test import override_settings
from django.test.testcases import TestCase


class StaticInlineTestCase(TestCase):

    def setUp(self):
        # Django 1.8 won't create the STATIC_ROOT directory itself
        if not os.path.exists(settings.STATIC_ROOT):
            os.makedirs(settings.STATIC_ROOT)

    def tearDown(self):
        # Manually delete the collectstatic directory after every test
        # so we can be sure, all tests start from scratch.
        shutil.rmtree(settings.STATIC_ROOT, ignore_errors=True)

    def render_template(self, template_string):
        return Template(template_string).render(Context())

    # --------------------------------------------------------------------------
    # Static files are in app directory (not collected)
    # --------------------------------------------------------------------------
    @override_settings(DEBUG=True)
    def test_debug_on(self):
        """
        Test static files are correctly included inline the template,
        when DEBUG mode is True.
        """
        template = '{% load staticinline %}<script>{% staticinline "testapp/myfile.js" %}</script>'
        expected = '<script>HelloWorld();\n</script>'
        rendered = self.render_template(template)
        self.assertEqual(expected, rendered)
        self.assertTrue(settings.DEBUG)

    @override_settings(DEBUG=False)
    def test_debug_off(self):
        """
        Test static files are correctly included inline the template,
        when DEBUG mode is False.
        """
        template = '{% load staticinline %}<script>{% staticinline "testapp/myfile.js" %}</script>'
        expected = '<script>HelloWorld();\n</script>'
        rendered = self.render_template(template)
        self.assertEqual(expected, rendered)
        self.assertFalse(settings.DEBUG)

    # --------------------------------------------------------------------------
    # Static files were collected using 'manage.py collectstatic'
    # --------------------------------------------------------------------------
    @override_settings(DEBUG=True)
    def test_debug_on_with_collectstatic(self):
        """
        Test static files are correctly included inline the template,
        when DEBUG mode is True, and files were collected
        """
        call_command('collectstatic', '-c', interactive=False)

        template = '{% load staticinline %}<script>{% staticinline "testapp/myfile.js" %}</script>'
        expected = '<script>HelloWorld();\n</script>'
        rendered = self.render_template(template)
        self.assertEqual(expected, rendered)
        self.assertTrue(settings.DEBUG)

    @override_settings(DEBUG=False)
    def test_debug_off_with_collectstatic(self):
        """
        Test static files are correctly included inline the template,
        when DEBUG mode is False, and files were collected
        """
        call_command('collectstatic', '-c', interactive=False)

        template = '{% load staticinline %}<script>{% staticinline "testapp/myfile.js" %}</script>'
        expected = '<script>HelloWorld();\n</script>'
        rendered = self.render_template(template)
        self.assertEqual(expected, rendered)
        self.assertFalse(settings.DEBUG)

    # --------------------------------------------------------------------------
    # File does not exist
    # --------------------------------------------------------------------------
    @override_settings(DEBUG=True)
    def test_debug_on_file_missing(self):
        """
        ValueError is raised if DEBUG mode is True
        and the included file is missing.
        """
        template = '{% load staticinline %}<script>{% staticinline "testapp/doesnotexist.js" %}</script>'
        self.assertRaises(ValueError, self.render_template, template)
        self.assertTrue(settings.DEBUG)

    @override_settings(DEBUG=False)
    def test_debug_off_file_missing(self):
        """
        Empty string is returned if DEBUG mode is False
        and the included file is missing.
        """
        template = '{% load staticinline %}<script>{% staticinline "testapp/doesnotexist.js" %}</script>'
        expected = '<script></script>'
        rendered = self.render_template(template)
        self.assertEqual(expected, rendered)
        self.assertFalse(settings.DEBUG)
