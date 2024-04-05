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
To build this repo into docker and run its application image`<br>`

```
docker compose up --build


# Build this repo to application image
docker build -t deepweb-scraper:latest .

# remove old container
docker rm -f deepweb-scraper-container

# Run docker container
<!-- docker run -it -d --name deepweb-scraper-container -p 8080:80 deepweb-scraper:latest -->
docker run -it -d --name deepweb-scraper-container deepweb-scraper:latest

```
