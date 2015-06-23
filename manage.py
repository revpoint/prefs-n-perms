#!/usr/bin/env python
import os
import sys

from django.conf import settings
from tests import settings as test_settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    settings.configure(test_settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
