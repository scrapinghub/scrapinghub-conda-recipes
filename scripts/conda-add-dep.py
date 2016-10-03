#!/usr/bin/env python
"""Patch a conda package adding additional dependencies."""
from __future__ import print_function

import argparse
import contextlib
import json
import os
import tarfile
import tempfile


@contextlib.contextmanager
def change_workdir(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


@contextlib.contextmanager
def patch_json_data(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)

    yield data

    with open(filename, 'w') as fp:
        json.dump(data, fp)


def patch_index(package, filename='info/index.json'):
    with patch_json_data(filename) as data:
        if package not in data['depends']:
            data['depends'].append(package)


def patch_recipe(package, filename='info/index.json'):
    with patch_json_data(filename) as data:
        if package not in data['depends']:
            data['depends'].append(package)


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('package', metavar='package.tar.bz')
    parser.add_argument('deps', metavar='dep', default=[], nargs='+')
    parser.add_argument('--temp-dir', default=tempfile.mkdtemp())
    parser.add_argument('--output')

    args = parser.parse_args()

    print("Extracting %s contents" % args.package)
    with tarfile.TarFile.bz2open(args.package, mode='r') as tar:
        with change_workdir(args.temp_dir):
            tar.extractall()

    print("Patching index and recipe")
    with change_workdir(args.temp_dir):
        for name in args.deps:
            print("Adding %s as dependency" % name)
            try:
                patch_index(name)
            except Exception as e:
                print("Failed to patch index: %s" % str(e))

            try:
                patch_recipe(name)
            except Exception as e:
                print("Failed to patch recipe: %s" % str(e))

    if args.output:
        print("Writing to %s" % args.output)
        dest = args.output
    else:
        print("Overwriting %s contents" % args.package)
        dest = args.package

    with tarfile.TarFile.bz2open(dest, mode='w') as tar:
        tar.add(args.temp_dir, arcname='')


if __name__ == "__main__":
    main()
