#!/bin/bash

# argv
backend_dir="backend"
frontend_dir="frontend"

# Backend Startup
cd $backend_dir
gnome-terminal -- /bin/bash -c "echo \"starting back-end\"; python3 ./src/main.py;"

cd ..

# Frontend Startup
cd $frontend_dir
gnome-terminal -- /bin/bash -c "echo \"starting front-end\"; npm install; npm run build; npm start;"

# env set
cd $home_dir/$base_dir

echo "Website front-end & back-end have been started!!!"
