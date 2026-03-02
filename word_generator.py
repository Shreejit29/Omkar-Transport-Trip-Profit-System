from docx import Document
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
                border.set(qn('w:color'), '000000')
                tcBorders.append(border)
            tcPr.append(tcBorders)


def generate_word(trip_date,
                  s1, d1, m1, r1, w1, f1,
                  s2, d2, m2, r2, w2, f2,
                  total_fare,
                  advance, pending_payment,
                  diesel, toll, food, driver,
                  other_expenses,
                  total_expenses, profit):

    doc = Document()
    doc.add_heading("Omkar Transport - Round Trip Report", level=1)

    trip_data = [
        ["Sr. No.", "Particular", "Value"],
        ["1", "Date", str(trip_date)],
        ["2", "Journey 1 Route", f"{s1} → {d1}"],
        ["3", "Material 1", m1],
        ["4", "Fare 1", f"₹ {f1:.2f}"],
        ["5", "Journey 2 Route", f"{s2} → {d2}"],
        ["6", "Material 2", m2],
        ["7", "Fare 2", f"₹ {f2:.2f}"],
        ["8", "Total Round Trip Fare", f"₹ {total_fare:.2f}"],
    ]

    table = doc.add_table(rows=len(trip_data), cols=3)
    for i, row in enumerate(trip_data):
        for j, cell in enumerate(row):
            table.rows[i].cells[j].text = cell
    add_table_borders(table)

    doc.add_heading("Expense Details", level=2)

    expense_data = [
        ["Sr. No.", "Expense Type", "Amount"],
        ["1", "Diesel", f"₹ {diesel:.2f}"],
        ["2", "Toll", f"₹ {toll:.2f}"],
        ["3", "Food", f"₹ {food:.2f}"],
        ["4", "Driver Charges", f"₹ {driver:.2f}"],
    ]

    sr = 5
    for e in other_expenses:
        if e["name"]:
            expense_data.append([str(sr), e["name"], f"₹ {e['amount']:.2f}"])
            sr += 1

    expense_data.append([str(sr), "Total Expenses", f"₹ {total_expenses:.2f}"])

    table = doc.add_table(rows=len(expense_data), cols=3)
    for i, row in enumerate(expense_data):
        for j, cell in enumerate(row):
            table.rows[i].cells[j].text = cell
    add_table_borders(table)

    doc.add_heading("Final Summary", level=2)

    summary = [
        ["Sr. No.", "Particular", "Amount"],
        ["1", "Total Round Trip Fare", f"₹ {total_fare:.2f}"],
        ["2", "Total Expenses", f"₹ {total_expenses:.2f}"],
        ["3", "Net Profit", f"₹ {profit:.2f}"],
        ["4", "Advance Received", f"₹ {advance:.2f}"],
        ["5", "Pending Payment", f"₹ {pending_payment:.2f}"],
    ]

    table = doc.add_table(rows=len(summary), cols=3)
    for i, row in enumerate(summary):
        for j, cell in enumerate(row):
            table.rows[i].cells[j].text = cell
    add_table_borders(table)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
