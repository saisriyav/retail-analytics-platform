import sqlite3
import pandas as pd
from pathlib import Path

RAW_FILES = [
    Path("data/raw/online_retail_II_2009_2010.csv"),
    Path("data/raw/online_retail_II_2010_2011.csv"),
]
DB_PATH = Path("data/sqlite/retail.db")

def load_one(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path.resolve()}")

    # Your sample shows semicolon-delimited
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = [c.replace("\ufeff", "") for c in df.columns]
    # Normalize headers
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Unify column names across the two files (some versions use different labels)
    rename_map = {
        "invoice": "invoice_no",
        "invoiceno": "invoice_no",
        "stockcode": "stock_code",
        "description": "description",
        "quantity": "quantity",
        "invoicedate": "invoice_datetime",
        "unitprice": "unit_price",
        "price": "unit_price",
        "customer_id": "customer_id",
        "customerid": "customer_id",
        "country": "country",
    }
    df = df.rename(columns=rename_map)

    # Keep only required columns (ignore any extras)
    required = ["invoice_no", "stock_code", "description", "quantity",
                "invoice_datetime", "unit_price", "customer_id", "country"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{path.name} is missing columns: {missing}")

    df = df[required].copy()

    # Clean numeric columns
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")

    # Parse datetime (your format: 1.12.2009 07:45)
    df["invoice_datetime"] = pd.to_datetime(df["invoice_datetime"], errors="coerce", dayfirst=True)

    # Drop unusable rows
    df = df.dropna(subset=["invoice_no", "stock_code", "invoice_datetime", "quantity", "unit_price", "country"])

    # Derived fields
    df["line_revenue"] = df["quantity"] * df["unit_price"]
    df["is_cancelled"] = ((df["quantity"] < 0) | (df["invoice_no"].astype(str).str.startswith("C"))).astype(int)

    # Standardize types for DB
    df["invoice_no"] = df["invoice_no"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str)
    df["description"] = df["description"].astype(str)
    df["country"] = df["country"].astype(str)

    return df

def main():
    frames = [load_one(p) for p in RAW_FILES]
    df = pd.concat(frames, ignore_index=True)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)

    # Staging table: full combined dataset
    df.to_sql("stg_retail", con, if_exists="replace", index=False)

    # Dimension: products
    dim_product = df[["stock_code", "description"]].dropna().drop_duplicates()
    dim_product.to_sql("dim_product", con, if_exists="replace", index=False)

    # Fact: sales lines
    fact_cols = ["invoice_no", "invoice_datetime", "stock_code", "quantity",
                 "unit_price", "customer_id", "country", "line_revenue", "is_cancelled"]
    fact_sales = df[fact_cols].copy()
    fact_sales.to_sql("fact_sales", con, if_exists="replace", index=False)

    # Quick verification
    cur = con.cursor()
    for t in ["stg_retail", "dim_product", "fact_sales"]:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"{t}: {cur.fetchone()[0]} rows")

    con.close()
    print(f"\nDone. Database created at: {DB_PATH.resolve()}")

if __name__ == "__main__":
    main()
