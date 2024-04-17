from typing import Dict, List, Set, Tuple
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import prometheus_client
import uvicorn
from schema import DeepWebInfo


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


keyword_and_urls:Dict[str,Set[str]] = {}

keyword_and_urls_gauge = prometheus_client.Gauge(
    "keyword_and_urls_gauge",
    "Gauge of the amount of urls per keyword",
    labelnames=["keyword"],
)

keyword_and_urls_histogram = prometheus_client.Histogram(
    "keyword_and_urls_histogram",
    "Histogram of the amount of urls per keyword",
    labelnames=["keyword"],
    buckets=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
)

urls_lister = prometheus_client.Counter(
    "urls_lister",
    "Listing urls",
    labelnames=["url"],
)




@app.post("/push-deepweb-info")
async def push_deepweb_info(request: DeepWebInfo):
    if request.keyword not in keyword_and_urls:
        keyword_and_urls[request.keyword] = set()
    keyword_and_urls[request.keyword].add(request.url)
    #update gauge
    keyword_and_urls_gauge.labels(request.keyword).set(len(keyword_and_urls[request.keyword]))
    #update histogram
    keyword_and_urls_histogram.labels(request.keyword).observe(len(keyword_and_urls[request.keyword]))
    #update counter (lister)
    urls_lister.labels(request.url).inc()

    return {"message": "Data received successfully!"}

@app.get("/metrics")
async def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest(),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
    # try:
    #     _server_api_ip = socket.gethostbyname('tor_proxy')
    # except socket.gaierror:
    #     print("Error:", "Failed to get the IP address of the tor proxy. torproxy container might not be started yet.")
    #     sys.exit(1)
    # uvicorn.run(app, )