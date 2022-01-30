## GitHub

### Create a GitHub Personal Access Token

With these permissions:

1. write:packages
2. read:packages
3. delete:packages

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

## Digital Ocean

### Create a DigitalOcean API Access Token

Add it to environment

```shell
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

### Check the Status

```shell
curl \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITAL_OCEAN_ACCESS_TOKEN'' \
    "https://api.digitalocean.com/v2/droplets?name=django-docker"
```

### Set up SSH Access on Server

```shell
ssh-keygen -t rsa
# Copy your public key to this file
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_rsa
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
curl \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITAL_OCEAN_ACCESS_TOKEN'' \
    "https://api.digitalocean.com/v2/databases?name=django-docker-db" \
  | jq '.databases[0].connection'
```
