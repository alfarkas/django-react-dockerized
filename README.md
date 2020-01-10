# About me
Basic DRF + React app, using containers with Docker and Docker Compose.

# Basic commands

You can run commands inside the containers using the 'execute' file, indicating the container destination: frontend/backend
 - `./execute backend manage {command}`
 - `./execute frontend install {package}`

# Befor start
- Create a .env with the variables of the .env.example and complete the blanks with values.

## Containers
### Development

Generate SSL certificates to enable HTTPS:
- `cd ssl`
- `./self_signed`
- Delete the folders created
- Run it again `./self_signed`

Start and build the containers:

- `./build_backend`
- `./build_frontend`

Start all containers:

- `docker-compose -f docker-compose-dev.yml up` or `docker-compose -f docker-compose-dev.yml up -d` to run them in background.

Restart all containers:

- `docker-compose -f docker-compose-dev.yml restart`

Stop all containers:

- `docker-compose -f docker-compose-dev.yml stop`

## Backend
Create a super-user:

- `./execute backend manage createsuperuser`

Collect static files:

- `./execute backend manage collectstatic`

Apply migrations to the DB:

- `./execute backend manage migrate`
