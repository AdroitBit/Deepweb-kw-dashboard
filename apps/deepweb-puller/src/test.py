from _base import *

urls=URLs()
urls.add_urls(["https://us.onion","https://whatsapp.onion","https://facebook.onion","https://google.com","https://google.com"])
for i in range(5):
    print(urls.url_index)
    print(urls.get_url().url)
