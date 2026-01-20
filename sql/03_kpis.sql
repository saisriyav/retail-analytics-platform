-- KPI 1: Net Revenue
SELECT ROUND(SUM(line_revenue), 2) AS net_revenue
FROM fact_sales
WHERE is_cancelled = 0;

-- KPI 2: Total Orders
SELECT COUNT(DISTINCT invoice_no) AS total_orders
FROM fact_sales
WHERE is_cancelled = 0;

-- KPI 3: Total Customers
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM fact_sales
WHERE is_cancelled = 0
  AND customer_id IS NOT NULL;

-- KPI 4: Average Order Value (AOV)
WITH order_revenue AS (
  SELECT invoice_no, SUM(line_revenue) AS revenue
  FROM fact_sales
  WHERE is_cancelled = 0
  GROUP BY invoice_no
)
SELECT ROUND(AVG(revenue), 2) AS avg_order_value
FROM order_revenue;

-- KPI 5: Monthly Net Revenue Trend
SELECT
  substr(invoice_datetime, 1, 7) AS year_month,
  ROUND(SUM(line_revenue), 2) AS net_revenue
FROM fact_sales
WHERE is_cancelled = 0
GROUP BY year_month
ORDER BY year_month;
