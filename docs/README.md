# TrueAlgebra Documentation
This is the TrueAlgebra documentation directory. The TrueAlgebra/docs/source directory is the source of the documentation.

## Overview on Building the Source
In the interest of simplicity there is no Makefile and the make command is not used to generate the documents. Instead sphinx-build which comes with the sphinx package is used to build the documents.

The ipython package must be installed in the environment in order to build the documents. The reason is the `conf.py` file (in the source directory) there are two ipython extensions specified. In the documentation source *.rst files, ipython cell inputs were manually entered. But the ipython cell outputs were automatically generated and formatted by the ipython extensions during the building of the documentation. 

Essentially, the documentation is written around an ipython session. A ipython session is executed as part of every build process.

## Create and Prepare Environment
The recent development work has been on a Debian 12 operating system with python 3.11.2.  First create and activate a new environment with the commands:

    python3 -m venv ~/env/TAenv
    source ~/env/TAenv/bin/activate

Next, cd into the truealgebra package. Enter commands:

    pip install -e .
    pip install ipython
    pip install -U sphinx
    pip install sphinx_rtd_theme
    pip install pickleshare

Please note that the ipython package is required for building the TrueAlgebra documentation, but is not needed for the using TrueAlgebra.

## Build the Documents
Change directory into truealgebra/docs. then to build the documentation with sphinx-build.

    sphinx-build source <path-to-html-dir> 

If the html target directory does not exist, sphinx-build will create it. By default, sphinx-build will build html files.

To build other types of files such as pdf see the sphinx-build help:

    sphinx-build --help

## Step 4, Display the Documents
open browser to `<path-to-html-dir>/index.html`.

## Editing the Documents
When a user edits any of the files in the source source directory or the TrueAlgebra/truealgebra directory, the environment truealgebra package automatically updates. But the user must manually rebuild the documentation by reentering the command `sphinx-build source <path-to-html-dir>` and refreshing the browser tab.
