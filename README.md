# Raptor-Web

### A CMS for game server communities

A Django Project containing multiple applications (including a Discord Bot) that can be used by game server communities to host their information and keep track of players.

Currently the app only supports Minecraft servers, and is under heavy development.

Originally built to replace this [Enjin spaghetti](https://web.archive.org/web/20220317144720/https://www.shadowraptornetwork.com/) that encompassed ShadowRaptor Network's website.

I plan to release this as a CMS similar to Enjin (but better!), however there is a long list of features to be implemented still. Stay tuned! As of now, basic instructions for deploying the application are provided below. Full documentation will be written as the application matures.

## Deploying raptor-web

Raptor-web can only be deployed using Docker. [The system must have Docker Engine and Docker Compose installed.](https://docs.docker.com/compose/install/)

1) Clone this repository to a location on the host you wish to deploy the app on.

2) Follow the instructions [in the config README](https://github.com/zediious/raptor-web/blob/main/config/README.md) to set up and configure the environment variables for the project.

3) Run `docker compose up -d` to deploy the web server, raptor-web application, and database stack.

4) Read the [docker/nginx README](https://github.com/zediious/raptor-web/blob/main/docker/nginx/conf.d/README.md) and ensure you have generated a new certificate for your domain name and made that available to the application before deploying.

## Docker Volumes

Four docker volumes are created and used by the docker compose file, to persist certain data. Below are you will find each of these followed by a description of their purpose and what you can do with them;

### raptor-conf

- Stores the webserver configuration, and more importantly the web server certificate and private key. By default, the certificate is a self-signed certificate. As outlined in the [docker/nginx README](https://github.com/zediious/raptor-web/blob/main/docker/nginx/conf.d/README.md), you MUST change these to a valid certificate and private key. Follow the instructions at the above README link to see how you can generate the certificate and private key.

### raptor-db

- Stores the mysql database/tables utilized by the application, as well as the base mariadb configuration.

### raptor-logs

- Stores the logs output by the application.

### raptor-media

- Stores user-uploaded media files. This volume is added to by raptor-web, and read from by NGINX to serve the media files.
