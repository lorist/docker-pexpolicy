# docker-pexpolicy

```https://github.com/lorist/docker-pexpolicy.git```

```cd docker-pexpolicy```
Build and run:
```docker-compose up --build -d```

Create the DB:
```docker-compose run web /usr/local/bin/python create_db.py```

Create an external policy to point to http://<docker_host_ip>

To create VMRs browse to http://<docker_host_ip>

TODO: push to Docker Hub and create a docker swarm and stack option

