#!/usr/bin/env python
"""
The startup module for this application.
Supported command line arguments
a. python app web
b. python app tools
"""

import os
import sys



if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "smweb.settings"
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
