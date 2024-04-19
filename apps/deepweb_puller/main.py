import os
from typing import Set
import asyncio

from _base import *


async def main():

    while True:
        print("="*100)
        print("Starting new iteration")
        print("="*100)
        await asyncio.sleep(2)

        keywords=os.getenv("KEYWORDS", "drug")
        keywords = [k.strip() for k in keywords.split(",")]
        while True:
            await asyncio.sleep(0)
            is_declare_success=True
            for keyword in keywords:
                await asyncio.sleep(0)
                response_result = await declare_keyword_to_server_api(keyword)
                if response_result.status_code!=200:
                    is_declare_success=False
                    break
            if is_declare_success:
                break
        process_chunk_size = int(os.getenv("URL_PROCESS_CHUNK_SIZE", 10))
        

        print("="*60)
        print("Obtaining urls from onion engine")
        print("="*60)
        checking_urls:URLs=URLs()
        for keyword in keywords:
            for page_index in range(1,5):
                new_urls=await URL("https://onionengine.com/search.php").obtain_onion_urls_from_page(
                    params={
                        "search":keyword,
                        "page":page_index,
                        "submit":"Search"
                    }
                )
                print("="*60)
                print(f"https://onionengine.com/search.php with keyword {keyword} in page {page_index} provided {len(new_urls)} urls")
                print("="*60)
                checking_urls.add_urls(new_urls)
        print("="*60)
        print("Obtain urls from https://github.com/gt0day/DarkWeb")
        print("="*60)
        new_urls=await URL("https://raw.githubusercontent.com/gt0day/DarkWeb/main/README.md").obtain_onion_urls_from_page(params={})
        print("="*60)
        print(f"https://github.com/gt0day/DarkWeb provided {len(new_urls)} urls")
        print("="*60)
        checking_urls.add_urls(new_urls)


        
        print("="*100)
        checking_urls.randomized()
        print(f"Checking {len(checking_urls)} urls process")
        print("="*100)
        
        checked_count=0
        CHECKING_URLS_LIMIT=int(os.getenv("CHECKING_URLS_LIMIT", 10000))
        while checking_urls.is_empty() == False:
            if checked_count>=CHECKING_URLS_LIMIT:
                print("="*40)
                print(f"Checked {checked_count} urls. Limit is reached.")
                print("="*40)
                break
            tasks=[]
            async def add_if_keyword_appear_in_page(url:URL,keywords:List[str]):
                await url.obtain_page({})
                if url.page_content!="":
                    found_urls=await url.obtain_urls_from_page({})
                    print(f"Found {len(found_urls)} urls in {url.url}")
                    for found_url in found_urls:
                        checking_urls.add_url(found_url)
                    for keyword in keywords:
                        if await url.check_keyword_in_page(keyword):
                            print(f"Keyword {keyword} found in {url.url}")
                            #push that shit to server-api
                            await push_to_server_api(keyword,url)
            count=0
            for url in checking_urls.get_urls(process_chunk_size):
                tasks.append(asyncio.create_task(
                    add_if_keyword_appear_in_page(url, keywords)
                ))
                count+=1
            
            print("="*40)
            print(f"{count} urls are being checked")
            print("="*40)
            await asyncio.gather(*tasks)
            checked_count+=process_chunk_size

        

if __name__=='__main__':
    asyncio.run(main())