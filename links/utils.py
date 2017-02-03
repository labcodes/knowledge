import requests
from bs4 import BeautifulSoup


def get_title_from_url(slack_url):
    slack_url = ensure_http_prefix(slack_url)

    try:
        soup_url = BeautifulSoup(requests.get(slack_url).text)
    except:
        raise ConnectionError

    try:
        title = soup_url.find('meta', property='og:title')

        if title:
            title = soup_url.get('content')
        else:
            title = soup_url.find('title').string

    except AttributeError:
        title = soup_url.find('title').string

    return title


def ensure_http_prefix(slack_url):
    return 'http://' + slack_url if 'http' not in slack_url else slack_url
