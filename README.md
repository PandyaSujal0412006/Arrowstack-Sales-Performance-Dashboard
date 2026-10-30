# 📊 Arrowstack Project 1: Sales Performance Dashboard

**Intern**: Sujal Pandya | **Roll ID**: AS-2026-92197 | **Offer Ref**: AST/INT/2026/OFFER/92197  
**Program**: Arrowstack Technologies Virtual Internship • Data Analytics Track (Batch 2026)  
**Academic Institution**: CHARUSAT  

---

> ⚠️ **Synthetic Data Notice**: In compliance with the Arrowstack Internship Handbook guidelines, all data presented in this project is statistically synthesized for demonstration and analytical portfolio purposes. It does not represent actual or proprietary financial records of Arrowstack Technologies.

---

## 📌 Executive Overview
The **Sales Performance Dashboard** is an enterprise-grade analytics solution engineered to give executive stakeholders (CRO, VP of Sales, Regional Directors) transparent, real-time visibility into revenue trajectories, average deal values, discounting practices, geographic distribution, and digital acquisition funnel bottlenecks.

### Key Capabilities:
- **Core KPI Cards**: Total Net Revenue ($22.5M+), Completed Transactions, Average Order Value (AOV: ~$6,085), and End-to-End Funnel Conversion Rate (3.12%).
- **Interactive Multi-Dimensional Filtering**: Real-time drilldowns by Date Range, Geographical Region, Customer Segment, Product Category, and Acquisition Channel.
- **Dynamic Plotly Visualizations**: Dual-axis monthly revenue and order progression, MoM growth velocity indicators, regional contribution breakdowns, and interactive funnel drop-off stages.
- **Embedded SQL Query Engine & Data Quality Auditor**: Embedded SQLite Star Schema with live SQL query console and automated rule checks.
- **Multi-Tab Structured Excel Analysis**: Formatted workbook with native formulas (`SUMIFS`, `COUNTIFS`, `AVERAGE`), summary cards, and pivot breakdowns.
- **Automated Validation Suite**: Pytest test suite with 100% passing results verifying financial and logical consistency.

---

## 🗂️ Project Structure
```
01_Project_Sales_Performance_Dashboard/
├── app.py                     # Interactive Streamlit Web Application
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview and run guide
├── data/
│   ├── generate_data.py       # Reproducible synthetic data generation script
│   ├── raw_sales_data.csv     # Raw generated transaction dataset (3,800 rows)
│   ├── cleaned_sales_data.csv # Transformed and validated analytical dataset
│   └── sales_database.db      # SQLite Star Schema relational database
├── sql/
│   ├── 01_schema.sql          # DDL tables, indexes, constraints, and views
│   ├── 02_kpi_queries.sql     # Production analytical queries (Revenue, AOV, MoM)
│   └── 03_data_quality_checks.sql # Automated integrity and boundary validation checks
├── analysis/
│   ├── generate_excel.py      # Automated openpyxl workbook generator
│   └── sales_performance_analysis.xlsx # 5-tab formatted Excel analytical model
├── tests/
│   ├── test_sales_kpis.py     # Pytest automated test suite (6 passing tests)
│   └── validation_report.txt  # Dated test execution output and evidence log
└── docs/
    ├── requirements_and_scope.md    # Business requirements, stakeholders & scope
    ├── data_dictionary_and_kpi.md   # Field schemas and mathematical definitions
    ├── decision_log.md              # Technical trade-offs and rationale
    └── viva_interview_prep.md       # Handbook Section 16 interview Q&A
```

---

## 🚀 How to Run the Dashboard

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.
```bash
cd "01_Project_Sales_Performance_Dashboard"
python -m pip install -r requirements.txt
```

### 2. Run Data Generation (Optional - Pre-generated files are included)
```bash
python data/generate_data.py
python analysis/generate_excel.py
```

### 3. Run Automated Validation Tests
```bash
pytest tests/test_sales_kpis.py -v
```

### 4. Launch the Interactive Dashboard
```bash
streamlit run app.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 📈 Key Metrics & Analytical Findings
1. **Enterprise Leverage**: Enterprise accounts contribute over 58% of net revenue while accounting for only 40% of orders, driven by high AOV ($8,400+).
2. **Regional Centers**: North America (38%) and Europe (26%) lead sales volume, with Cloud Infrastructure products exhibiting the highest net margins.
3. **Funnel Bottleneck**: Product detail page views convert to cart additions at only 28–32%, revealing a critical UX opportunity to introduce self-service ROI calculators.
