## DO NOT USE THE `certificate.crt` and `privatekey.key` provided in this directory in production!

They are a self-signed certificate, for development and testing. You MUST replace them with valid certificate files when deploying. The recommended method for doing so is using Let's Encrypt via Certbot.

## Creating a certificate and making it available to raptor-web

To do the following, you must already have a domain and have created DNS A/AAAA records to point that domain name to the server you wish to deploy from.

1) Using `certbot`, the following command will generate these files and place them in `/etc/letsencrypt/live/<FQDN>/[fullchain.pem, privkey.pem]`.

    ```bash
    certbot certonly -d <FQDN>
    ```

2) You can then either directly re-locate these files to the `raptor-conf` docker volume, located in `var/lib/docker/volumes/raptor/<dir_name>_raptor-conf`, or create [symlinks](https://www.howtogeek.com/287014/how-to-create-and-use-symbolic-links-aka-symlinks-on-linux/) to the `fullchain.pem` and `privkey.pem` files.

In either case, your newly generate files need to be available to the `raptor-conf` docker volume. Under NO circumstances should the included certificate files be used in production deployments.
