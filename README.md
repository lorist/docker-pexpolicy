# docker-pexpolicy

Nginx fronting a flask app that offers external policy for Pexip VMRs stored in a postgresql DB.


```https://github.com/lorist/docker-pexpolicy.git```

```cd docker-pexpolicy```
Build and run:
```docker-compose up --build -d```

Create the DB:
```docker-compose run web /usr/local/bin/python create_db.py```

Create an external policy to point to http://<docker_host_ip>

To create VMRs browse to http://<docker_host_ip>

```
docker-compose ps
               Name                              Command               State            Ports
------------------------------------------------------------------------------------------------------
orchestrating-docker-pex_data_1       docker-entrypoint.sh true        Exit 0
orchestrating-docker-pex_nginx_1      /usr/sbin/nginx                  Up       0.0.0.0:80->80/tcp
orchestrating-docker-pex_postgres_1   docker-entrypoint.sh postgres    Up       0.0.0.0:5432->5432/tcp
orchestrating-docker-pex_web_1        /usr/local/bin/gunicorn -w ...   Up       5000/tcp
```


TODO: push to Docker Hub and create a docker swarm and stack option

