import psycopg2
from psycopg2.extras import DictCursor, NamedTupleCursor
import os
import datetime


def get_conn():
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")
        connection = psycopg2.connect(DATABASE_URL)
        return connection
    except Exception:
        print("Can't connect to database")


def add_url_into_db(url):
    with get_conn() as conn, conn.cursor() as curs:
        date = datetime.date.today()
        curs.execute(
            """INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id""",
            (url, date)
        )
        conn.commit()
        id = curs.fetchone()
    return id[0]


def get_url_by_name(url):
    with get_conn().cursor(cursor_factory=NamedTupleCursor) as curs:
        query = 'SELECT * FROM urls WHERE name = (%s)'
        curs.execute(query, (url,))
        data = curs.fetchone()
        return data


def get_url_by_id(id):
    with get_conn().cursor(cursor_factory=NamedTupleCursor) as curs:
        query = 'SELECT * FROM urls WHERE id = (%s)'
        curs.execute(query, (id,))
        url = curs.fetchone()
        return url


def get_urls_list():
    with get_conn().cursor(cursor_factory=DictCursor) as curs:
        query = (
            'SELECT '
            'urls.id AS id, '
            'urls.name AS name, '
            'url_checks.created_at AS last_check, '
            'status_code '
            'FROM urls '
            'LEFT JOIN url_checks '
            'ON urls.id = url_checks.url_id '
            'AND url_checks.id = ('
            'SELECT max(id) FROM url_checks WHERE urls.id = url_checks.url_id) '
            'ORDER BY urls.id DESC;'
        )
        curs.execute(query)
        urls = curs.fetchall()
        return urls


def get_check_by_url_id(id):
    with get_conn().cursor(cursor_factory=NamedTupleCursor) as curs:
        query = 'SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC'
        curs.execute(query, (id,))
        checks = curs.fetchall()
        return checks


def add_url_check_into_db(check_info):
    with get_conn() as connection, connection.cursor() as curs:
        query = (
            'INSERT INTO url_checks '
            '(url_id, status_code, h1, title, description, created_at) '
            'VALUES (%s, %s, %s, %s, %s, %s)'
        )
        values = (
            check_info.get('url_id'),
            check_info.get('status_code'),
            check_info.get('h1', ''),
            check_info.get('title', ''),
            check_info.get('description', ''),
            datetime.date.today()
        )
        curs.execute(query, values)
