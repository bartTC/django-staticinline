#!/usr/bin/env python

import sys

from django import setup
from django.conf import settings
from django.test.runner import DiscoverRunner

def runtests():
    if not settings.configured:
        from staticinline.tests.testapp import settings as TEST_SETTINGS
        settings.configure(**TEST_SETTINGS.__dict__)
    setup()
    test_runner = DiscoverRunner(verbosity=1)
    failures = test_runner.run_tests(['staticinline'])
    if failures:
        sys.exit(failures)

if __name__ == '__main__':
    runtests()
