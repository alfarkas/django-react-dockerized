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

Build the containers:

- `./build_backend`
- `./build_frontend --target=dev` for local development 
- `./build_frontend` for production

Start all containers:

- `docker-compose -f docker-compose-dev.yml up` or `docker-compose -f docker-compose-dev.yml up -d` to run them in background.

Stop all containers:

- `docker-compose -f docker-compose-dev.yml down`

Restart all containers:

- `docker-compose -f docker-compose-dev.yml restart`

Stop all containers:

- `docker-compose -f docker-compose-dev.yml stop`

## Backend
Apply migrations to the DB:

- `./execute backend manage migrate`

Create a super-user:

- `./execute backend manage createsuperuser`

Collect static files:

- `./execute backend manage collectstatic`

##  Project configuration

Create a file inside backend.project called `local_settings.py` and paste the code from `local_settings.example.py`
(if you don't have a sentry url/id, comment this code in your `local_settings.py` after paste)

Create a file in the root of the project (same level as README.md) called `.env`, paste the code from `.env.example` and complete it with your credentials.