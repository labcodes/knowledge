import requests
from bs4 import BeautifulSoup


def get_title_from_url(slack_url):
    slack_url = ensure_http_prefix(slack_url)

    try:
        soup_url = BeautifulSoup(requests.get(slack_url).text)
    except:
        raise ConnectionError

    try:
        meta_tag_with_title = soup_url.find('meta', property='og:title')

        if meta_tag_with_title:
            title = meta_tag_with_title.get('content')
        else:
            title = soup_url.find('title').string

    except AttributeError:
        slashes_index = slack_url.find('//')
        dot_separation = slack_url.find('.')
        title = slack_url[slashes_index + 2:dot_separation]

    return title


def ensure_http_prefix(slack_url):
    return 'http://' + slack_url if 'http' not in slack_url else slack_url
