-- ==============================================================================
-- PROJECT 1: SALES PERFORMANCE DASHBOARD - DATABASE SCHEMA
-- Arrowstack Technologies Data Analytics Internship (Batch 2026)
-- Candidate: Sujal Pandya | Roll ID: AS-2026-92197
-- Database Dialect: SQLite / ANSI SQL-compliant
-- ==============================================================================

-- 1. DIMENSION: Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_segment VARCHAR(64) NOT NULL,
    region VARCHAR(64) NOT NULL,
    country VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. DIMENSION: Products
CREATE TABLE IF NOT EXISTS dim_products (
    product_key INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(128) NOT NULL UNIQUE,
    product_category VARCHAR(64) NOT NULL
);

-- 3. FACT: Sales Transactions
CREATE TABLE IF NOT EXISTS fact_sales (
    order_id VARCHAR(64) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(32) NOT NULL,
    customer_segment VARCHAR(64) NOT NULL,
    region VARCHAR(64) NOT NULL,
    country VARCHAR(64) NOT NULL,
    product_category VARCHAR(64) NOT NULL,
    product_name VARCHAR(128) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    discount_rate NUMERIC(5, 4) NOT NULL CHECK (discount_rate >= 0.0 AND discount_rate <= 1.0),
    gross_revenue NUMERIC(14, 2) NOT NULL CHECK (gross_revenue >= 0),
    net_revenue NUMERIC(14, 2) NOT NULL CHECK (net_revenue >= 0),
    sales_channel VARCHAR(64) NOT NULL,
    order_status VARCHAR(32) NOT NULL CHECK (order_status IN ('Completed', 'Cancelled', 'Refunded')),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

-- 4. FACT: Daily Digital Traffic and Conversion Funnel
CREATE TABLE IF NOT EXISTS fact_daily_traffic (
    traffic_date DATE PRIMARY KEY,
    website_sessions INTEGER NOT NULL CHECK (website_sessions >= 0),
    product_views INTEGER NOT NULL CHECK (product_views >= 0),
    cart_additions INTEGER NOT NULL CHECK (cart_additions >= 0),
    orders_placed INTEGER NOT NULL CHECK (orders_placed >= 0),
    conversion_rate_pct NUMERIC(6, 2) NOT NULL CHECK (conversion_rate_pct >= 0.0 AND conversion_rate_pct <= 100.0)
);

-- Indexing Strategy for analytical query acceleration
CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON fact_sales(order_date);
CREATE INDEX IF NOT EXISTS idx_fact_sales_region ON fact_sales(region);
CREATE INDEX IF NOT EXISTS idx_fact_sales_category ON fact_sales(product_category);
CREATE INDEX IF NOT EXISTS idx_fact_sales_status ON fact_sales(order_status);

-- Analytical View: Monthly Sales Summary
CREATE VIEW IF NOT EXISTS v_monthly_sales_summary AS
SELECT 
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(CASE WHEN order_status = 'Completed' THEN 1 ELSE 0 END) AS completed_orders,
    SUM(CASE WHEN order_status = 'Completed' THEN gross_revenue ELSE 0 END) AS gross_revenue,
    SUM(CASE WHEN order_status = 'Completed' THEN net_revenue ELSE 0 END) AS net_revenue,
    ROUND(SUM(CASE WHEN order_status = 'Completed' THEN net_revenue ELSE 0 END) * 1.0 / 
          NULLIF(SUM(CASE WHEN order_status = 'Completed' THEN 1 ELSE 0 END), 0), 2) AS average_order_value
FROM fact_sales
GROUP BY strftime('%Y-%m', order_date);
