#!/bin/sh
# sh pre-set
relativeBinDir='../../bin/activate'
relativeSrcDir='./src/'
relativepostDataDir='./postData/'

# venv source activate
source $(dirname "$0")/$relativeBinDir

# rm files under dir ./postData/
cd $(dirname "$0")/../
rm -r $relativepostDataDir
mkdir $relativepostDataDir
echo "rm files under dir ./postData/"

# python assignment
cd $relativeSrcDir
python myAssignment.py

# venv source deactivate
deactivate

# All done
echo "Python assignment all done!"

