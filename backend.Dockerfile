FROM python:3.8-slim-buster
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        python3-psycopg2 \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pipenv

WORKDIR /opt/backend
RUN useradd -m container_user
RUN chown -R container_user:container_user /opt/backend

COPY src/backend/Pipfile ./
COPY src/backend/Pipfile.lock ./
RUN pipenv install --system

# Copy entrypoint
COPY src/backend/entrypoint.sh ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/opt/backend/entrypoint.sh"]
#CMD ["manage", "runserver", "0.0.0.0:8000"]