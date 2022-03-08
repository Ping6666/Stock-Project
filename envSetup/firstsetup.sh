#!/bin/sh
# first you need to setup files under dir ./envSetup/
# 1. for uwsgi under file myuwsgi.ini: userhome, socket
# 2. for nginx under file default: ip addr, server unix dir
# 3. for supervisor under file mysite.conf: directory, command
# 4. if env is Raspberry_Pi deal all line with '# For Raspberry_Pi'

# second decide where to store the project
projectBaseDir='/home/ping' # plz give a(n) (absolute) path
projectDirName='stockproject'
pipArgv=' --no-cache-dir --extra-index-url https://www.piwheels.org/simple ' # For Raspberry_Pi

# sh pre-set
runningBaseDir=${PWD}
envSetupDir='envSetup'
rawDataDir='rawData'
postDataDir='postData'

# setup sys env
sudo apt-get -qq install python3-pip=20.0.2-5ubuntu1.6 -y

# setup uwsgi env
sudo apt-get -qq install build-essential=12.8ubuntu1.1 -y
sudo apt-get -qq install python3-dev=3.8.2-0ubuntu2 -y
pip install -q ${pipArgv} -v uwsgi==2.0.20
mkdir ${projectBaseDir}/www/
touch ${projectBaseDir}/www/my_stock_site.sock

# setup virtualenv
pip install -q ${pipArgv} -v virtualenv==20.13.0
cd $projectBaseDir
echo "current runing dir: ${PWD}"
${projectBaseDir}/.local/bin/virtualenv -q $projectDirName # For non-Raspberry_Pi
# virtualenv -q $projectDirName # For Raspberry_Pi
cd $runningBaseDir/$(dirname "$0")
echo "current runing dir: ${PWD}"
cp -r ${PWD}/../../Stock-Project-main/ $projectBaseDir/$projectDirName/
mv $projectBaseDir/$projectDirName/Stock-Project-main/ $projectBaseDir/$projectDirName/code/

# setup nginx env
sudo apt-get -qq install nginx=1.18.0-0ubuntu1.2 -y
sudo cp ./default /etc/nginx/sites-enabled/

# setup supervisor env
sudo apt-get -qq install supervisor=4.1.0-1ubuntu1 -y
sudo cp ./mysite.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update

# setup python main env
# sudo apt-get -qq install libxml2-dev libxslt-dev python-dev -y # For Raspberry_Pi
cd $projectBaseDir/$projectDirName/code/
mkdir $rawDataDir
mkdir $postDataDir
source ../bin/activate
pip install ${pipArgv} -r ./$envSetupDir/required.txt

# All done
echo "If no warning, then congrats all done!"
