import sqlite3

con = sqlite3.connect("data/sqlite/retail.db")
cur = con.cursor()

print("\nTop 10 countries by net revenue:\n")

cur.execute("""
SELECT country,
       ROUND(SUM(line_revenue), 2) AS revenue
FROM fact_sales
WHERE is_cancelled = 0
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;
""")

for row in cur.fetchall():
    print(row)

cur.execute("""
SELECT COUNT(*) FROM fact_sales WHERE is_cancelled = 1;
""")

print("\nCancelled / return rows:", cur.fetchone()[0])

con.close()
