from flask import (
    Flask, render_template, request, flash,
    redirect, url_for,
)

from dotenv import load_dotenv
import os
from .url import validate, normalize
from .db import add_url_into_db, get_url_by_name
from .db import get_url_by_id, get_urls_list


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
    else:
        id = add_url_into_db(url)
        flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_url', id=id))


@app.route('/urls/<int:id>', methods=["GET"])
def get_url(id):
    url = get_url_by_id(id)
    if url is None:
        flash('Запрашиваемая страница не найдена', 'alert-danger')
        return render_template('index.html'), 404
    return render_template(
        'url_info.html',
        url=url,
    )


@app.route('/urls', methods=["GET"])
def get_urls():
    saved_urls = get_urls_list()
    return render_template(
        'urls_list'.html,
        urls=saved_urls,
    )


if __name__ == '__main__':
    app.run()
