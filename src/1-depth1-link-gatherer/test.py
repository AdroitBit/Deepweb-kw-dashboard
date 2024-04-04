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
# response = requests.post(onion_url, proxies=proxies,data={
#     'ctl00$ContentPlaceHolder1$TxtSearch':'yanothai.c@ku.th',
#     "ctl00$ContentPlaceHolder1$SearchType":'Email',
#     "ctl00$ContentPlaceHolder1$ChkShowAll":True,
# })


form_data = {
    # '__VIEWSTATE': '__VIEWSTATE_value',
    '__VIEWSTATE': '/wEPDwULLTE2NTE2NzQ1NzcPFgIeDUFudGlYc3JmVG9rZW4FIDQ3NGRlNmJhY2ZmOTQ3NzJiZDQ5NWZkYjQ5NWIwMWVmFgJmD2QWAgIDD2QWAgIBD2QWAmYPZBYCAgUPEA8WAh4HRW5hYmxlZGhkZGRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBSRjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJENoa1Nob3dBbGw/3SFSh5Hco/utUsjOAfRkmlmK+i4SrP/Hk1GDQtYK+Q==',
    '__VIEWSTATEGENERATOR': '94D56744',
    # '__EVENTVALIDATION': '__EVENTVALIDATION_value',
    '__EVENTVALIDATION': '/wEdAAgISRSBeNlRP7sBQ7hILeQKWKrNrxJ9H/Sq1/LwagLSvfuTvlXhUaV0lpXjmWrHYXlCwAVToG4T5YUsihCDBa9MfteltqTNG3zxqCR+jDI4SqEN3PJMAfsZ3M5euJgXnRordMAAB2G3bzYF2ekjNxJjeHRGm7AHgPLi1Rc2/WxSAvMu1534+p0sKMSqz+04awOV1TmrFwKwY4YRepkvniN/',
    'ctl00$ContentPlaceHolder1$TxtSearch': 'search_term',
    'ctl00$ContentPlaceHolder1$SearchType': 'Email',  # Or 'Username' depending on the search type
    'ctl00$ContentPlaceHolder1$ChkShowPass': 'on',  # If the checkbox is checked
    'ctl00$ContentPlaceHolder1$ChkShowAll': 'on',  # If the checkbox is checked
    'ctl00$ContentPlaceHolder1$HiddenJS': 'Enable',
    'ctl00$ContentPlaceHolder1$BtnSearch': 'Search'
}

# Send the POST request
response = requests.post(onion_url, data=form_data,proxies=proxies)


# Check if the request was successful (status code 200)
if response.status_code == 200:
    print('Request successful!')
    print('Response content:')
    print(response.text)
else:
    print('Failed to make the request. Status code:', response.status_code)