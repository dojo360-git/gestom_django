import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Lister toutes les tables

# Avoir le nom des tables : 
#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")


# Avoir les noms des champs : 
cursor.execute("PRAGMA table_info(core_flux);")
print([col[1] for col in cursor.fetchall()])

