# stock project

## install docker and docker-compose

[Install Docker Engine on Ubuntu | Docker Documentation](https://docs.docker.com/engine/install/ubuntu/#installation-methods)

follow through **Install using the repository**: Set up the repository, Install Docker Engine.

[Post-installation steps for Linux | Docker Documentation](https://docs.docker.com/engine/install/linux-postinstall/)

### Docker document

[Docker run reference](https://docs.docker.com/engine/reference/run/)

## start up (install docker first)

### docker network

- `sudo docker network create web_service`

### docker compose

- `sudo docker compose up -d`
- `sudo docker compose stop`
- `sudo docker compose down`
    - `sudo docker compose down --volumes`
    - `sudo docker compose down --rmi`
- `sudo docker compose rm`

### watcher

- `sudo docker network ls`
- `sudo docker compose ps --all`
- `sudo docker ps -all`
