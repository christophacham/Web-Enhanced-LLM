import requests
from bs4 import BeautifulSoup


def get_web_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def parse_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text


url = 'https://example.com'
html_content = get_web_content(url)
if html_content:
    text_content = parse_content(html_content)
    print(text_content)
