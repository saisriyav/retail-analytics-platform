# Data Dictionary – Online Retail Transactions

## Dataset Overview
This dataset contains historical transactional data from an online retail business.
Each row represents a single line item within a customer invoice.

The data is used to analyze sales performance, customer behavior, product demand,
and revenue trends.

---

## Table: online_retail_transactions

| Column Name   | Data Type | Description |
|--------------|----------|-------------|
| Invoice      | String   | Unique identifier for each invoice. Multiple rows can share the same invoice number. |
| StockCode    | String   | Unique product (item) identifier. |
| Description  | String   | Text description of the product. |
| Quantity     | Integer  | Number of units purchased in the transaction. Negative values indicate returns. |
| InvoiceDate  | Datetime | Date and time when the invoice was generated. |
| Price        | Float    | Unit price of the product (excluding tax). |
| CustomerID   | Integer  | Unique identifier for a customer. Can be null for guest checkouts. |
| Country      | String   | Country where the customer is located. |

---

## Notes & Assumptions
- Each invoice can contain multiple products.
- Transactions with negative quantities represent product returns.
- Missing CustomerID values indicate non-registered or guest customers.
- Prices are assumed to be in the retailer’s base currency.
