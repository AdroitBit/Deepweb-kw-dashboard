


import re
import socket
import ssl
import sys
from typing import Any, Dict, List, Union
from urllib.parse import urljoin
import aiohttp
import aiohttp.client_exceptions
from aiohttp_socks import ProxyConnectionError, ProxyConnector, ProxyError, ProxyTimeoutError
from bs4 import BeautifulSoup
from schema import DeepWebInfo, PushKeyword


class ResponseResult:
    def __init__(self, status_code: int=0, content: bytes=b"",content_type:str="", request_from_url:str=""):
        self.status_code = status_code
        self.content = content
        self.content_type=content_type
        self.request_from_url=""

    def is_html(self):
        return "text/html" in self.content_type
    def is_json(self):
        return "application/json" in self.content_type
    def is_xml(self):
        return "application/xml" in self.content_type
    def is_text(self):
        return "text/plain" in self.content_type
    
    def get_text(self):
        return self.content.decode('utf-8')
    

async def _request_get_on_url(url:str,params:Dict[str,str],use_tor:bool=True) -> ResponseResult:
    print("called get on",url,params)
    if use_tor==True:
        try:
            _tor_proxy_ip = socket.gethostbyname('tor_proxy')
        except socket.gaierror:
            print("Error:", "Failed to get the IP address of the tor proxy. torproxy container might not be started yet.")
            return ResponseResult()
    
    print("performing get on",url,params)
    try:
        if use_tor==False:
            async with aiohttp.ClientSession() as session:
                async with session.get(url,params=params) as response:
                    content_type=response.headers.get('content-type','')
                    return ResponseResult(response.status,await response.read(),content_type,url)
        if use_tor==True:
            async with aiohttp.ClientSession(connector=ProxyConnector.from_url(f'socks5://{_tor_proxy_ip}:9050')) as session:
            # async with aiohttp.ClientSession() as session:
                async with session.get(url,params=params) as response:
                    content_type=response.headers.get('content-type','')
                    return ResponseResult(response.status,await response.read(),content_type,url)
    except Exception as e:
        print("Error:",str(e),url,params)
        return ResponseResult()
    return ResponseResult()
        
async def _request_post_on_url(url:str,data:Dict[str,Any]={},json:Dict[str,Any]={},use_tor:bool=False) -> ResponseResult:
    print("called post on",url,data)
    if use_tor==True:
        try:
            _tor_proxy_ip = socket.gethostbyname('tor_proxy')
            connector=ProxyConnector.from_url(f'socks5://{_tor_proxy_ip}:9050')
        except socket.gaierror:
            print("Error:", "Failed to get the IP address of the tor proxy. torproxy container might not be started yet.")
            return ResponseResult()
    else:
        connector=None
    
    
    print("performing post on",url,data,json)
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            if data:
                async with session.post(url,data=data) as response:
                    return ResponseResult(response.status,await response.read(),response.headers.get('content-type',''),url)
            if json:
                async with session.post(url,json=json) as response:
                    return ResponseResult(response.status,await response.read(),response.headers.get('content-type',''),url)
    except Exception as e:
        print("Error:",str(e),url,data,json)
        return ResponseResult()
    return ResponseResult()


