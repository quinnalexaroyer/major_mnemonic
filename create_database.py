import sqlite3

conn = sqlite3.connect("mnemonic.db")
c = conn.cursor()
c.execute("CREATE TABLE mnemonic (id INTEGER PRIMARY KEY AUTOINCREMENT, word VARCHAR, number INTEGER, zero INTEGER, category INTEGER, exception VARCHAR)")
c.execute("CREATE INDEX word ON mnemonic (word)")
c.execute("CREATE INDEX number ON mnemonic (number)")
c.execute("CREATE INDEX category ON mnemonic (category)")
conn.commit()
