-- ==============================================================================
-- PROJECT 1: SALES PERFORMANCE DASHBOARD - DATA QUALITY & INTEGRITY CHECKS
-- Arrowstack Technologies Data Analytics Internship (Batch 2026)
-- Candidate: Sujal Pandya | Roll ID: AS-2026-92197
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- CHECK 1: Primary Key Uniqueness on fact_sales
-- Expected: 0 duplicate order_id records
-- ------------------------------------------------------------------------------
SELECT 
    'Check 1: fact_sales PK Uniqueness' AS check_name,
    COUNT(*) AS failure_count
FROM (
    SELECT order_id 
    FROM fact_sales 
    GROUP BY order_id 
    HAVING COUNT(*) > 1
);

-- ------------------------------------------------------------------------------
-- CHECK 2: Null Checks on Mandatory Business Columns
-- Expected: 0 records with missing values
-- ------------------------------------------------------------------------------
SELECT 
    'Check 2: Null Checks on fact_sales' AS check_name,
    COUNT(*) AS failure_count
FROM fact_sales
WHERE order_id IS NULL
   OR order_date IS NULL
   OR customer_id IS NULL
   OR region IS NULL
   OR product_name IS NULL
   OR net_revenue IS NULL;

-- ------------------------------------------------------------------------------
-- CHECK 3: Financial Integrity & Domain Rule Validation
-- Tests: quantity > 0, unit_price >= 0, discount_rate between 0 and 1,
-- and net_revenue <= gross_revenue
-- Expected: 0 violating records
-- ------------------------------------------------------------------------------
SELECT 
    'Check 3: Financial Rule Validation' AS check_name,
    COUNT(*) AS failure_count
FROM fact_sales
WHERE quantity <= 0
   OR unit_price < 0
   OR discount_rate < 0.0 OR discount_rate > 1.0
   OR net_revenue < 0
   OR net_revenue > (gross_revenue + 0.05); -- allowance for penny rounding

-- ------------------------------------------------------------------------------
-- CHECK 4: Referential Integrity Check
-- Verifies that all customer_id values in fact_sales exist in dim_customers
-- Expected: 0 orphan records
-- ------------------------------------------------------------------------------
SELECT 
    'Check 4: Orphan Customer ID Foreign Key Check' AS check_name,
    COUNT(*) AS failure_count
FROM fact_sales f
LEFT JOIN dim_customers c ON f.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- ------------------------------------------------------------------------------
-- CHECK 5: Traffic Funnel Boundary Checks
-- Verifies that orders_placed <= cart_additions <= product_views <= website_sessions
-- Expected: 0 violating days
-- ------------------------------------------------------------------------------
SELECT 
    'Check 5: Funnel Hierarchy Logical Consistency' AS check_name,
    COUNT(*) AS failure_count
FROM fact_daily_traffic
WHERE product_views > website_sessions
   OR cart_additions > product_views
   OR orders_placed > cart_additions;

-- ------------------------------------------------------------------------------
-- CHECK 6: Date Range Validity
-- Ensures orders are within the valid project horizon (2025 to 2026)
-- Expected: 0 out-of-bounds records
-- ------------------------------------------------------------------------------
SELECT 
    'Check 6: Chronological Bounds Check' AS check_name,
    COUNT(*) AS failure_count
FROM fact_sales
WHERE order_date < '2025-01-01' OR order_date > '2026-12-31';
