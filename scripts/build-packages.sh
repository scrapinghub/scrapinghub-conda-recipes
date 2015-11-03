#!/bin/bash
OUTPUT_DIR=$1
shift
PACKAGES=$@

if [ -z "$OUTPUT_DIR" -o -z "$PACKAGES" ]; then
  echo "Usage: $0 <OUTPUT_DIR> <PACKAGE> ..."
  exit 1
fi

if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p $OUTPUT_DIR
fi

set -ex

conda -V

for NAME in $PACKAGES; do
  BUILD_OUTPUT=$(conda build --output $NAME)
  conda build $NAME
  conda convert -q -p all -o $OUTPUT_DIR $BUILD_OUTPUT
done
