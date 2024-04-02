import psycopg2
from psycopg2.extras import DictCursor, NamedTupleCursor
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn(database_url):
    connection = psycopg2.connect(database_url)
    return connection


def add_url_into_db(url):
    with get_conn(DATABASE_URL).cursor(cursor_factory=NamedTupleCursor) as curs:
        query = (
            'INSERT INTO urls '
            '(name, created_at) '
            'VALUES (%s, %s) '
            'RETURNING id'
        )
        values = (url, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        curs.execute(query, values)
        return curs.fetchone().id


def get_url_by_name(url):
    with get_conn(DATABASE_URL).cursor(cursor_factory=DictCursor) as curs:
        query = 'SELECT * FROM urls WHERE name = (%s)'
        curs.execute(query, (url,))
        return curs.fetchone()


def get_url_by_id(id):
    with get_conn(DATABASE_URL).cursor(cursor_factory=DictCursor) as curs:
        query = 'SELECT * FROM urls WHERE id = (%s)'
        curs.execute(query, (id,))
        return curs.fetchone()


def get_urls_list():
    with get_conn(DATABASE_URL).cursor(cursor_factory=DictCursor) as curs:
        query = 'SELECT * FROM urls'
        curs.execute(query, (id, ))
        data = curs.fetchall()
        return data
