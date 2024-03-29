from flask import Flask,Response
from flask_mysqldb import MySQL
import json
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_USER'] = os.environ.get("MYSQL_DATABASE_USER", default='mailcow')
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_DATABASE_PASSWORD", default='mailcow')
app.config['MYSQL_PORT'] = os.environ.get("MYSQL_DATABASE_PORT", default=3306)
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DATABASE_DB", default='mailcow')
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_DATABASE_HOST", default='mysql-mailcow')

TRAEFIK_ROUTER = os.environ.get("TRAEFIK_ROUTER", default="nginx-mailcow-secure")
TRAEFIK_CERTRESOLVER = os.environ.get("TRAEFIK_CERTRESOLVER", default="http")
TRAEFIK_HTTPS_ENTRYPOINT = os.environ.get("TRAEFIK_HTTPS_ENTRYPOINT", default="https")
TRAEFIK_MAILCOW_SERVICE = os.environ.get("TRAEFIK_MAILCOW_SERVICE", default="nginx-mailcow@docker")

mysql.init_app(app)

@app.route('/')
def hello():
  try:
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT domain from domain where active=1;")
    rows=cursor.fetchall()
    tls_domains = []

    for row in rows:
      subdomains = ["mail", "imap", "smtp", "pop3", "autodiscover", "autoconfig", "webmail", "email"]
      domains = [ domain + "." + row[0] for domain in subdomains]
      tls_domains += [ { 'main' : "mail." + row[0], 'sans' : domains }]
    traefik_config = { 'http' : 
      { 'routers' : 
        { TRAEFIK_ROUTER : 
          { 'tls' : 
            { 
              'domains' : tls_domains,
              'certresolver' : TRAEFIK_CERTRESOLVER
            },
            'entryPoints' : [ TRAEFIK_HTTPS_ENTRYPOINT ],
            'rule' : 'HostRegexp(`{host:(autodiscover|autoconfig|webmail|mail|email).+}`)',
            'service' : TRAEFIK_MAILCOW_SERVICE
          }
        }
      }
    }
    response = json.dumps(traefik_config,indent=4)
        
    return Response(response, mimetype='text/json')
  except Exception as e:
    print(e)
  finally:
    cursor.close()

