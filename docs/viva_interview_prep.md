# Project 1: Viva / Interview Questions & Model Answers
**Candidate**: Sujal Pandya | Roll ID: AS-2026-92197  
**Arrowstack Technologies Virtual Internship (Batch 2026)**  
**Handbook Alignment**: Section 16 Evaluation Criteria  

---

### Q1: What business or user problem does the project solve, and how did you define success?
**Model Answer**:  
"The project addresses the lack of unified revenue visibility and customer acquisition efficiency for B2B technology operations. Commercial leaders previously struggled to evaluate the net financial yield of discounting strategies, regional variations, and web funnel drop-offs.  
I defined success across three dimensions:
1. **Analytical Accuracy**: Zero data-quality defects (zero duplicate transactions, no negative prices, 100% referential integrity).
2. **Defensible Reporting**: Clear separation of Completed transactions vs. Cancelled/Refunded deals when calculating Net Revenue and AOV.
3. **Actionability**: Delivering a low-friction interactive dashboard that equips executives to pinpoint underperforming territories and optimization bottlenecks in under 3 clicks."

### Q2: Which design, technical, analytical or research decision had the biggest impact on the result?
**Model Answer**:  
"The decision to structure the data layer as an ANSI SQL Star Schema (`fact_sales`, `fact_daily_traffic`, `dim_customers`, `dim_products`) rather than leaving it in flat denormalized CSVs had the greatest impact. It unlocked high-performance dimensional filtering, enabled automated referential integrity testing, and allowed stakeholders to execute ad-hoc SQL queries directly within the dashboard interface."

### Q3: How did you validate the quality or correctness of your work?
**Model Answer**:  
"I implemented a 3-layer validation framework:
1. **SQL Automated Integrity Checks**: Checked primary key uniqueness, null bounds, financial range rules, and hierarchical funnel constraints ($Sessions \ge Views \ge Carts \ge Orders$).
2. **Pytest Unit Test Suite**: Wrote 6 automated tests in `test_sales_kpis.py` covering schema validity, mathematical reconciliation of formulas, and Excel structure. All 6 passed in 1.61 seconds.
3. **Cross-Tool Excel Reconciliation**: Re-computed metrics in Excel using native formulas (`SUMIFS`, `COUNTIFS`, `AVERAGE`) to verify that numbers matched the Python and SQL results to the cent."

### Q4: What edge cases, limitations or risks did you identify?
**Model Answer**:  
"Key edge cases identified:
* **Order Status Anomalies**: Handling cancelled and refunded orders so they don't artificially inflate realized sales while retaining their audit footprint.
* **Leap Years and Calendar Variations**: Accounting for differing month lengths when calculating MoM percentage shifts.
* **Limitations**: The current implementation operates on batch historical data rather than real-time event streaming; currency conversions are pre-standardized to USD."

### Q5: What would you change if this solution had to support 10x the users/data/workload?
**Model Answer**:  
"If scaling from ~3,800 records to millions of records and hundreds of concurrent users:
1. Migrate SQLite to an enterprise data warehouse (Snowflake, BigQuery, or Amazon Redshift) with columnar storage and pre-aggregated materialized views for monthly and regional rollups.
2. Implement Redis or Memcached caching for repeated analytical queries in Streamlit.
3. Decouple the frontend from direct computation using an asynchronous FastAPI service layer with paginated endpoints."

### Q6: How would you explain the project to a non-technical stakeholder?
**Model Answer**:  
"I would explain it as a cockpit for the business: just like a pilot needs an instrument panel showing altitude, speed, and fuel, our sales leadership needs an instant view of how much cash the company is bringing in, which regions and products are driving that revenue, and where online visitors are getting stuck before making a purchase. This dashboard turns raw transaction logs into clear, actionable business guidance."

### Q7: Which part of the project required the most independent problem-solving?
**Model Answer**:  
"Designing the synthetic data generator to accurately reflect real-world business dynamics—such as quarterly enterprise procurement spikes, segment-specific discounting tiers, and mathematically consistent web funnel drop-offs—while embedding realistic edge cases without breaking integrity constraints."
