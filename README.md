# Deepweb-Scraper







To build this repo into docker and run its application image
```
# Build this repo to application image
docker build -t deepweb-scraper:latest .

# remove old container
docker rm -f deepweb-scraper-container

# Run docker container
docker run -it -d --name deepweb-scraper-container -p 8080:80 deepweb-scraper:latest

```