class URL:
    """URL class to handle requests and responses"""
    def __init__(self, url:str,use_tor:bool=True):
        self.url = url
        self.response = ResponseResult()
        self.page_content:str=""
        self.use_tor=use_tor
    async def make_get_request(self,params:Dict[str,str]):
        self.response = await _request_get_on_url(self.url,params,self.use_tor)
        return self.response
    
    async def make_post_request(self,data:Dict[str,str]={},json:Dict[str,str]={}):
        self.response = await _request_post_on_url(self.url,data=data,json=json,use_tor=self.use_tor)
        return self.response

    async def obtain_page(self,params:Dict[str,str]):
        if self.page_content!="":
            return self.page_content
        else:
            self.response = await self.make_get_request(params)
            if self.response is None:
                print("Can't get page from url:",self.url,"response is None")
                self.page_content=""
            if self.response.is_html():
                try:
                    self.page_content=self.response.get_text()
                except UnicodeDecodeError:
                    print("Can't get html text from url:",self.url,"UnicodeDecodeError")
                    self.page_content=""
            elif self.response.is_text():
                try:
                    self.page_content=self.response.get_text()
                except UnicodeDecodeError:
                    print("Can't get plain text from url:",self.url,"UnicodeDecodeError")
                    self.page_content=""
            else:
                print("Can't get page from url:",self.url,"content_type:",self.response.content_type,"status_code:",self.response.status_code)
                self.page_content=""
            return self.page_content
        
    async def obtain_json(self,params:Dict[str,str]):
        self.response = await self.make_get_request(params)
        if self.response.is_json():
            return self.response.get_text()
        else:
            raise Exception("Requested URL is Not a json page")
        

    async def obtain_urls_from_page(self,params:Dict[str,str]) -> List[str]:
        page = await self.obtain_page(params)
        if not page:
            return []
        urls:List[str]=[]
        soup = BeautifulSoup(page, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(self.url, href)
            a_tag['href'] = absolute_url
            urls.append(absolute_url)

        for form_tag in soup.find_all('form', action=True):
            action = form_tag['action']
            absolute_url = urljoin(self.url, action)
            form_tag['action'] = absolute_url
            urls.append(absolute_url)

        # for link in soup.find_all('link', href=True):
        #     href = link['href']
        #     absolute_url = urljoin(self.url, href)
        #     link['href'] = absolute_url
        #     urls.append(absolute_url)

        # for script in soup.find_all('script', src=True):
        #     src = script['src']
        #     absolute_url = urljoin(self.url,src)
        #     script['src'] = absolute_url
        #     urls.append(absolute_url)
        return urls
    
    async def obtain_onion_urls_from_page(self,params:Dict[str,str]) -> List[str]:
        pattern=r"http[\S]+\.onion"
        page = await self.obtain_page(params)
        if not page:
            return []
        found_strs=re.findall(pattern,page)
        urls=[]
        for found_str in found_strs:
            url:str=""
            if isinstance(found_str,str):
                url=found_str
            elif isinstance(found_str,tuple):
                url=''.join(found_str)
            if "tor2web" in url:
                continue
            if "onionsearchengine" in url:
                continue
            if "onionengine" in url:
                continue
            urls.append(url)
        return list(set(urls))
    
    async def check_keyword_in_page(self,keyword:str):
        page = await self.obtain_page({})
        if not page:
            return False
        return keyword in page
    
    def __eq__(self,other:Union[str,'URL']):
        if isinstance(other,str):
            return self.url==other
        elif isinstance(other,URL):
            return self.url==other.url


class URLs():
    def __init__(self):
        self._urls:List[URL] = []
        self._url_index=0
        self._bypass_urls=[
            "https://eu.onion",
            "https://us.onion",
            "https://whatsapp.onion"
        ]
    def add_url(self,url:str):
        if url not in self._bypass_urls:
            # print("Checking for adding url :",url)
            is_already_in_the_list:bool = False
            for url_obj in self._urls:
                if url_obj.url==url:
                    is_already_in_the_list=True
                    break
            if is_already_in_the_list==False:
                # print("Adding url:",url)
                self._urls.append(URL(url))
    def add_urls(self,urls:List[str]):
        for url in urls:
            self.add_url(url)

    def get_url(self):
        url_index=self._url_index
        self._url_index+=1
        if self.is_empty():
            return None
        if url_index>len(self._urls)-1:
            return None
        return self._urls[url_index]
    def get_urls(self,count:int) -> List[URL]:
        r_urls=[]
        while len(r_urls)<count:
            popped_url=self.get_url()
            if popped_url is None:
                break
            r_urls.append(popped_url)
        return r_urls
    def __len__(self):
        return len(self._urls)
    def is_empty(self):
        return len(self._urls)==0 or self._url_index>=len(self._urls)
    def randomized(self):
        import random
        random.shuffle(self._urls)
    


async def push_to_server_api(keyword:str,url:URL):
    print(f"Push {url.url} to server-api")

    try:
        _server_api_ip = socket.gethostbyname('server_api')
    except socket.gaierror:
        print("Error:", "Failed to get the IP address of the server_api")
        sys.exit(1)
        # return ResponseResult()
    data=DeepWebInfo(
        keyword=keyword,
        url=url.url
    )
    response=await URL(f"http://{_server_api_ip}:5000/push/deepweb-info",use_tor=False).make_post_request(json=data.dict())
    # response=await URL(f"http://localhost:5000/push-deepweb-info",use_tor=False).make_post_request(data.dict())
    # response = await URL(f"http://158.108.7.231:5000/push-deepweb-info",use_tor=False).make_post_request(data.dict())
    if response.status_code==200:
        print("Pushed to server-api with response:",response.get_text())
    else:
        print("Failed to push to server-api with response:",response.get_text())
    return response

async def declare_keyword_to_server_api(keyword:str):
    print(f"Declare {keyword} to server-api")
    try:
        _server_api_ip = socket.gethostbyname('server_api')
    except socket.gaierror:
        print("Error:", "Failed to get the IP address of the server_api")
        sys.exit(1)
        # return ResponseResult()
    response=await URL(f"http://{_server_api_ip}:5000/push/keyword",use_tor=False).make_post_request(json=PushKeyword(keyword=keyword).dict())
    if response.status_code==200:
        print("Declared to server-api with response:",response.get_text())
    else:
        print("Failed to declare to server-api with response:",response.status_code,response.get_text())
    return response