from urllib.parse import urlparse
import validators


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
    url_read = urlparse(url)
    return url_read.scheme + '://' + url_read.netloc
