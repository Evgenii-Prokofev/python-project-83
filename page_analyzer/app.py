from flask import (
    Flask, render_template, request, flash,
    redirect, url_for,
)
import requests

from dotenv import load_dotenv
import os
from .url import validate, normalize
from .url import parse_url_info
from .db import add_url_into_db, get_url_by_name
from .db import get_url_by_id, get_urls_list
from .db import get_check_by_url_id
from .db import add_url_check_into_db


load_dotenv()


app = Flask(__name__)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def get_index():
    return render_template('index.html'), 200


@app.route('/urls', methods=["POST"])
def add_url():
    url = request.form.get('url')
    if not url:
        flash('Заполните это поле', 'alert-danger')
        return render_template('index.html'), 422
    error = validate(url)
    if error:
        flash(error, 'alert-danger')
        return render_template('index.html'), 422
    normalize_url = normalize(url)
    url_name = get_url_by_name(normalize_url)
    if url_name:
        id = url_name.id
        flash('Страница уже существует', 'alert-info')
        return redirect(url_for('get_url', id=id))
    id = add_url_into_db(url)
    flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_url', id=id))


@app.route('/urls/<int:id>', methods=["GET"])
def get_url(id):
    url = get_url_by_id(id)
    if url is None:
        flash('Запрашиваемая страница не найдена', 'alert-danger')
        return render_template('index.html'), 404
    checks = get_check_by_url_id(id)
    return render_template(
        'url_info.html',
        url=url,
        checks=checks,
    )


@app.route('/urls', methods=["GET"])
def get_urls():
    saved_urls = get_urls_list()
    return render_template(
        'urls_list.html',
        urls=saved_urls,
    )


@app.route('/urls/<int:id>/checks', methods=["POST"])
def check_urls(id):
    url = get_url_by_id(id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('get_url', id=id))
    check_url_info = parse_url_info(response.text)
    check_url_info['url_id'] = id
    check_url_info['status_code'] = response.status_code
    add_url_check_into_db(check_url_info)
    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('get_url', id=id))


if __name__ == '__main__':
    app.run()
