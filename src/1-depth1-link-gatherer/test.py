import requests

# Configure SOCKS proxy (replace with your actual SOCKS proxy settings)
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# URL of the Onion website you want to access
# onion_url = 'http://jgwe5cjqdbyvudjqskaajbfibfewew4pndx52dye7ug3mt3jimmktkid.onion/'
# onion_url = 'http://xjfbpuj56rdazx4iolylxplbvyft2onuerjeimlcqwaihp3s6r4xebqd.onion/'


#breach data
onion_url = "http://breachdbsztfykg2fdaq2gnqnxfsbj5d35byz3yzj73hazydk4vq72qd.onion/"

# Make a GET request using the SOCKS proxy
# response = requests.post(onion_url, proxies=proxies)
response = requests.post(onion_url, proxies=proxies)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print('Request successful!')
    print('Response content:')
    print(response.text)
else:
    print('Failed to make the request. Status code:', response.status_code)