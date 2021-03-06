#!/bin/bash
set -euv

if [ -z "${ANACONDA_TOKEN:-}" ]; then
  echo "Missing ANACONDA_TOKEN environment variable"
  exit 1
fi

if [ -z "${ANACONDA_USER:-}" ]; then
  echo "Missing ANACONDA_USER environment variable"
  exit 1
fi

if [ -z "${ANACONDA_LABEL:-}" ]; then
  echo "Missing ANACONDA_LABEL environment variable"
  exit 1
fi

if [ -z "${BUILD_OUTPUT:-}" ]; then
  echo "Missing BUILD_OUTPUT environment variable"
  exit 1
fi

# TODO: Only upload packages that need to be uploaded. We could use the
# --interactive flag but it may ask to register a package or to replace it, so
# no single question.
# The --force flag causes to overwrite files (removing them) and losing the
# applied labels.
# The --interactive (defaulting to No) causes to not creating a new version
# package if it doesn't exist.
echo "Uploading packages to $ANACONDA_USER/$ANACONDA_LABEL"
for TARBALL in $BUILD_OUTPUT/{linux,win,osx}-*/*.tar.bz2; do
  # We use a custom anaconda wrapper to force the upload of new releases while
  # not overwriting existing releases.
  scripts/anaconda-wrapper.py -t $ANACONDA_TOKEN upload \
    --register --interactive -u $ANACONDA_USER -c $ANACONDA_LABEL $TARBALL
done
