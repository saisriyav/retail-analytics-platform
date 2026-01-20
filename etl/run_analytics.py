import sqlite3

con = sqlite3.connect("data/sqlite/retail.db")
cur = con.cursor()

with open("sql/04_analytics_views.sql", "r") as f:
    sql = f.read()

queries = [q.strip() for q in sql.split(";") if q.strip()]

for q in queries:
    cur.execute(q)

con.commit()
con.close()

print("Analytics tables created successfully.")
