import sqlite3

__connection = None

def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res
    return inner

@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS movies')
    c.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            user_name   TEXT NOT NULL,
            movie_id    INTEGER NOT NULL,
            movie_name  TEXT NOT NULL
        )
    ''')

    if force:
        c.execute('DROP TABLE IF EXISTS similars')
    c.execute('''
        CREATE TABLE IF NOT EXISTS similars (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            user_name   TEXT NOT NULL,
            movie_id    INTEGER NOT NULL,
            movie_name  TEXT NOT NULL
        )
    ''')

    conn.commit()

@ensure_connection
def add_information(conn, user_id: int, user_name: str, movie_id: int, movie_name: str):
    c = conn.cursor()
    c.execute('INSERT INTO movies (user_id, user_name, movie_id, movie_name) VALUES (?, ?, ?, ?)', (user_id, user_name, movie_id, movie_name))
    conn.commit()

@ensure_connection
def add_similar(conn, user_id: int, user_name: str, movie_id: int, movie_name: str):
    c = conn.cursor()
    c.execute('INSERT INTO similars (user_id, user_name, movie_id, movie_name) VALUES (?, ?, ?, ?)', (user_id, user_name, movie_id, movie_name))
    conn.commit()
