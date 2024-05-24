# Deepweb-Scraper

Currently It is best to run this repo with CSI Linux.`<br>`
This is because CSI Linux have default configuration that essential for OSINT (Open Source Intelligence) tools.`<br>`

And there is just no CSI Linux for Docker yet.

So the work around for user is VirtualBox with CSI Linux image : `https://csilinux.com/`

```
python3 src/main.py
```

Docker (WIP) (waiting for CSI Linux docker image)`<br>`
As CSI Linux docker image is not available yet.`<br>`
To build this repo into docker and run its application image `<br>`

```


# start docker engine
sudo systemctl start docker # on linux. Or run docker desktop on windows

# Uncompose 
docker compose down

# Compose this repo into container and run
docker compose up --build --force-recreate # this will run in foreground

or 

docker compose up -d --build --force-recreate  # for detached mode


```

PORT expose according to docker-compose.yml

```

```
