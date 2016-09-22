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

    upload_package_orig = binstar_client.commands.upload.upload_package

    def upload_package_fixed(*args, **kwargs):
        out = upload_package_orig(*args, **kwargs)
        if not out:
            # When not overriding, it returns [] while caller expects tuples.
            out = ['-unknown-', {}]
        return out

    binstar_client.commands.upload.input = auto_input
    binstar_client.commands.upload.upload_package = upload_package_fixed
    binstar_client.utils.input = auto_input


def process_args(args):
    while args:
        token = args.pop(0)
        # For labels, handle comma-separated list automatically. That is, repeat
        # the parameter for each value. This to ease overriding channels via
        # single argument.
        if token in ['-l', '-c']:
            labels = args.pop(0).split(',')
            for lab in labels:
                yield token
                yield lab
        else:
            yield token


def main():
    patch_binstar_upload()

    sys.argv = list(process_args(sys.argv))
    sys.exit(anaconda_cli.main())


if __name__ == "__main__":
    main()
