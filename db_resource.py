from pprint import pprint

from psycopg2 import connect as _2connect
from psycopg2.extras import RealDictCursor, register_hstore

from settings import dbconn


def connect():
    conn = _2connect(**dbconn)
    register_hstore(conn)
    conn.cursor_factory = RealDictCursor
    return conn


def select_from(query, *args):
    with connect() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query, *args)
            params = cursor.fetchall()
            return len(params) == 1 and params[0] or params


def execute_sql(query, *args):
    with connect() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query, *args)


def get_trans_data(tran_id):
    data = select_from("""SELECT ps_tran_id, amount, actual_amount, currency, card_bin, 
                                 card_last_digits, terminal_id, timestart, timeend
                          FROM transactions WHERE id = %s""", [tran_id])
    return data


if __name__ == '__main__':
    tran = 9001539162

    x = get_trans_data(tran)
    pprint(x)
