from flask import (
    Flask, render_template, request, flash,
)

from dotenv import load_dotenv
import os
from .url import validate


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def get_index():
    return render_template('index.html'), 200


@app.route('/urls', methods=["POST"])
def add_url():
    url = request.form.get('url')
    error = validate(url)
    if error:
        flash(error, 'alert-danger')
        return render_template('index.html'), 422


if __name__ == '__main__':
    app.run()
