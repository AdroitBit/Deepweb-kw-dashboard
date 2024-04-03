import yaml
import os
import requests
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configure SOCKS proxy (replace with your actual SOCKS proxy settings)
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def main():
    with open("onion_links/collectionors.yaml", "r") as f:
        data = yaml.safe_load(f)
    for link_collector_url in data:
        link_collector_page=requests.get(link_collector_url, proxies=proxies)
        if link_collector_page.status_code != 200:
            print('Failed to make the request. Status code:', link_collector_page.status_code)
            continue
        print(f'Request to {link_collector_url} successful!')
        link_collector_text = link_collector_page.text
        print(link_collector_text)

if __name__ == "__main__":
    main()