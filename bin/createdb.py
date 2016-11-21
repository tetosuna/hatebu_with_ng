import sqlite3

conn=sqlite3.connect('/data/ng.db')
c = conn.cursor()
try:
    c.execute('create table ng_titles(word text, user text)')
except:
    pass

try:
    c.execute('create table ng_domains(word text, user text)')
except:
    pass

conn.commit()
conn.close()
