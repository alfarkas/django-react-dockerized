# About me
Basic DRF + React app, using containers with Docker and Docker Compose.

# Basic commands

## Containers
### Development

Generate SSL certificates to enable HTTPS:
- `cd ssl`
- `./self_signed`

Start and build the containers:

- `docker-compose -f docker-compose-dev.yml build`

If you want to build a specific container, just add the name it has in the docker-compose file at the end. 

e.g. `docker-compose -f docker-compose-dev.yml build frontend`

Start all containers:

- `docker-compose -f docker-compose-dev.yml up`

Restart all containers:

- `docker-compose -f docker-compose-dev.yml restart`

## Backend
Create a super-user:

- `docker-compose -f docker-compose-dev.yml run backend createsuperuser`

Collect static files:

- `docker-compose -f docker-compose-dev.yml run backend collectstatic`

Apply migrations to the DB:

- `docker-compose -f docker-compose-dev.yml run backend migrate`
