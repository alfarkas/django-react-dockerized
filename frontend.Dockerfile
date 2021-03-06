FROM node:12.13.1-alpine3.9 as dev

WORKDIR /usr/src/

# copy both 'package.json' and 'package-lock.json' (if available)
COPY src/frontend/package.json /usr/src/
COPY src/frontend/package-lock.json /usr/src/
COPY src/frontend/public /usr/src/public
COPY src/frontend/src /usr/src/src

# install project dependencies
RUN npm install

# Copy entrypoint
COPY src/frontend/entrypoint.sh /usr/src/entrypoint.sh

ENTRYPOINT ["/usr/src/entrypoint.sh"]

EXPOSE 3000

RUN npm run build 

FROM nginx:1.17.6 as prod

COPY --from=dev /usr/src/build /opt/frontend