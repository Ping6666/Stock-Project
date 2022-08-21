# stock project

version: v0.7.6.6.7

## install docker and docker-compose

[Install Docker Engine on Ubuntu | Docker Documentation](https://docs.docker.com/engine/install/ubuntu/#installation-methods)

follow through **Install using the repository**: Set up the repository, Install Docker Engine.

[Post-installation steps for Linux | Docker Documentation](https://docs.docker.com/engine/install/linux-postinstall/)

### Docker document

[Docker run reference](https://docs.docker.com/engine/reference/run/)

## start up (install docker first)

### docker network

- `sudo docker network create $net_name`

### docker compose

- `sudo docker compose up [-d]`

### docker

- `sudo docker stop $container_name`
- `sudo docker rm -v $container_name`

### prune

- `docker system prune [-a]`
- `docker container prune [--filter "until=12h"]`
- `sudo docker image prune [-a]`

### watcher

- `sudo docker compose ps -a`
- `sudo docker ps -a`

* `sudo docker logs $container_name`

- `sudo docker image ls`
- `sudo docker volume ls`
- `sudo docker network ls`

## ENV

### inside docker

need to change all path about file_base to "./"
add "core." to path

### outside docker

need to change all path about file_base to "../"
