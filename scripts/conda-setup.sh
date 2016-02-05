#!/bin/bash
set -euv

if [ -z "${CONDA_HOME:-}" ]; then
  echo "Missing CONDA_HOME environment variable"
  exit 1
fi

if [ -z "${ANACONDA_USER:-}" ]; then
  echo "Missing ANACONDA_USER environment variable"
  exit 1
fi

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

if [ ! -d $CONDA_HOME ]; then
  wget -q https://repo.continuum.io/miniconda/Miniconda-latest-${CONDA_OS}-${OS_ARCH}.sh -O /tmp/miniconda.sh
  bash /tmp/miniconda.sh -b -f -p $CONDA_HOME
  rm -f /tmp/miniconda.sh
fi

PATH=$CONDA_HOME/bin:$PATH

conda config --set always_yes yes
conda config --set show_channel_urls yes
conda config --add channels scrapinghub
conda config --add channels $ANACONDA_USER

conda update -q conda
conda install -q conda-build anaconda-client
conda install -q conda-build-all -c conda-forge

conda info -a
