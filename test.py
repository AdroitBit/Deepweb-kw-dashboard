import requests

# response=requests.get("https://onionengine.com/search.php?search=123&submit=Search&page=2")
response=requests.get("https://onionengine.com/search.php",params={
    "search":"123",
    "submit":"Search",
    "page":2
})

print(response)
print(response.text)
