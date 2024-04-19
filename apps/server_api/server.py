from typing import Dict, List, Set, Tuple
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from schema import *
import psutil


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


keyword_and_urls:Dict[str,Set[str]] = {}



@app.post("/push/keyword")
async def push_keyword(request: PushKeyword):
    keyword_and_urls.setdefault(request.keyword, set())
    return {"message": "Data received successfully!"}

@app.post("/push/deepweb-info")
async def push_deepweb_info(request: DeepWebInfo):
    if request.keyword not in keyword_and_urls:
        keyword_and_urls[request.keyword] = set()
    keyword_and_urls[request.keyword].add(request.url)
    return {"message": "Data received successfully!"}

@app.get("/list/keywords")
async def list_keywords():
    return list(keyword_and_urls.keys())

@app.get("/list/urls")
async def list_urls():
    s:Set[str] = set()
    for urls in keyword_and_urls.values():
        s.update(urls)
    return list(s)

@app.get("/list/urls/{keyword}")
async def list_urls_with_keyword(keyword: str):
    
    if keyword not in keyword_and_urls:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return list(keyword_and_urls[keyword])


@app.get("/keyword_and_urls/antd/column_chart")
async def keyword_and_urls_antd_column_chart():
    data = []
    for keyword in keyword_and_urls.keys():
        data.append({
            "label": keyword,
            "value": len(keyword_and_urls[keyword])
        })
    return data

@app.get("/keyword_and_urls/antd/table")
async def keyword_and_urls_antd_datasource():
    data = []
    for keyword in keyword_and_urls.keys():
        for url in keyword_and_urls[keyword]:
            data.append({"keyword": keyword, "url": url})
    return data



@app.get("/server_health")
async def server_health():
    return ServerHealth(
        cpu_percent=psutil.cpu_percent(interval=1),
        memory_percent=psutil.virtual_memory().percent
    )
@app.get("/server_health/antd/gauge")
async def server_health_antd_bar_chart():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    memory_absolute = psutil.virtual_memory().used/1024/1024 # in MB
    memory_absolute_max = psutil.virtual_memory().total/1024/1024 # in MB
    return [
        {
            "label": "CPU",
            "value": cpu_percent,
            "display_label": f"{cpu_percent:.2f}%",
            "highest_value": 100,
        },
        {
            "label":" Memory",
            "value": memory_absolute,
            "display_label": f"{memory_percent:.2f}% | {memory_absolute:.2f} MB",
            "highest_value": memory_absolute_max,
        }
    ]


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000,reload=True)