import sqlite3 as sql
from constants.py import DB_NAME

con = sql.connect(DB_NAME)

with con:
  con.execute("""
    CREATE TABLE pops (
      user_id INTEGER NOT NULL PRIMARY KEY,
      pop_num INTEGER NOT NULL DEFAULT 0
    );
  """)

con.close()
