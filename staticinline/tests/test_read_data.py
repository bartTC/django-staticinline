import shutil
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management import call_command
from django.test import override_settings
from django.test.testcases import TestCase

from staticinline.main import FileDoesNotExistError, read_static_file


class ReadDataTests(TestCase):
    def setUp(self) -> None:
        # Django 1.8 won't create the STATIC_ROOT directory itself
        Path(settings.STATIC_ROOT).mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        # Manually delete the collectstatic directory after every test,
        # so we can be sure, all tests start from scratch.
        shutil.rmtree(settings.STATIC_ROOT)

    def test_read(self) -> None:
        """
        File is not read from the app's static dir when DEBUG is off.
        """
        pytest.raises(FileDoesNotExistError, read_static_file, "testapp/myfile.js")

    @override_settings(DEBUG=True)
    def test_missing_debug(self) -> None:
        """
        An exception is raised if the included file is not found in any
        static dirs.
        """
        pytest.raises(
            FileDoesNotExistError, read_static_file, "testapp/doesnotexist.js"
        )

    @override_settings(DEBUG=True)
    def test_read_debug(self) -> None:
        """
        File is read from the app's static dir when DEBUG is on.
        """
        data = read_static_file("testapp/myfile.js")
        assert data == "HelloWorld();\n"

    def test_collectstatic(self) -> None:
        """
        Files is read from STATIC_ROOT when DEBUG is off.
        """
        call_command("collectstatic", "-c", interactive=False)
        data = read_static_file("testapp/myfile.js")
        assert data == "HelloWorld();\n"

    @override_settings(DEBUG=True)
    def test_collectstatic_extraneous_debug(self) -> None:
        """
        Extraneous files in STATIC_ROOT are not read when DEBUG is on.
        """
        call_command("collectstatic", "-c", interactive=False)
        path = Path("testapp/unexpected.bat")
        with (settings.STATIC_ROOT / path).open("w") as f:
            f.write("@echo off")
        pytest.raises(FileDoesNotExistError, read_static_file, path)
