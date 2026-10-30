-- ==============================================================================
-- PROJECT 1: SALES PERFORMANCE DASHBOARD - CORE KPI ANALYTICAL QUERIES
-- Arrowstack Technologies Data Analytics Internship (Batch 2026)
-- Candidate: Sujal Pandya | Roll ID: AS-2026-92197
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. EXECUTIVE KPI SUMMARY
-- Calculates Total Net Revenue, Completed Orders, Total Units Sold, 
-- Average Order Value (AOV), and Overall Conversion Rate
-- ------------------------------------------------------------------------------
WITH sales_kpis AS (
    SELECT 
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(CASE WHEN order_status = 'Completed' THEN 1 ELSE 0 END) AS completed_orders,
        SUM(CASE WHEN order_status = 'Completed' THEN net_revenue ELSE 0 END) AS total_net_revenue,
        SUM(CASE WHEN order_status = 'Completed' THEN gross_revenue ELSE 0 END) AS total_gross_revenue,
        SUM(CASE WHEN order_status = 'Completed' THEN quantity ELSE 0 END) AS total_units_sold,
        ROUND(
            SUM(CASE WHEN order_status = 'Completed' THEN net_revenue ELSE 0 END) * 1.0 / 
            NULLIF(SUM(CASE WHEN order_status = 'Completed' THEN 1 ELSE 0 END), 0), 
            2
        ) AS average_order_value_aov
    FROM fact_sales
),
traffic_kpis AS (
    SELECT 
        SUM(website_sessions) AS total_sessions,
        SUM(orders_placed) AS total_funnel_orders,
        ROUND(
            (SUM(orders_placed) * 100.0) / NULLIF(SUM(website_sessions), 0), 
            2
        ) AS overall_conversion_rate_pct
    FROM fact_daily_traffic
)
SELECT 
    s.total_orders,
    s.completed_orders,
    ROUND(s.total_net_revenue, 2) AS net_revenue_usd,
    ROUND(s.total_gross_revenue, 2) AS gross_revenue_usd,
    s.total_units_sold,
    s.average_order_value_aov AS aov_usd,
    t.total_sessions,
    t.overall_conversion_rate_pct
FROM sales_kpis s
CROSS JOIN traffic_kpis t;


-- ------------------------------------------------------------------------------
-- 2. MONTHLY REVENUE TREND & MOM GROWTH RATE
-- Evaluates monthly revenue progression and Month-over-Month (MoM) growth %
-- ------------------------------------------------------------------------------
WITH monthly_data AS (
    SELECT 
        strftime('%Y-%m', order_date) AS sales_month,
        COUNT(DISTINCT order_id) AS order_count,
        ROUND(SUM(net_revenue), 2) AS monthly_net_revenue,
        ROUND(AVG(net_revenue), 2) AS monthly_aov
    FROM fact_sales
    WHERE order_status = 'Completed'
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    sales_month,
    order_count,
    monthly_net_revenue,
    monthly_aov,
    LAG(monthly_net_revenue, 1) OVER (ORDER BY sales_month) AS prev_month_net_revenue,
    ROUND(
        ((monthly_net_revenue - LAG(monthly_net_revenue, 1) OVER (ORDER BY sales_month)) * 100.0) /
        NULLIF(LAG(monthly_net_revenue, 1) OVER (ORDER BY sales_month), 0),
        2
    ) AS mom_growth_pct
FROM monthly_data
ORDER BY sales_month ASC;


-- ------------------------------------------------------------------------------
-- 3. REGION-WISE PERFORMANCE & REVENUE SHARE
-- Aggregates orders, revenue, and contribution percentage by geographical territory
-- ------------------------------------------------------------------------------
WITH total_rev AS (
    SELECT SUM(net_revenue) AS grand_total_revenue 
    FROM fact_sales 
    WHERE order_status = 'Completed'
)
SELECT 
    s.region,
    COUNT(DISTINCT s.order_id) AS completed_orders,
    SUM(s.quantity) AS total_units,
    ROUND(SUM(s.net_revenue), 2) AS region_net_revenue,
    ROUND(AVG(s.net_revenue), 2) AS region_aov,
    ROUND((SUM(s.net_revenue) * 100.0) / t.grand_total_revenue, 2) AS revenue_share_pct
FROM fact_sales s
CROSS JOIN total_rev t
WHERE s.order_status = 'Completed'
GROUP BY s.region, t.grand_total_revenue
ORDER BY region_net_revenue DESC;


-- ------------------------------------------------------------------------------
-- 4. PRODUCT CATEGORY & PRODUCT-LEVEL DRILL-DOWN
-- Performance breakdown by category and specific SKU with profit/revenue yield
-- ------------------------------------------------------------------------------
SELECT 
    product_category,
    product_name,
    COUNT(DISTINCT order_id) AS orders_count,
    SUM(quantity) AS units_sold,
    ROUND(AVG(unit_price), 2) AS avg_selling_price,
    ROUND(AVG(discount_rate * 100.0), 2) AS avg_discount_pct,
    ROUND(SUM(gross_revenue), 2) AS gross_revenue,
    ROUND(SUM(net_revenue), 2) AS net_revenue,
    ROUND(SUM(net_revenue) * 1.0 / NULLIF(SUM(quantity), 0), 2) AS revenue_per_unit
FROM fact_sales
WHERE order_status = 'Completed'
GROUP BY product_category, product_name
ORDER BY product_category, net_revenue DESC;


-- ------------------------------------------------------------------------------
-- 5. CUSTOMER SEGMENT & SALES CHANNEL MATRIX
-- Cross-tabulation of B2B segments against acquisition channels
-- ------------------------------------------------------------------------------
SELECT 
    customer_segment,
    sales_channel,
    COUNT(DISTINCT order_id) AS orders_count,
    ROUND(SUM(net_revenue), 2) AS segment_channel_revenue,
    ROUND(AVG(net_revenue), 2) AS aov
FROM fact_sales
WHERE order_status = 'Completed'
GROUP BY customer_segment, sales_channel
ORDER BY customer_segment, segment_channel_revenue DESC;


-- ------------------------------------------------------------------------------
-- 6. CONVERSION FUNNEL DROP-OFF ANALYSIS
-- Stage-by-stage drop-off from visitor session to order completion
-- ------------------------------------------------------------------------------
SELECT 
    SUM(website_sessions) AS total_sessions,
    SUM(product_views) AS total_product_views,
    ROUND((SUM(product_views) * 100.0) / NULLIF(SUM(website_sessions), 0), 2) AS session_to_view_pct,
    SUM(cart_additions) AS total_cart_additions,
    ROUND((SUM(cart_additions) * 100.0) / NULLIF(SUM(product_views), 0), 2) AS view_to_cart_pct,
    SUM(orders_placed) AS total_orders_placed,
    ROUND((SUM(orders_placed) * 100.0) / NULLIF(SUM(cart_additions), 0), 2) AS cart_to_order_pct,
    ROUND((SUM(orders_placed) * 100.0) / NULLIF(SUM(website_sessions), 0), 2) AS overall_conversion_pct
FROM fact_daily_traffic;
