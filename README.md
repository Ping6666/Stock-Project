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

- `sudo docker compose build`
- `sudo docker compose up -d`
- `sudo docker compose stop`
- `sudo docker compose down`
    - `sudo docker compose down --volumes`
    - `sudo docker compose down --rmi`
- `sudo docker compose rm`

### docker

- `sudo docker stop`
- `sudo docker rm -v`

### watcher

- `sudo docker network ls`
- `sudo docker compose ps -a`
- `sudo docker ps -a`

## BUGs

- fail refreshing crawler files
    - cannot call python core_worker.py with subprocess.Popen()
