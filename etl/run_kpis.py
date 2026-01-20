import sqlite3

con = sqlite3.connect("data/sqlite/retail.db")
cur = con.cursor()

with open("sql/03_kpis.sql", "r") as f:
    sql = f.read()

queries = [q.strip() for q in sql.split(";") if q.strip()]

for i, q in enumerate(queries, start=1):
    print(f"\n--- KPI {i} ---")
    cur.execute(q)
    for row in cur.fetchall():
        print(row)

con.close()
