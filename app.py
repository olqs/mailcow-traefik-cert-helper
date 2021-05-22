from flask import Flask,Response
from flaskext.mysql import MySQL
import yaml
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = os.environ.get("MYSQL_DATABASE_USER", default='mailcow')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get("MYSQL_DATABASE_PASSWORD", default='mailcow')
app.config['MYSQL_DATABASE_PORT'] = os.environ.get("MYSQL_DATABASE_PORT", default=3306)
app.config['MYSQL_DATABASE_DB'] = os.environ.get("MYSQL_DATABASE_DB", default='mailcow')
app.config['MYSQL_DATABASE_HOST'] = os.environ.get("MYSQL_DATABASE_HOST", default='localhost')

TRAEFIK_ROUTER = os.environ.get("TRAEFIK_ROUTER", default="nginx-mailcow-secure")

mysql.init_app(app)

@app.route('/')
def hello():
  try:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT domain from domain;")
    rows=cursor.fetchall()
    tls_domains = []

    for row in rows:
      subdomains = ["main", "imap", "smtp", "pop3", "autodiscover", "autoconfig", "webmail", "email", "mailtest"]
      domains = [ domain + "." + row[0] for domain in subdomains]
      tls_domains += [ { 'main' : "mail." + row[0], 'sans' : domains }]
    traefik_config = { 'http' : 
      { 'routers' : 
        { TRAEFIK_ROUTER : 
          { 'tls' : 
            { 
              'domains' : tls_domains,
              'certresolver' : 'http'
            },
            'endpoints' : 'https',
            'rule' : 'Host(`mailtest.worli.info`)',
            'service' : 'nginx-mailcow@docker',
          }
        }
      }
    }
    response = yaml.dump(traefik_config)
        
    return Response(response, mimetype='text/yaml')
  except Exception as e:
    print(e)
  finally:
    cursor.close()
    conn.close()

