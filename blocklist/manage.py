#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
from django.core.management.commands.runserver import Command as runserver
from django.core.management import execute_from_command_line


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blocklist.settings")
    django.setup()
    runserver.default_addr = "192.168.178.6"
    runserver.default_port = "8080"
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
