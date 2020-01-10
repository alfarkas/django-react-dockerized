# About me
Basic DRF + React app, using containers with Docker and Docker Compose in a single local Swarm node.

# Basic commands

You can run commands inside the containers using the 'execute' file, indicating the container destination: frontend/backend
 - `./execute backend manage {command}`
 - `./execute frontend install {package}`

## Containers
### Development

Generate SSL certificates to enable HTTPS:
- `cd ssl`
- `./self_signed`
- (if it doesn't work) 
   - Delete the folders created
   - Run it again `./self_signed`

Start and build the containers:

- `./build_backend`
- `./build_frontend`

Initialize the swarm

 `docker swarm init`

e.g. `docker-compose -f docker-compose-dev.yml build frontend`

Start the stack:

- `docker stack deploy -c docker-compose-dev.yml nameOfStack`

Take down the stack:

- `docker stack rm nameOfStack`

Scale a service (most likely celery workers):

- `docker service scale nameOfService=Amount`

## Backend
Create a super-user:

- `./execute backend manage createsuperuser`

Collect static files:

- `./execute backend manage collectstatic`

Apply migrations to the DB:

- `./execute backend manage migrate`
