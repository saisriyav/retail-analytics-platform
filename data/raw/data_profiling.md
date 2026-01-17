# Data Profiling – Online Retail Transactions

## Dataset Scope
- Time Period: 2009–2010
- Data Granularity: Invoice line items (one row per product per invoice)
- Source: Online retail transactional system

---

## Structural Observations
- Multiple rows can share the same Invoice number
- Each row represents a single product within an order
- Dataset includes both sales and potential return transactions

---

## Column-Level Profiling

### Invoice
- Repeating values observed
- Represents a single customer order

### StockCode
- Alphanumeric product identifiers
- Unique per product

### Description
- Free-text product names
- Numeric characters appear as part of product descriptions (e.g., size, quantity)
- Not suitable for numerical aggregation

### Quantity
- Integer values
- Positive values indicate product sales
- Dataset may include negative values representing returns

### InvoiceDate
- Timestamp includes both date and time
- Enables time-based trend analysis

### Price
- Decimal values
- Represents unit price per product

### CustomerID
- Numeric identifier
- Some records may contain missing values
- Missing values likely represent guest or anonymous customers

### Country
- Text-based geographic field
- Majority of records appear to originate from the United Kingdom

---

## Data Quality Considerations
- Duplicate Invoice numbers are expected due to line-item structure
- Revenue calculations must account for returned items
- Null CustomerID values should be handled explicitly in analytics
