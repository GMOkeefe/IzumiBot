import sqlite3 as sql

DB_NAME = 'izumi.db'

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
    self.conds = [(field, value, comparator)]
    if (parent != None):
      self.conds += parent.conds
  
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
      cur = con.cursor()
      return cur.execute(self.gen_statement_for_execute(), self.gen_tuple_for_execute())
  
  def gen_statement_for_execute(self):
    statement = "SELECT " + self.col_name + " FROM " + self.table_name

    if self.conds != None:
      statement += " WHERE " + self.conds[0][0] + " " + self.conds[0][2] + " ?"
      for cond in self.conds[1:]:
        statement += " AND " + self.conds[0] + " " + cond[2] + " ?"
    
    return statement + ";"

  def gen_tuple_for_execute(self):
    lst = []
    if self.conds != None:
      for cond in self.conds:
        lst += [cond[1]]
    
    return tuple(lst)

  def gen_statement(self):
    statement = "SELECT " + self.col_name + " FROM " + self.table_name

    if self.conds != None:
      statement += " WHERE " + self.conds[0][0] + " " + \
        self.conds[0][2] + " " + str(self.conds[0][1])
      for cond in self.conds[1:]:
        statement += " AND " + cond[0] + " " + cond[2] + " " + \
          str(cond[1])
      
    return statement + ";"

def read(table_name):
  with sql.connect(DB_NAME) as con:
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", \
      (table_name,))

    if (len(cur.fetchall()) == 0):
      raise sql.ProgrammingError("No such table exists")
    
    return Table(table_name)

def insert(table_name, **values):
  vallist = []
  statement = "INSERT INTO " + table_name + " ("
  for key, value in values.items():
    statement += key
    vallist += [value]
  statement += ") VALUES (?"
  for value in vallist[1:]:
    statement += ", ?"
  statement += ");"

  with sql.connect(DB_NAME) as con:
    cur = con.cursor()

    cur.execute(statement, vallist)