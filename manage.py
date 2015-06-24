#!/usr/bin/env python
import os
import sys

from django.conf import settings as django_settings
from test import settings as test_settings

if __name__ == "__main__":
    if not django_settings.configured:
        django_settings.configure(test_settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
