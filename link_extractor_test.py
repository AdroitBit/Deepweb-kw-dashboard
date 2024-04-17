from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL
base_url = "https://example.com/docs/"

# Sample HTML code with relative URLs
html_code = """
<html>
<body>
<a href="page1.html">Page 1</a>
<a href="../page2.html">Page 2</a>
<a href="/other/page3.html">Page 3</a>
<a href="https://example2.com/page4.html">Page 4</a>
http://yessir.onion
</body>
</html>
"""

# Function to extract and convert relative URLs to absolute URLs
def convert_relative_urls(html, base):
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    
    # Find all 'a' tags (anchor tags) with 'href' attributes
    for a_tag in soup.find_all('a', href=True):
        # Get the href attribute (URL) of the 'a' tag
        href = a_tag['href']
        
        # Convert the relative URL to absolute URL using urljoin
        absolute_url = urljoin(base, href)
        
        # Update the 'href' attribute of the 'a' tag with the absolute URL
        a_tag['href'] = absolute_url

    for input_tag in soup.find_all('input', src=True):
        # this is for tor blocking so we can enter it anyway
        src = input_tag['value']
        absolute_url = urljoin(base, src)
        input_tag['value'] = absolute_url
    
    return str(soup)

# Convert relative URLs in the HTML code to absolute URLs
converted_html = convert_relative_urls(html_code, base_url)

# Parse the modified HTML code
parsed_html = BeautifulSoup(converted_html, "html.parser")

# Extract all URLs from the modified HTML code
all_urls = [link.get('href') for link in parsed_html.find_all('a', href=True)]

# Print the extracted URLs
print("Extracted URLs:")
for url in all_urls:
    print(url)

# Additional: Extract URLs from plain text (outside anchor tags)
plain_text_urls = parsed_html.find_all(string=lambda text: isinstance(text, str) and 'http' in text)
print("\nExtracted URLs from plain text:")
for url in plain_text_urls:
    print(url)
