# Usage

## Dependencies Installation

- [docker](installation.md#docker)
- [npm & node](installation.md#npm--node)
- [miniconda](installation.md#miniconda)

## Production

### Env setup

- docker

### config files

- `docker-compose.yml`
- `.env`

#### `docker-compose.yml`

copy `docker-compose.all.yml` and name as `docker-compose.yml`

#### `.env`

create a file and name as `.env` with content below

```
# ----- nginx ----- #

UPSTREAM_FRONTEND_IP=frontend
UPSTREAM_BACKEND_IP=backend
```

### open up

```bash
sudo docker compose up -d (--build)
```

### close off

```bash
sudo docker compose down
```

## Development

### Env setup

- docker
- npm & node
- miniconda

### config files

- `docker-compose.yml`
- `.env`

#### `docker-compose.yml`

copy `docker-compose.nginx.yml` and name as `docker-compose.yml`

#### `.env`

create a file and name as `.env` with content below

```
# ----- nginx ----- #

UPSTREAM_FRONTEND_IP=host.docker.internal
UPSTREAM_BACKEND_IP=host.docker.internal
```

### env create

```bash
conda env create -f ./backend/env/environment.yml
```

### open up

```bash
sudo docker compose up -d (--build)

conda activate stock
bash run.sh
```

### close off

```bash
sudo docker compose down
```
