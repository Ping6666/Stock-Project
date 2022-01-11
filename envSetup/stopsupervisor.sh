#!/bin/bash
sudo supervisorctl shutdown
sudo supervisord -c /etc/supervisor/supervisord.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl stop all
sudo systemctl stop nginx
