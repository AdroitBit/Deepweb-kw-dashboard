from typing import Dict, List
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import prometheus_client
import uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


deepweb_info_appear_count = prometheus_client.Counter(
    "deepweb_info_amount_appear",
    "Amount of times the keyword appears in the deep web",
    labelnames=["keyword", "appear_count"],
)


deepweb_info_metrices = prometheus_client.Counter(
    "deepweb_info_amount_appear",
    "Amount of times the keyword appears in the deep web",
    labelnames=["keyword", "url"],
)


# deepweb_info_amount_appear = prometheus_client.Counter(
#     "",
#     "Amount of times the keyword appears in the deep web",
#     labelnames=["keyword", "url"],
# )

# deepweb_info_amount_appear = prometheus_client.Summary(
#     "deepweb_info_processing_seconds",
#     "Time taken to process deep web information",
#     labelnames=["keyword", "url"],
# )


class DeepWebInfo(BaseModel):
    keyword_and_url: Dict[str, List[str]]

@app.post("/push-deepweb-info")
async def push_deepweb_info(request: DeepWebInfo) -> dict:
    for keyword, urls in request.keyword_and_url.items():
        deepweb_info_appear_count.labels(keyword=keyword, appear_count=len(urls)).inc()
        for url in urls:
            deepweb_info_metrices.labels(keyword=keyword, url=url).inc()


            print(f"Keyword: {keyword}, URL: {url}")
    return {"message": "Data received successfully!"}

@app.get("/metrics")
async def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest(),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)