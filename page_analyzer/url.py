from urllib.parse import urlparse
import validators
from bs4 import BeautifulSoup


MAX_URL_LENGHT = 255


def validate(url):
    error = None
    if not url:
        error = 'Отсутствует URL'
    elif len(url) > MAX_URL_LENGHT:
        error = f'URL превышает {MAX_URL_LENGHT} символов'
    elif not validators.url(url):
        error = 'Некорректный URL'
    return error


def normalize(url):
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}"


def parse_url_info(url_content):
    parsed_info = {}
    soup = BeautifulSoup(url_content, 'html.parser')
    h1_tag = soup.find('h1')
    parsed_info['h1'] = h1_tag.get_text().strip() if h1_tag else ''
    title_tag = soup.find('title')
    parsed_info['title'] = title_tag.get_text().strip() if title_tag else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    if description_tag:
        parsed_info['description'] = description_tag.get('content', '').strip()
    else:
        parsed_info['description'] = ''
    return parsed_info
