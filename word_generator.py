from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from io import BytesIO


def add_table_borders(table):
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')

            for border_name in ('top', 'left', 'bottom', 'right'):
                border = OxmlElement(f'w:{border_name}')
                border.set(qn('w:val'), 'single')
                border.set(qn('w:sz'), '4')
                border.set(qn('w:space'), '0')
                border.set(qn('w:color'), '000000')
                tcBorders.append(border)

            tcPr.append(tcBorders)


def generate_word(trip_date, source, destination, material,
                  rate, weight, total_freight,
                  advance, pending_payment,
                  diesel, toll, food, driver, other,
                  total_expenses, profit):

    doc = Document()
    doc.add_heading("Omkar Transport - Trip Report", level=1)

    # ---------------- TRIP DETAILS TABLE ----------------
    trip_data = [
        ["Sr. No.", "Particular", "Value"],
        ["1", "Date", str(trip_date)],
        ["2", "Source", source],
        ["3", "Destination", destination],
        ["4", "Material", material],
        ["5", "Rate per Tonne", f"₹ {rate:.2f}"],
        ["6", "Weight", f"{weight:.2f} Tonnes"],
        ["7", "Total Freight", f"₹ {total_freight:.2f}"],
    ]

    table = doc.add_table(rows=len(trip_data), cols=3)
    for row_idx, row in enumerate(trip_data):
        for col_idx, cell in enumerate(row):
            table.rows[row_idx].cells[col_idx].text = cell

    add_table_borders(table)

    doc.add_heading("Payment Details", level=2)

    payment_data = [
        ["Sr. No.", "Particular", "Amount"],
        ["1", "Advance Received", f"₹ {advance:.2f}"],
        ["2", "Pending Payment", f"₹ {pending_payment:.2f}"],
    ]

    table = doc.add_table(rows=len(payment_data), cols=3)
    for row_idx, row in enumerate(payment_data):
        for col_idx, cell in enumerate(row):
            table.rows[row_idx].cells[col_idx].text = cell

    add_table_borders(table)

    doc.add_heading("Expense Details", level=2)

    expense_data = [
        ["Sr. No.", "Expense Type", "Amount"],
        ["1", "Diesel", f"₹ {diesel:.2f}"],
        ["2", "Toll", f"₹ {toll:.2f}"],
        ["3", "Food", f"₹ {food:.2f}"],
        ["4", "Driver Charges", f"₹ {driver:.2f}"],
        ["5", "Other", f"₹ {other:.2f}"],
        ["6", "Total Expenses", f"₹ {total_expenses:.2f}"],
    ]

    table = doc.add_table(rows=len(expense_data), cols=3)
    for row_idx, row in enumerate(expense_data):
        for col_idx, cell in enumerate(row):
            table.rows[row_idx].cells[col_idx].text = cell

    add_table_borders(table)

    doc.add_heading("Profit Summary", level=2)

    profit_data = [
        ["Sr. No.", "Description", "Amount"],
        ["1", "Total Freight", f"₹ {total_freight:.2f}"],
        ["2", "Total Expenses", f"₹ {total_expenses:.2f}"],
        ["3", "Net Profit", f"₹ {profit:.2f}"],
    ]

    table = doc.add_table(rows=len(profit_data), cols=3)
    for row_idx, row in enumerate(profit_data):
        for col_idx, cell in enumerate(row):
            table.rows[row_idx].cells[col_idx].text = cell

    add_table_borders(table)

    doc.add_paragraph("\nSignature: _______________________")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
