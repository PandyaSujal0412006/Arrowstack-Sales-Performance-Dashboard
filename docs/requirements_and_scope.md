# Project 1: Requirements & Scope Document
**Domain**: B2B Enterprise & Cloud Technology Sales Analytics  
**Intern**: Sujal Pandya | Roll ID: AS-2026-92197 | Reference: AST/INT/2026/OFFER/92197  
**Entity**: Arrowstack Technologies (Batch 2026)  

---

## 1. Real-World Scenario
An enterprise technology and cloud solutions provider requires unified operational visibility into sales revenue, transaction volumes, average deal sizes, geographic penetration, and marketing funnel efficiency across multi-tier accounts. Currently, data resides in siloed CRM tables and digital web logs, preventing leadership from identifying revenue leakages and regional growth opportunities.

## 2. Business Stakeholder & Use Case
* **Primary Stakeholder**: Chief Revenue Officer (CRO), VP of Commercial Sales, and Regional Sales Directors.
* **Decisions Enabled**:
  1. Allocation of regional marketing and enterprise field headcount.
  2. Evaluation and rationalization of discounting bands (e.g. capped at 20% for Enterprise, 10% for Mid-market).
  3. Digital funnel friction reduction between product consideration and cart checkout.
* **Measurable Benefit**: Target 8–12% increase in AOV through product cross-bundling, and 15% reduction in funnel drop-off between trial view and contract initiation.

## 3. Scope Boundaries
* **In-Scope**:
  * Cleaned sales transactions from January 2025 through October 2026.
  * Regional drill-downs across North America, Europe, Asia-Pacific, Latin America, and Middle East & Africa.
  * Product category performance across Cloud Infrastructure, Software Licenses, Hardware & Edge, and Professional Services.
  * End-to-end web acquisition funnel tracking (Sessions -> Views -> Carts -> Orders).
  * Automated data quality rules and reproducible testing suite.
* **Out-of-Scope**:
  * Individual sales representative payroll and commission calculations.
  * Third-party ERP payment gateway direct webhook integration (simulated via transactional status flags).

## 4. Acceptance Criteria Checklist
- [x] Executive KPI metric cards (Total Net Revenue, Completed Orders, AOV, Units Sold, Conversion Rate).
- [x] Dual-axis monthly revenue and order progression with MoM growth velocity indicators.
- [x] Regional and customer segment contribution heatmaps and breakdown charts.
- [x] Category and SKU-level yield tables with average discount tracking.
- [x] Multi-tab formatted Excel analytical model with native formulas.
- [x] Complete SQLite Star Schema relational database with query runner.
- [x] Automated unit test suite with 100% passing status.
