import asyncio
import re
from typing import Any, Dict
import requests
import yaml
import os
import httpx
os.chdir(os.path.dirname(os.path.abspath(__file__)))


proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}


async def fetch_data(url:str,method:str,params:Dict[str,Any],links:Dict[str,Any]):
    async with httpx.AsyncClient() as client:
        client.proxies = proxies
        if method == "GET":
            response = await client.get(url,params=params)
        elif method == "POST":
            response = await client.post(url,data=params)
        if response.status_code == 200:
            page=response.text
            pattern = r"(http|https)(://)([^\s\n\"<]+)"
            for link in re.findall(pattern, page):
                link = ''.join(link).strip()
                links[link] = None
            print(f'Request successful on {url}!')
        else:
            print(f'Failed to make the request on {url}. Status code:', response.status_code)


async def main():
    links_config=None
    links:Dict[str,Any] = {}
    with open("links.yaml", "r") as file:
        links_config = yaml.safe_load(file)

    tasks=[]
    for link_config in links_config["collectioners"]:
        
        tasks.append(fetch_data(
            link_config["url"],
            link_config["method"],
            link_config["params"],
            links
        ))
    await asyncio.gather(*tasks)





    with open("result-depth1.yaml", "w") as file:
        yaml.dump(links, file)



if __name__ == "__main__":
    asyncio.run(main())
