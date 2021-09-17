import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.test import override_settings
from django.test.testcases import TestCase

from staticinline.main import read_static_file


class ReadDataTests(TestCase):
    def setUp(self):
        # Django 1.8 won't create the STATIC_ROOT directory itself
        if not os.path.exists(settings.STATIC_ROOT):
            os.makedirs(settings.STATIC_ROOT)

    def tearDown(self):
        # Manually delete the collectstatic directory after every test
        # so we can be sure, all tests start from scratch.
        shutil.rmtree(settings.STATIC_ROOT)

    def test_read(self):
        """
        File is not read from the app's static dir when DEBUG is off.
        """
        self.assertRaises(ValueError, read_static_file, "testapp/myfile.js")

    @override_settings(DEBUG=True)
    def test_missing_debug(self):
        """
        An exception is raised if the included file is not found in any
        static dirs.
        """
        self.assertRaises(ValueError, read_static_file, "testapp/doesnotexist.js")

    @override_settings(DEBUG=True)
    def test_read_debug(self):
        """
        File is read from the app's static dir when DEBUG is on.
        """
        data = read_static_file("testapp/myfile.js")
        self.assertEqual(data, "HelloWorld();\n")

    def test_collectstatic(self):
        """
        Files is read from STATIC_ROOT when DEBUG is off.
        """
        call_command("collectstatic", "-c", interactive=False)
        data = read_static_file("testapp/myfile.js")
        self.assertEqual(data, "HelloWorld();\n")

    @override_settings(DEBUG=True)
    def test_collectstatic_extraneous_debug(self):
        """
        Extraneous files in STATIC_ROOT are not read when DEBUG is on.
        """
        call_command("collectstatic", "-c", interactive=False)
        path = "testapp/unexpected.bat"
        with open(os.path.join(settings.STATIC_ROOT, path), "w") as f:
            f.write("@echo off")
        self.assertRaises(ValueError, read_static_file, path)
