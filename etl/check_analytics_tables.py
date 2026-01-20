import sqlite3

con = sqlite3.connect("data/sqlite/retail.db")
cur = con.cursor()

tables = ["monthly_revenue", "country_revenue", "top_products"]

for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(t, "rows =", cur.fetchone()[0])

print("\nSample monthly_revenue (first 5 rows):")
cur.execute("SELECT * FROM monthly_revenue ORDER BY year_month LIMIT 5;")
for row in cur.fetchall():
    print(row)

con.close()
