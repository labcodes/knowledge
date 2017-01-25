import requests
from bs4 import BeautifulSoup

def get_title_from_url(slack_url):
    soup_url = BeautifulSoup(requests.get(slack_url).text)
    title = soup_url.find('meta', property='og:title').get('content')

    if not title:
        title = soup_url.find('title').string

    return title
