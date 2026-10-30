# Project 1: Data Dictionary & KPI Mathematical Definitions
**Candidate**: Sujal Pandya | Roll ID: AS-2026-92197  
**Arrowstack Technologies Virtual Internship (Batch 2026)**  

---

## 1. Data Dictionary

### Table: `fact_sales`
| Column Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR(64) | PRIMARY KEY | Unique identifier for the customer purchase transaction |
| `order_date` | DATE | NOT NULL | Date when order was initiated (YYYY-MM-DD) |
| `customer_id` | VARCHAR(32) | NOT NULL, FK | Reference identifier to customer master record |
| `customer_segment`| VARCHAR(64) | NOT NULL | Tier: Enterprise, Mid-Market, SMB, Government & Edu |
| `region` | VARCHAR(64) | NOT NULL | Geographical sales theater (North America, Europe, APAC, etc.) |
| `country` | VARCHAR(64) | NOT NULL | Country of billing entity |
| `product_category`| VARCHAR(64) | NOT NULL | Category: Cloud Infrastructure, Software Licenses, Hardware, Services |
| `product_name` | VARCHAR(128)| NOT NULL | Specific SKU / product offering |
| `quantity` | INTEGER | CHECK (> 0) | Number of units purchased in the transaction |
| `unit_price` | NUMERIC(12,2)| CHECK (>= 0) | Base catalog price per unit in USD |
| `discount_rate` | NUMERIC(5,4)| CHECK (0..1) | Contractual discount percentage applied (e.g. 0.15 = 15%) |
| `gross_revenue` | NUMERIC(14,2)| CHECK (>= 0) | Total list price revenue: $Gross = Quantity \times UnitPrice$ |
| `net_revenue` | NUMERIC(14,2)| CHECK (>= 0) | Realized revenue: $Net = Gross \times (1 - DiscountRate)$ |
| `sales_channel` | VARCHAR(64) | NOT NULL | Channel: Direct Sales, Partner Reseller, Digital Portal, Inbound |
| `order_status` | VARCHAR(32) | CHECK IN | Status: 'Completed', 'Cancelled', 'Refunded' |

### Table: `fact_daily_traffic`
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `traffic_date` | DATE (PK) | Observation date |
| `website_sessions`| INTEGER | Total digital visitor sessions recorded |
| `product_views` | INTEGER | Total product detail page visits |
| `cart_additions` | INTEGER | Number of sessions where products were added to cart |
| `orders_placed` | INTEGER | Number of checkout conversions executed |
| `conversion_rate_pct`| NUMERIC(6,2)| Conversion efficiency: $(Orders / Sessions) \times 100$ |

---

## 2. KPI Formulas & Definitions

### 1. Total Net Revenue
$$\text{Total Net Revenue} = \sum_{i \in \text{Completed Orders}} \text{net\_revenue}_i$$

### 2. Average Order Value (AOV)
$$\text{AOV} = \frac{\sum_{i \in \text{Completed}} \text{net\_revenue}_i}{N_{\text{Completed Orders}}}$$

### 3. Month-over-Month (MoM) Growth Rate
$$\text{MoM Growth \%}_t = \left(\frac{\text{Net Revenue}_t - \text{Net Revenue}_{t-1}}{\text{Net Revenue}_{t-1}}\right) \times 100$$

### 4. Overall Conversion Rate
$$\text{Conversion Rate \%} = \left(\frac{\sum \text{Orders Placed}}{\sum \text{Website Sessions}}\right) \times 100$$

### 5. Regional Revenue Share
$$\text{Revenue Share \%}_{\text{Region}} = \left(\frac{\sum_{\text{Region}} \text{Net Revenue}}{\sum_{\text{All Regions}} \text{Net Revenue}}\right) \times 100$$
