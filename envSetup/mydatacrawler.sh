#!/bin/sh
# sh pre-set
relativeBinDir='../../bin/activate'
relativeSrcDir='../src/'

# venv source activate
source $(dirname "$0")/$relativeBinDir

# python assignment
cd $(dirname "$0")/$relativeSrcDir
python myAssignment.py

# venv source deactivate
deactivate

# All done
echo "Python assignment all done!"
