#!/bin/sh
# first you need to setup files under dir ./envSetup/
# 1. for uwsgi under file myuwsgi.ini: userhome, socket
# 2. for nginx under file default: ip addr, server unix dir
# 3. for supervisor under file mysite.conf: directory, command

# second decide where to store the project
projectBaseDir='/home/ping' # plz give a(n) (absolute) path
projectDirName='stockproject'

# sh pre-set
runningBaseDir=${PWD}
envSetupDir='envSetup'
rawDataDir='rawData'
postDataDir='postData'

# setup sys env
sudo apt -qq install python3-pip=20.0.2-5ubuntu1.6 -y

# setup virtualenv
pip install -v -qq virtualenv==20.13.0
cd $projectBaseDir
echo "current runing dir: ${PWD}"
~/.local/bin/virtualenv -q $projectDirName
cd $runningBaseDir/$(dirname "$0")
echo "current runing dir: ${PWD}"
cp -r ${PWD}/../../Stock-Project-main/ $projectBaseDir/$projectDirName/
mv $projectBaseDir/$projectDirName/Stock-Project-main/ $projectBaseDir/$projectDirName/code/

# setup uwsgi env
pip install -v -qq uwsgi==2.0.20
mkdir ~/www/
touch ~/www/my_stock_site.sock

# setup nginx env
sudo apt -qq install nginx=1.18.0-0ubuntu1.2 -y
sudo cp ./default /etc/nginx/sites-enabled/

# setup supervisor env
sudo apt -qq install supervisor=4.1.0-1ubuntu1 -y
sudo cp ./mysite.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update

# setup python main env
cd $projectBaseDir/$projectDirName/code/
mkdir $rawDataDir
mkdir $postDataDir
source ../bin/activate
pip install -r ./$envSetupDir/required.txt

# All done
echo "If no warning, then congrats all done!"
