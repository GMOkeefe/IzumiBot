import sqlite3 as sql
from constants.py import DB_NAME

class Table:
  def __init__(self, name):
    self.name = name
  
  def where(self, field, value, comparator='='):
    return Query(self.name, field, value, comparator)

  def select(self, col_name):
    return Result(self.name, col_name)

class Query:
  def __init__(self, table_name, field, value, comparator, parent=None):
    self.table_name = table_name
    self.conds = [(field, value, comparator)] + parent.conds
  
  def where(self, field, value, comparator='='):
    return Query(self.table_name, field, value, comparator, parent=self)
  
  def select(self, col_name):
    return Result(self.table_name, col_name, conds=self.conds)

class Result:
  def __init__(self, table_name, col_name, conds=None):
    self.table_name = table_name
    self.col_name = col_name
    self.conds = conds
  
  def execute(self):
    with sql.connect(DB_NAME) as con:
      with con.cursor() as cur:
        cur.execute(self.gen_statement())
  
  def gen_statement(self):
    statement = "SELECT " + self.col_name + " FROM " + self.table_name

    if (self.conds != None):
      statement += " WHERE " + self.conds[0][0] + " " + \
        self.conds[0][2] + " " + self.conds[0][1]
      for cond in self.conds[1:]:
        statement += " AND " + cond[0] + " " + cond[2] + " " + \
          cond[1]
      
    return statement + ";"

def read(table_name):
  with sql.connect(DB_NAME) as con:
    cmd = """
      SELECT name
        FROM sqlite_master
        WHERE type='table'
          AND name='
    """ + table_name + "';"

    con.execute(cmd)