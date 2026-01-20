-- Monthly Revenue
DROP TABLE IF EXISTS monthly_revenue;
CREATE TABLE monthly_revenue AS
SELECT
  substr(invoice_datetime, 1, 7) AS year_month,
  ROUND(SUM(line_revenue), 2) AS net_revenue,
  COUNT(DISTINCT invoice_no) AS orders
FROM fact_sales
WHERE is_cancelled = 0
GROUP BY year_month
ORDER BY year_month;

-- Revenue by Country
DROP TABLE IF EXISTS country_revenue;
CREATE TABLE country_revenue AS
SELECT
  country,
  ROUND(SUM(line_revenue), 2) AS net_revenue,
  COUNT(DISTINCT invoice_no) AS orders
FROM fact_sales
WHERE is_cancelled = 0
GROUP BY country
ORDER BY net_revenue DESC;

-- Top Products by Revenue
DROP TABLE IF EXISTS top_products;
CREATE TABLE top_products AS
SELECT
  f.stock_code,
  d.description,
  ROUND(SUM(f.line_revenue), 2) AS net_revenue,
  SUM(f.quantity) AS units_sold
FROM fact_sales f
JOIN dim_product d
  ON f.stock_code = d.stock_code
WHERE f.is_cancelled = 0
GROUP BY f.stock_code, d.description
ORDER BY net_revenue DESC
LIMIT 50;
