# Installation

## docker

### Set up the repository

```bash
# 1. Update the apt package index and install packages to allow apt to use a repository over HTTPS
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# 2. Add Docker’s official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 3. Use the following command to set up the repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Install Docker Engine

```bash
# 1. Update the apt package index
sudo apt-get update

# 2. Install Docker Engine, containerd, and Docker Compose
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 3. docker installation verification
docker --version
```

## npm & node

```bash
# curl
sudo apt-get install curl

# nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

# nvm installation verification (reopen terminal)
command -v nvm

# install npm & node
nvm install --lts

# list of installation
nvm ls

# npm & node installation verification
node --version
npm --version
```

## miniconda

1. find Installer in [link](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links)
2. follow the instruction (and reopen terminal)

```bash
# conda installation verification
conda --version
```

## References

- [Install Docker Engine on Ubuntu | Docker Documentation](https://docs.docker.com/engine/install/ubuntu/#installation-methods)
- [Set up Node.js on WSL 2 | Microsoft Learn](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl)
- [https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links)
