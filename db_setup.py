import sqlite3 as sql

DB_NAME = 'izumi.db'

with sql.connect(DB_NAME) as con:
  cur = con.cursor()

  try:
    cur.execute("""
      CREATE TABLE pops (
        user_id INTEGER NOT NULL PRIMARY KEY,
        pop_num INTEGER NOT NULL DEFAULT 0
      );
    """)
  except sql.Error as e:
    print(str(e))

  try:
    cur.execute("""
      CREATE TABLE test (
        id INTEGER NOT NULL PRIMARY KEY,
        name VARCHAR(64)
      );
    """)
    cur.execute("INSERT INTO test VALUES (0, 'test1');")
    cur.execute("INSERT INTO test VALUES (1, 'test2');")
    cur.execute("INSERT INTO test VALUES (2, 'test3');")
  except sql.Error as e:
    print(str(e))
