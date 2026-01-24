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

DROP TABLE IF EXISTS top_products;

CREATE TABLE top_products AS
SELECT
    f.stock_code,

    COALESCE(
      MAX(
        CASE
          WHEN p.description IS NOT NULL
           AND LENGTH(TRIM(p.description)) >= 10
           AND LOWER(p.description) NOT LIKE '%wrong%'
           AND LOWER(p.description) NOT LIKE '%mark%'
           AND LOWER(p.description) NOT LIKE '%damag%'
           AND LOWER(p.description) NOT LIKE '%broken%'
           AND LOWER(p.description) NOT LIKE '%smashed%'
           AND LOWER(p.description) NOT LIKE '%rust%'
           AND LOWER(p.description) NOT LIKE '%adjust%'
           AND LOWER(p.description) NOT LIKE '%fix%'
           AND LOWER(p.description) NOT LIKE '%amend%'
           AND LOWER(p.description) NOT LIKE '%credit%'
           AND LOWER(p.description) NOT LIKE '%manual%'
           AND LOWER(p.description) NOT LIKE '%mail%'
           AND LOWER(p.description) NOT LIKE '%cargo%'
           AND LOWER(p.description) NOT LIKE '%order%'
           AND LOWER(p.description) NOT LIKE '%amazon%'
           AND LOWER(p.description) NOT LIKE '%dotcom%'
           AND LOWER(p.description) NOT LIKE '%crush%'
           AND LOWER(p.description) NOT LIKE '%stock%'
           AND LOWER(p.description) NOT LIKE '%return%'
           AND LOWER(p.description) NOT LIKE '%ctn%'
           AND LOWER(p.description) NOT IN ('nan', 'missing', 'short')
          THEN TRIM(p.description)
        END
      ),
      'Description unavailable'
    ) AS description,

    ROUND(SUM(f.quantity * f.unit_price), 2) AS net_revenue,
    SUM(f.quantity) AS units_sold
FROM fact_sales f
LEFT JOIN dim_product p
    ON f.stock_code = p.stock_code
WHERE f.quantity > 0
GROUP BY f.stock_code
ORDER BY SUM(f.quantity * f.unit_price) DESC
LIMIT 50;
