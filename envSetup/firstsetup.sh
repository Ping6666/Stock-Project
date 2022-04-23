#!/bin/sh
# first you need to setup files under dir ./envSetup/
# if env is Raspberry_Pi deal all line with '# For Raspberry_Pi'

# second decide where to store the project
projectBaseDir='/home/ping' # plz give a(n) (absolute) path (user home)
serverIp='192.168.0.1'

projectDirName='stockproject'
pipArgv=' --no-cache-dir --extra-index-url https://www.piwheels.org/simple ' # For Raspberry_Pi

# sh pre-set
runningBaseDir=${PWD}
projectDefualtName='Stock-Project' # use git clone to download this repository
envSetupDir='envSetup'
rawDataDir='rawData'
postDataDir='postData'

function replaceFileTextBysearch {
    # $1: search, $2: replace, $3: filename
    if [[ $1 != "" && $2 != "" ]]; then
        echo "target file: $3, with $1 change to $2."
        sed -i "s@$1@$2@g" $3
    fi
}

cd $projectBaseDir
echo "current runing dir: ${PWD}"

# replace for custom file text
replaceFileTextBysearch "PWD_DIR" "$projectBaseDir" "./$projectDefualtName/$envSetupDir/mysite.conf"
replaceFileTextBysearch "PWD_DIR" "$projectBaseDir" "./$projectDefualtName/$envSetupDir/myuwsgi.ini"
replaceFileTextBysearch "PWD_DIR" "$projectBaseDir" "./$projectDefualtName/$envSetupDir/default"
replaceFileTextBysearch "Server_IP" "$serverIp" "./$projectDefualtName/$envSetupDir/default"

sudo apt-get update
sudo apt-get -qq install python3-pip build-essential python3-dev nginx supervisor -y
sudo pip install -q -v uwsgi==2.0.20 virtualenv==20.13.0

# For Raspberry_Pi
# sudo pip install -q $pipArgv -v uwsgi==2.0.20 virtualenv==20.13.0

mkdir $projectBaseDir/www/
touch $projectBaseDir/www/my_stock_site.sock

virtualenv -q $projectDirName

cd $runningBaseDir/$(dirname "$0")
echo "current runing dir: ${PWD}"

cp -r ${PWD}/../../$projectDefualtName/ $projectBaseDir/$projectDirName/
mv $projectBaseDir/$projectDirName/$projectDefualtName/ $projectBaseDir/$projectDirName/code/

sudo cp ./default /etc/nginx/sites-enabled/
sudo cp ./mysite.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update

cd $projectBaseDir/$projectDirName/code/
echo "current runing dir: ${PWD}"
mkdir $rawDataDir
mkdir $postDataDir

source ../bin/activate
pip install -r ./$envSetupDir/required.txt

# For Raspberry_Pi
# sudo apt-get -qq install libxml2-dev libxslt-dev python-dev -y 
# pip install $pipArgv -r ./$envSetupDir/required.txt

sudo apt-get clean && apt-get autoremove

cd $projectBaseDir
echo "current runing dir: ${PWD}"

bash ./stockproject/code/envSetup/stopsupervisor.sh
bash ./stockproject/code/envSetup/stopsupervisor.sh
bash ./stockproject/code/envSetup/stopsupervisor.sh
bash ./stockproject/code/envSetup/stopsupervisor.sh
sudo supervisorctl start mysite:*

echo "If no warning, then congrats all done!"
