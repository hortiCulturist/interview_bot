import sqlite3 as sqlt

db_name = 'interview.db'

def start_db():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS "data" ('
                 '"id"	INTEGER UNIQUE,'
                 '"first_name"	BLOB,'
                 '"username"	BLOB,'
                 '"points" INTEGER);')
    base.commit()

def db_add(id, first_name, username):
    base = sqlt.connect(db_name)
    cur = base.cursor()

    cur.execute('INSERT INTO data VALUES (?, ?, ?, null)', (id, first_name, username,))
    base.commit()
    base.close()

def update_point(id, pint):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('UPDATE data SET points = ? WHERE id = ?', (pint, id))
    base.commit()
    base.close()

def all_user():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    users = cur.execute('SELECT id from data').fetchall()
    base.close()
    return users