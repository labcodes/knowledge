import requests
from bs4 import BeautifulSoup


def get_title_from_url(slack_url):
    if 'http' not in slack_url:
        slack_url = 'http://' + slack_url

    soup_url = BeautifulSoup(requests.get(slack_url).text)
    try:
        title = soup_url.find('meta', property='og:title').get('content')
    except AttributeError:
        title = soup_url.find('title').string

    return title
