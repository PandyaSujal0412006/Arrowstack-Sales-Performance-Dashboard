# Project 1: Decision Log & Architectural Trade-Offs
**Candidate**: Sujal Pandya | Roll ID: AS-2026-92197  
**Arrowstack Technologies Virtual Internship (Batch 2026)**  

---

| Decision ID | Decision Title | Options Evaluated | Chosen Approach | Justification & Impact |
| :--- | :--- | :--- | :--- | :--- |
| **DEC-001** | Presentation Framework | Power BI vs Streamlit vs React | **Streamlit with Plotly** | Allows zero-license reproducible interactive execution in Python, combining dynamic charts with embedded SQL querying and CSV exports. |
| **DEC-002** | Revenue Treatment for Cancelled Orders | Gross Revenue Inclusion vs Exclusion | **Exclusion (Completed Only)** | Including cancelled or refunded orders in net revenue distorts managerial decisions and inflates AOV. Transparent toggle provided for auditing. |
| **DEC-003** | Database Storage Layer | Flat CSV vs SQLite vs PostgreSQL Server | **SQLite Star Schema** | Standardized ANSI SQL compatibility, zero external server dependencies, immediate portability for mentor evaluation. |
| **DEC-004** | Acquisition Funnel Modeling | Aggregated Monthly vs Daily Grain | **Daily Grain Modeling** | Daily records allow granular date filtering in the dashboard and accurate correlation between marketing pushes and conversions. |
| **DEC-005** | Discounting Policy Tracking | Fixed Currency Discount vs Percentage | **Percentage-based Rate** | Enables scale-invariant evaluation of customer segments (e.g. Enterprise contracts vs SMB volume pricing). |
