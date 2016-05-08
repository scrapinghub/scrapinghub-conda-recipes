#!/usr/bin/env python
"""Anaconda command wrapper to run interactive upload with custom answers."""
import re
import sys

import binstar_client.commands.upload
import binstar_client.scripts.cli as anaconda_cli
import binstar_client.utils


INTERATIVE_PATTERNS = {
    '^Would you like to create it now': 'y',  # new release
    'Enter a short description': '',  # new release
    'Would you like to make an announcement': 'n',  # new release
    'Distribution .+ already exists. Would you like to replace it': 'n',  # release exists
}


def patch_binstar_upload():
    patterns = {}
    for pat, out in INTERATIVE_PATTERNS.items():
        patterns[re.compile(pat)] = out

    def auto_input(prompt):
        sys.stdout.write(prompt)
        for regex, ans in patterns.items():
            if regex.search(prompt):
                sys.stdout.write(ans + '\n')
                return ans

    binstar_client.commands.upload.input = auto_input
    binstar_client.utils.input = auto_input


if __name__ == "__main__":
    patch_binstar_upload()
    sys.exit(anaconda_cli.main())
