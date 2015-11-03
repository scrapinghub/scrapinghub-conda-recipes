#!/bin/bash
set -e

COMMIT_RANGE=$1
CHANGED_FILES=$(git diff --name-only $COMMIT_RANGE)

for FILE in $CHANGED_FILES; do
  PACKAGE=$(dirname $FILE)
  if [ -f "$PACKAGE/meta.yaml" ]; then
    echo $PACKAGE
  fi
done | sort | uniq
