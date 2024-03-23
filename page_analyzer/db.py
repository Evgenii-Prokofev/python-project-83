import psycopg2
from psycopg2.extras import NamedTupleCursor
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


def add_url_into_db(url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
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
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        query = 'SELECT * FROM urls WHERE name = (%s)'
        curs.execute(query, (url,))
        data = curs.fetchone()
        return data


def get_url_by_id(id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        query = 'SELECT * FROM urls WHERE id = (%s)'
        curs.execute(query, (id,))
        data = curs.fetchone()
        return data
