import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError


def get_title_from_url(slack_url):
    slack_url = ensure_http_prefix(slack_url)

    try:
        soup_url = BeautifulSoup(requests.get(slack_url).text)

        meta_tag_with_title = soup_url.find('meta', property='og:title')

        if meta_tag_with_title:
            title = meta_tag_with_title.get('content')
        else:
            title = soup_url.find('title').string

    except AttributeError:
        slashes_index = slack_url.find('//')
        dot_separation = slack_url.find('.')
        title = slack_url[slashes_index + 2:dot_separation]

    except ConnectionError:
        raise ConnectionError

    return title


def ensure_http_prefix(slack_url):
    return 'http://' + slack_url if 'http' not in slack_url else slack_url


def text_has_tag(text):
    text = text.strip(" ")
    return True if len(text.split(" ")) > 1 else False


def get_url_from_text(text):
    text = text.strip(" ")
    index_end_of_url = text.find(" ")
    return text if index_end_of_url == -1 else text[:index_end_of_url]


def get_tags_from_text(text):
    if text_has_tag(text):
        text = text.strip(" ")
        index_end_of_url = text.find(" ")
        slack_url_without_url = text[index_end_of_url + 1:]

        if len(slack_url_without_url.split(",")) == 1:
            tags = slack_url_without_url
        else:
            tags = [tag.strip(" ") for tag in slack_url_without_url.split(",")]
            tags = ", ".join(tags)
        return tags
    else:
        return ""
