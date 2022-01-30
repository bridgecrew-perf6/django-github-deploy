Continuous Deployment of Django to Digital Ocean with Docker and GitHub Actions
===============================================================================

---

## Goals

1. Deploy Django to DigitalOcean with Docker
2. Configure GitHub actions to continuously deploy Django to DigitalOcean
3. Use GitHub Packages to store Docker Images
4. Set up Passwordless SSH Login
5. Configure DigitalOcean's Managed Databases for data persistence

---

## GitHub Auth

### Create a GitHub Personal Access Token

With these permissions:

1. write:packages
2. read:packages
3. delete:packages

---

## Setup GitHub Packages

### Build and tag the image

```shell
docker build -f app/Dockerfile -t ghcr.io/GITHUB_USERNAME/GITHUB_REPO/web:latest ./app
```

### Authenticate to GitHub Packages with Docker

```shell
docker login ghcr.io -u GITHUB_USERNAME -p GITHUB_TOKEN
```

### Push the image to the Container registry on GitHub Packages:

```shell
docker push ghcr.io/GITHUB_USERNAME/GITHUB_REPO/web:latest
```

### The package should now be on GitHub packages

Organisation:
https://github.com/orgs/<USERNAME>/packages

Personal:
https://github.com/<USERNAME>?tab=packages

---

## Setup Droplet

### Create a DigitalOcean API Access Token

```shell
# Add it to your local environment
export DIGITAL_OCEAN_ACCESS_TOKEN=[your_digital_ocean_token]
```

### Create the Droplet with Docker pre-installed

```shell
curl -X POST \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITAL_OCEAN_ACCESS_TOKEN'' \
    -d '{"name":"django-docker","region":"sfo3","size":"s-2vcpu-4gb","image":"docker-20-04"}' \
    "https://api.digitalocean.com/v2/droplets"
```

---

## Server SSH Auth

### SSH Access on Server

The root password should be emailed to you.

```shell
# SSH into server
ssh-keygen -t rsa
# Copy your public key to this file
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_rsa
```

### Create a Directory for the app

```shell
ssh -o StrictHostKeyChecking=no root@<YOUR_INSTANCE_IP> mkdir /app
```

---

## Database

### Create a Production DB

```shell
curl -X POST \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITAL_OCEAN_ACCESS_TOKEN'' \
    -d '{"name":"django-docker-db","region":"sfo3","engine":"pg","version":"13","size":"db-s-2vcpu-4gb","num_nodes":1}' \
    "https://api.digitalocean.com/v2/databases"
```

### Get the Connection Information

```shell
# The 'jq' at the end can be installed from homebrew (pretty prints JSON)
curl \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITAL_OCEAN_ACCESS_TOKEN'' \
    "https://api.digitalocean.com/v2/databases?name=django-docker-db" \
  | jq '.databases[0].connection'
```

---

## GitHub Actions

## Add the '.github' directory as shown in this repo

## Add Secrets to GitHub repo Secrets

```shell
# For example:
SECRET_KEY: 9zYGEFk2mn3mWB8Bmg9SAhPy6F4s7cCuT8qaYGVEnu7huGRKW9
SQL_DATABASE: defaultdb
SQL_HOST: django-docker-db-do-user-778274-0.a.db.ondigitalocean.com
SQL_PORT: 25060
SQL_USER: doadmin
SQL_PASSWORD: v60qcyaito1i0h66
NAMESPACE: Github username/org name 
PERSONAL_ACCESS_TOKEN: Github personal access token
DIGITAL_OCEAN_IP_ADDRESS: IP of droplet
```

## Allowed Hosts

Add droplet IP to Django allowed hosts in settings
