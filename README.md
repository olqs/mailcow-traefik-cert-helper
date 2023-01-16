# mailcow-traefik-cert-helper

Webservice to generate traefik config for email domains configured in mailcow database
This app/container is used in the german howtos
* https://worli.info/mailcow-traefik-automatisch-zertifikate-fuer-email-domaenen-generieren/
* https://goneuland.de/mailcow-e-mail-komplettsytem-mit-antivirus-spam-filer-webmail-webfrontend-installieren-mittels-docker-und-traefik/

## Configuration
The complete configuration is handled with environment variables

* Database Settings
  * MYSQL_DATABASE_HOST default mysql-mailcow
  * MYSQL_DATABASE_PORT default 3306
  * MYSQL_DATABASE_DB default mailcow
  * MYSQL_DATABASE_USER default mailcow
  * MYSQL_DATABASE_PASSWORD default mailcow
* Traefik Configuration
  * TRAEFIK_ROUTER default nginx-mailcow-secure
  * TRAEFIK_CERTRESOLVER default http
  * TRAEFIK_HTTPS_ENTRYPOINT default https
  * TRAEFIK_MAILCOW_SERVICE default nginx-mailcow@docker

## TODO
Implement environment variables for following traefik configurations:
* subdomains which are generated, currently: "mail", "imap", "smtp", "pop3", "autodiscover", "autoconfig", "webmail", "email"
