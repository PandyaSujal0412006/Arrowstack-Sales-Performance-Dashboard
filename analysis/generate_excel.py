"""
==============================================================================
PROJECT 1: SALES PERFORMANCE DASHBOARD - EXCEL WORKBOOK GENERATOR
Arrowstack Technologies Data Analytics Internship (Batch 2026)
Candidate: Sujal Pandya | Roll ID: AS-2026-92197
==============================================================================
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_sales_data.csv")
OUTPUT_EXCEL_PATH = os.path.join(BASE_DIR, "analysis", "sales_performance_analysis.xlsx")

def create_styled_excel():
    df = pd.read_csv(DATA_PATH)
    completed_df = df[df["order_status"] == "Completed"].copy()
    
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # Styles
    navy_header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    accent_blue_fill = PatternFill(start_color="2A5C9A", end_color="2A5C9A", fill_type="solid")
    kpi_card_fill = PatternFill(start_color="EBF3FA", end_color="EBF3FA", fill_type="solid")
    zebra_fill = PatternFill(start_color="F7F9FB", end_color="F7F9FB", fill_type="solid")
    total_fill = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
    
    font_title = Font(name="Calibri", size=16, bold=True, color="1B365D")
    font_subtitle = Font(name="Calibri", size=11, italic=True, color="555555")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_kpi_label = Font(name="Calibri", size=10, bold=True, color="555555")
    font_kpi_val = Font(name="Calibri", size=16, bold=True, color="1B365D")
    font_total = Font(name="Calibri", size=11, bold=True, color="000000")
    font_regular = Font(name="Calibri", size=11, color="000000")
    
    thin_border = Border(
        left=Side(style='thin', color='D3D3D3'),
        right=Side(style='thin', color='D3D3D3'),
        top=Side(style='thin', color='D3D3D3'),
        bottom=Side(style='thin', color='D3D3D3')
    )
    double_bottom_border = Border(
        top=Side(style='thin', color='000000'),
        bottom=Side(style='double', color='000000')
    )
    
    # ----------------------------------------------------
    # TAB 1: EXECUTIVE KPI SUMMARY
    # ----------------------------------------------------
    ws_exec = wb.create_sheet(title="Executive KPI Summary")
    ws_exec.views.sheetView[0].showGridLines = True
    
    ws_exec["B2"] = "ARROWSTACK TECHNOLOGIES - SALES PERFORMANCE DASHBOARD"
    ws_exec["B2"].font = font_title
    ws_exec["B3"] = "Executive Analytics Model | Candidate: Sujal Pandya (AS-2026-92197) | Synthetic Dataset"
    ws_exec["B3"].font = font_subtitle
    
    # KPI Cards Layout
    cards = [
        ("TOTAL NET REVENUE", "=SUM('Cleaned Sales Data'!M2:M3801)", "$#,##0.00", "B5", "C6"),
        ("TOTAL COMPLETED ORDERS", "=COUNTIF('Cleaned Sales Data'!O2:O3801, \"Completed\")", "#,##0", "E5", "F6"),
        ("AVERAGE ORDER VALUE (AOV)", "=C6/F6", "$#,##0.00", "H5", "I6"),
        ("TOTAL UNITS SOLD", "=SUMIF('Cleaned Sales Data'!O2:O3801, \"Completed\", 'Cleaned Sales Data'!I2:I3801)", "#,##0", "K5", "L6")
    ]
    
    for title, formula, num_fmt, top_left, bottom_right in cards:
        c_tl = ws_exec[top_left]
        tl_col, tl_row = top_left[0], int(top_left[1:])
        br_col, br_row = bottom_right[0], int(bottom_right[1:])
        
        ws_exec.merge_cells(f"{top_left}:{chr(ord(tl_col)+1)}{tl_row}")
        c_tl.value = title
        c_tl.font = font_kpi_label
        c_tl.alignment = Alignment(horizontal="center", vertical="center")
        
        ws_exec.merge_cells(f"{tl_col}{tl_row+1}:{bottom_right}")
        val_cell = ws_exec[f"{tl_col}{tl_row+1}"]
        val_cell.value = formula
        val_cell.font = font_kpi_val
        val_cell.number_format = num_fmt
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        for r in range(tl_row, br_row + 1):
            for c in range(ord(tl_col) - ord('A') + 1, ord(br_col) - ord('A') + 1):
                cell = ws_exec.cell(row=r, column=c)
                cell.fill = kpi_card_fill
                cell.border = thin_border

    # Segment Performance Table on Executive Tab
    ws_exec["B9"] = "Performance Breakdown by Customer Segment"
    ws_exec["B9"].font = Font(name="Calibri", size=13, bold=True, color="1B365D")
    
    headers_seg = ["Customer Segment", "Order Count", "Units Sold", "Gross Revenue ($)", "Net Revenue ($)", "AOV ($)", "Revenue Share %"]
    for col_idx, h in enumerate(headers_seg, start=2):
        cell = ws_exec.cell(row=10, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
        
    segments = ["Enterprise", "Mid-Market", "SMB", "Government & Edu"]
    for row_idx, seg in enumerate(segments, start=11):
        ws_exec.cell(row=row_idx, column=2, value=seg).font = font_regular
        
        # Formulas referencing data sheet
        ws_exec.cell(row=row_idx, column=3, value=f"=COUNTIFS('Cleaned Sales Data'!D:D, \"{seg}\", 'Cleaned Sales Data'!O:O, \"Completed\")").number_format = "#,##0"
        ws_exec.cell(row=row_idx, column=4, value=f"=SUMIFS('Cleaned Sales Data'!I:I, 'Cleaned Sales Data'!D:D, \"{seg}\", 'Cleaned Sales Data'!O:O, \"Completed\")").number_format = "#,##0"
        ws_exec.cell(row=row_idx, column=5, value=f"=SUMIFS('Cleaned Sales Data'!L:L, 'Cleaned Sales Data'!D:D, \"{seg}\", 'Cleaned Sales Data'!O:O, \"Completed\")").number_format = "$#,##0.00"
        ws_exec.cell(row=row_idx, column=6, value=f"=SUMIFS('Cleaned Sales Data'!M:M, 'Cleaned Sales Data'!D:D, \"{seg}\", 'Cleaned Sales Data'!O:O, \"Completed\")").number_format = "$#,##0.00"
        ws_exec.cell(row=row_idx, column=7, value=f"=F{row_idx}/C{row_idx}").number_format = "$#,##0.00"
        ws_exec.cell(row=row_idx, column=8, value=f"=F{row_idx}/$C$6").number_format = "0.0%"
        
        for col_idx in range(2, 9):
            ws_exec.cell(row=row_idx, column=col_idx).border = thin_border
            if row_idx % 2 == 0:
                ws_exec.cell(row=row_idx, column=col_idx).fill = zebra_fill
                
    # Total Row
    tot_row = 15
    ws_exec.cell(row=tot_row, column=2, value="Grand Total").font = font_total
    ws_exec.cell(row=tot_row, column=3, value="=SUM(C11:C14)").number_format = "#,##0"
    ws_exec.cell(row=tot_row, column=4, value="=SUM(D11:D14)").number_format = "#,##0"
    ws_exec.cell(row=tot_row, column=5, value="=SUM(E11:E14)").number_format = "$#,##0.00"
    ws_exec.cell(row=tot_row, column=6, value="=SUM(F11:F14)").number_format = "$#,##0.00"
    ws_exec.cell(row=tot_row, column=7, value="=F15/C15").number_format = "$#,##0.00"
    ws_exec.cell(row=tot_row, column=8, value="=SUM(H11:H14)").number_format = "0.0%"
    for col_idx in range(2, 9):
        c = ws_exec.cell(row=tot_row, column=col_idx)
        c.font = font_total
        c.fill = total_fill
        c.border = double_bottom_border

    # ----------------------------------------------------
    # TAB 2: MONTHLY REVENUE TRENDS
    # ----------------------------------------------------
    ws_month = wb.create_sheet(title="Monthly Trends")
    ws_month.views.sheetView[0].showGridLines = True
    
    ws_month["B2"] = "MONTHLY SALES PERFORMANCE & MOM GROWTH"
    ws_month["B2"].font = font_title
    
    headers_month = ["Year-Month", "Completed Orders", "Total Units", "Gross Revenue ($)", "Net Revenue ($)", "AOV ($)", "MoM Growth %"]
    for col_idx, h in enumerate(headers_month, start=2):
        cell = ws_month.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
        
    monthly_summary = completed_df.groupby("year_month").agg(
        orders=("order_id", "nunique"),
        units=("quantity", "sum"),
        gross_rev=("gross_revenue", "sum"),
        net_rev=("net_revenue", "sum")
    ).reset_index().sort_values("year_month")
    
    for r_idx, row in monthly_summary.iterrows():
        excel_row = 5 + r_idx
        ws_month.cell(row=excel_row, column=2, value=row["year_month"]).alignment = Alignment(horizontal="center")
        ws_month.cell(row=excel_row, column=3, value=row["orders"]).number_format = "#,##0"
        ws_month.cell(row=excel_row, column=4, value=row["units"]).number_format = "#,##0"
        ws_month.cell(row=excel_row, column=5, value=row["gross_rev"]).number_format = "$#,##0.00"
        ws_month.cell(row=excel_row, column=6, value=row["net_rev"]).number_format = "$#,##0.00"
        ws_month.cell(row=excel_row, column=7, value=f"=F{excel_row}/C{excel_row}").number_format = "$#,##0.00"
        
        if r_idx == 0:
            ws_month.cell(row=excel_row, column=8, value=0.0).number_format = "0.0%"
        else:
            prev_row = excel_row - 1
            ws_month.cell(row=excel_row, column=8, value=f"=(F{excel_row}-F{prev_row})/F{prev_row}").number_format = "0.0%"
            
        for col_idx in range(2, 9):
            ws_month.cell(row=excel_row, column=col_idx).border = thin_border
            if r_idx % 2 == 1:
                ws_month.cell(row=excel_row, column=col_idx).fill = zebra_fill
                
    # ----------------------------------------------------
    # TAB 3: REGIONAL PERFORMANCE
    # ----------------------------------------------------
    ws_reg = wb.create_sheet(title="Regional Performance")
    ws_reg.views.sheetView[0].showGridLines = True
    ws_reg["B2"] = "GEOGRAPHICAL REVENUE CONTRIBUTION & PENETRATION"
    ws_reg["B2"].font = font_title
    
    headers_reg = ["Region", "Completed Orders", "Total Units", "Gross Revenue ($)", "Net Revenue ($)", "AOV ($)", "Revenue Share %"]
    for col_idx, h in enumerate(headers_reg, start=2):
        cell = ws_reg.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
        
    region_summary = completed_df.groupby("region").agg(
        orders=("order_id", "nunique"),
        units=("quantity", "sum"),
        gross_rev=("gross_revenue", "sum"),
        net_rev=("net_revenue", "sum")
    ).reset_index().sort_values("net_rev", ascending=False)
    
    for r_idx, row in region_summary.iterrows():
        excel_row = 5 + r_idx
        ws_reg.cell(row=excel_row, column=2, value=row["region"])
        ws_reg.cell(row=excel_row, column=3, value=row["orders"]).number_format = "#,##0"
        ws_reg.cell(row=excel_row, column=4, value=row["units"]).number_format = "#,##0"
        ws_reg.cell(row=excel_row, column=5, value=row["gross_rev"]).number_format = "$#,##0.00"
        ws_reg.cell(row=excel_row, column=6, value=row["net_rev"]).number_format = "$#,##0.00"
        ws_reg.cell(row=excel_row, column=7, value=f"=F{excel_row}/C{excel_row}").number_format = "$#,##0.00"
        ws_reg.cell(row=excel_row, column=8, value=f"=F{excel_row}/SUM($F$5:$F${4+len(region_summary)})").number_format = "0.0%"
        
        for col_idx in range(2, 9):
            ws_reg.cell(row=excel_row, column=col_idx).border = thin_border
            if r_idx % 2 == 1:
                ws_reg.cell(row=excel_row, column=col_idx).fill = zebra_fill
                
    # ----------------------------------------------------
    # TAB 4: PRODUCT CATEGORY ANALYSIS
    # ----------------------------------------------------
    ws_prod = wb.create_sheet(title="Product Category Analysis")
    ws_prod.views.sheetView[0].showGridLines = True
    ws_prod["B2"] = "PRODUCT CATEGORY & SKU REVENUE CONTRIBUTION"
    ws_prod["B2"].font = font_title
    
    headers_prod = ["Product Category", "Product Name", "Orders", "Units Sold", "Gross Revenue ($)", "Net Revenue ($)", "Avg Discount %", "Revenue / Unit ($)"]
    for col_idx, h in enumerate(headers_prod, start=2):
        cell = ws_prod.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
        
    prod_summary = completed_df.groupby(["product_category", "product_name"]).agg(
        orders=("order_id", "nunique"),
        units=("quantity", "sum"),
        gross_rev=("gross_revenue", "sum"),
        net_rev=("net_revenue", "sum"),
        avg_disc=("discount_rate", "mean")
    ).reset_index().sort_values(["product_category", "net_rev"], ascending=[True, False])
    
    for r_idx, row in prod_summary.iterrows():
        excel_row = 5 + r_idx
        ws_prod.cell(row=excel_row, column=2, value=row["product_category"])
        ws_prod.cell(row=excel_row, column=3, value=row["product_name"])
        ws_prod.cell(row=excel_row, column=4, value=row["orders"]).number_format = "#,##0"
        ws_prod.cell(row=excel_row, column=5, value=row["units"]).number_format = "#,##0"
        ws_prod.cell(row=excel_row, column=6, value=row["gross_rev"]).number_format = "$#,##0.00"
        ws_prod.cell(row=excel_row, column=7, value=row["net_rev"]).number_format = "$#,##0.00"
        ws_prod.cell(row=excel_row, column=8, value=row["avg_disc"]).number_format = "0.0%"
        ws_prod.cell(row=excel_row, column=9, value=f"=G{excel_row}/E{excel_row}").number_format = "$#,##0.00"
        
        for col_idx in range(2, 10):
            ws_prod.cell(row=excel_row, column=col_idx).border = thin_border
            if r_idx % 2 == 1:
                ws_prod.cell(row=excel_row, column=col_idx).fill = zebra_fill

    # ----------------------------------------------------
    # TAB 5: CLEANED SALES DATA (Raw Table)
    # ----------------------------------------------------
    ws_data = wb.create_sheet(title="Cleaned Sales Data")
    ws_data.views.sheetView[0].showGridLines = True
    
    raw_headers = list(df.columns)
    for col_idx, h in enumerate(raw_headers, start=1):
        cell = ws_data.cell(row=1, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = accent_blue_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border
        
    for r_idx, row in df.iterrows():
        excel_row = 2 + r_idx
        for col_idx, val in enumerate(row, start=1):
            c = ws_data.cell(row=excel_row, column=col_idx, value=val)
            c.font = font_regular
            c.border = thin_border
            if col_idx in [10, 12, 13]: # unit_price, gross_rev, net_rev
                c.number_format = "$#,##0.00"
            elif col_idx == 11: # discount_rate
                c.number_format = "0.0%"

    # Autofit Column Widths across all sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if len(val_str) > max_len and not val_str.startswith('='):
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    os.makedirs(os.path.dirname(OUTPUT_EXCEL_PATH), exist_ok=True)
    wb.save(OUTPUT_EXCEL_PATH)
    print(f"[OK] Formatted analytical Excel workbook created at {OUTPUT_EXCEL_PATH}")

if __name__ == "__main__":
    create_styled_excel()
