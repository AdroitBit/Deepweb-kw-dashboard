import re
from typing import Dict, List
import requests
from schema import DeepWebInfo


proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# proxies = {
#     'http': 'socks5://127.0.0.1:9050',
#     'https': 'socks5://127.0.0.1:9050'
# }

def pull_via_search_engine_deepweb(keywords: List[str]):
    r:Dict[str,List[str]]={}
    for keyword in keywords:
        r[keyword]=[]
    return r

def pull_via_onion_search_engine(keywords: List[str]):
    r:Dict[str,List[str]]={}
    url="https://onionsearchengine.com/"
    for keyword in keywords:
        r.setdefault(keyword, [])
        for page_index in range(1, 10+1):
            response=requests.get(url,params={"search": keyword, "page": page_index},proxies=proxies)
            if response.status_code==200:
                print("Request successful!")
                print("Response content:")
                response_text=response.text
                print(response_text)
                for url_in_page in re.findall(r"(http)(.*)(\.onion)", response_text):
                    url_in_page="".join(url_in_page)
                    r[keyword].append(url_in_page)
                # print(response.text)
            else:
                print("Failed to make the request. Status code:", response.status_code)
    return r

def pull_in_link_container():
    pass


def merge_dicts(*dict_args: Dict[str, List[str]]) -> Dict[str, List[str]]:
    result = {}
    for dictionary in dict_args:
        for keyword, urls in dictionary.items():
            if keyword not in result:
                result[keyword] = []
            result[keyword].extend(urls)
    return result


if __name__=='__main__':
    # print(pull_via_onion_search_engine(["drug", "guns", "hitman"]))


    import requests
    url="https://check.torproject.org/"
    # response=requests.get(url)
    response=requests.get(url,proxies=proxies)
    print(response.text)
    # from requests_tor import RequestsTor
    # # rt= RequestsTor()
    # rt= RequestsTor(tor_ports=(9050,), tor_cport=9051)
    # url="https://check.torproject.org/"
    # response=rt.get(url)
    # print(response.text)