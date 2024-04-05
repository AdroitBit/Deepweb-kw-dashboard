import re
from typing import Dict, List
import requests
from schema import DeepWebInfo



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
            response=requests.get(url,params={"search": keyword, "page": page_index})
            if response.status_code==200:
                print("Request successful!")
                print("Response content:")
                response_text=response.text
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
    print(pull_via_onion_search_engine(["drug", "guns", "hitman"]))