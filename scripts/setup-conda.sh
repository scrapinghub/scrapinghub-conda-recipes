#!/bin/bash
CONDA_HOME=$1
if [ -z "$CONDA_HOME" ]; then
  echo "Usage: $0 <CONDA_HOME>"
  exit 1
fi

set -ex

OS_NAME=$(uname -s)
OS_ARCH=$(uname -m)
if [ $OS_NAME == "Linux" ]; then
  CONDA_OS=Linux
elif [ $OS_NAME == "Darwin" ]; then
  CONDA_OS=MacOSX
else
  echo "Unsupported system: $OS_NAME"
  exit 1
fi

CONDA_CMD=$CONDA_HOME/bin/conda
if [ ! -f "$CONDA_CMD" ]; then
  wget https://repo.continuum.io/miniconda/Miniconda-latest-${CONDA_OS}-${OS_ARCH}.sh -O ~/miniconda.sh
  bash ~/miniconda.sh -b -f -p $CONDA_HOME
  rm -f ~/miniconda.sh
fi

$CONDA_CMD update -qy conda
$CONDA_CMD install -qy conda-build anaconda-client
