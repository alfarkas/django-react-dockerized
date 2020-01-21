# About me
Basic DRF + React app, using containers with Docker and Docker Compose.

# Basic commands

You can run commands inside the containers using the 'execute' file, indicating the container destination: frontend/backend
 - `./execute backend manage {command}`
 - `./execute frontend install {package}`

## Containers
### Development

Generate SSL certificates to enable HTTPS:
- `cd ssl`
- `./self_signed`
- Delete the folders created
- Run it again `./self_signed`

Build the containers:

- `./build_backend`
- `./build_frontend --target=dev` for local development 
- `./build_frontend` for production

If you want to build a specific container, just add the name it has in the docker-compose file at the end. 

e.g. `docker-compose -f docker-compose-dev.yml build frontend`

Start all containers:

- `docker-compose -f docker-compose-dev.yml up`

Stop all containers:

- `docker-compose -f docker-compose-dev.yml down`

Restart all containers:

- `docker-compose -f docker-compose-dev.yml restart`

## Backend
Apply migrations to the DB:

- `./execute backend manage migrate`

Create a super-user:

- `./execute backend manage createsuperuser`

Collect static files:

- `./execute backend manage collectstatic`

##  Project configuration

Create a file inside backend.hci called `local_settings.py` and paste the code from `local_settings.example.py`
(if you don't have a sentry url/id, comment this code in your `local_settings.py` after paste)

Create a file in the root of the project (same level as README.md) called `.env`, paste the code from `.env.example` and complete your credentials.