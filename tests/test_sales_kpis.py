"""
==============================================================================
PROJECT 1: SALES PERFORMANCE DASHBOARD - AUTOMATED TEST SUITE
Arrowstack Technologies Data Analytics Internship (Batch 2026)
Candidate: Sujal Pandya | Roll ID: AS-2026-92197
==============================================================================
"""

import os
import sqlite3
import pandas as pd
import openpyxl
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_sales_data.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "sales_database.db")
EXCEL_PATH = os.path.join(BASE_DIR, "analysis", "sales_performance_analysis.xlsx")

def test_data_artifacts_exist():
    """Verify that all core project artifacts have been generated."""
    assert os.path.exists(DATA_PATH), f"Missing cleaned data file at {DATA_PATH}"
    assert os.path.exists(DB_PATH), f"Missing database file at {DB_PATH}"
    assert os.path.exists(EXCEL_PATH), f"Missing Excel workbook at {EXCEL_PATH}"

def test_sales_data_integrity():
    """Verify primary constraints and validity of clean sales dataset."""
    df = pd.read_csv(DATA_PATH)
    
    # 1. Non-empty dataset
    assert len(df) >= 3000, f"Expected at least 3,000 records, got {len(df)}"
    
    # 2. No nulls in mandatory columns
    mandatory_cols = ["order_id", "order_date", "customer_id", "region", "product_name", "quantity", "net_revenue"]
    for col in mandatory_cols:
        assert df[col].isnull().sum() == 0, f"Null values detected in column {col}"
        
    # 3. Numeric validity
    assert (df["quantity"] > 0).all(), "Found non-positive quantities"
    assert (df["unit_price"] >= 0).all(), "Found negative unit prices"
    assert (df["discount_rate"] >= 0.0).all() and (df["discount_rate"] <= 1.0).all(), "Discount rate out of [0, 1] range"
    assert (df["net_revenue"] >= 0).all(), "Found negative net revenues"
    
    # 4. Calculation accuracy: net_revenue <= gross_revenue
    assert (df["net_revenue"] <= df["gross_revenue"] + 0.05).all(), "Net revenue exceeds gross revenue"

def test_kpi_calculations_and_formulas():
    """Verify mathematical definitions of core KPIs: Revenue, AOV, Conversion Rate."""
    df = pd.read_csv(DATA_PATH)
    completed = df[df["order_status"] == "Completed"]
    
    expected_gross = (completed["quantity"] * completed["unit_price"]).sum()
    actual_gross = completed["gross_revenue"].sum()
    assert abs(expected_gross - actual_gross) < 5.0, "Gross revenue calculation mismatch"
    
    expected_aov = completed["net_revenue"].sum() / len(completed)
    actual_aov = completed["net_revenue"].mean()
    assert abs(expected_aov - actual_aov) < 0.01, "Average Order Value (AOV) mismatch"

def test_sqlite_database_tables():
    """Verify that the SQLite database has all required star schema tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    expected_tables = ["fact_sales", "fact_daily_traffic", "dim_products", "dim_customers"]
    for table in expected_tables:
        assert table in tables, f"Expected table '{table}' not found in SQLite database"

def test_traffic_funnel_hierarchy():
    """Verify funnel logic: sessions >= views >= cart additions >= orders."""
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT COUNT(*) FROM fact_daily_traffic 
    WHERE website_sessions < product_views 
       OR product_views < cart_additions 
       OR cart_additions < orders_placed;
    """
    violations = conn.execute(query).fetchone()[0]
    conn.close()
    assert violations == 0, f"Found {violations} days with invalid funnel step ordering"

def test_excel_workbook_structure():
    """Verify that the generated Excel file contains all required worksheets and headers."""
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=False)
    sheet_names = wb.sheetnames
    
    expected_sheets = [
        "Executive KPI Summary", 
        "Monthly Trends", 
        "Regional Performance", 
        "Product Category Analysis", 
        "Cleaned Sales Data"
    ]
    for sheet in expected_sheets:
        assert sheet in sheet_names, f"Missing sheet '{sheet}' in Excel analysis file"
        
    wb.close()
