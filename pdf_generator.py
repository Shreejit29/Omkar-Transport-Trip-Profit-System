from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def styled_table(data):
    table = Table(data, colWidths=[60, 220, 150])
    table.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ])
    return table


def generate_pdf(trip_date,
                 s1, d1, m1, r1, w1, f1,
                 s2, d2, m2, r2, w2, f2,
                 total_fare,
                 advance, pending_payment,
                 diesel, toll, food, driver,
                 other_expenses,
                 total_expenses, profit,
                 uploaded_files):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Omkar Transport - Round Trip Report</b>", styles['Title']))
    elements.append(Spacer(1, 20))

    trip_data = [
        ["Sr. No.", "Particular", "Value"],
        ["1", "Date", str(trip_date)],
        ["2", "Journey 1 Route", f"{s1} → {d1}"],
        ["3", "Fare 1", f"₹ {f1:.2f}"],
        ["4", "Journey 2 Route", f"{s2} → {d2}"],
        ["5", "Fare 2", f"₹ {f2:.2f}"],
        ["6", "Total Round Trip Fare", f"₹ {total_fare:.2f}"],
    ]

    elements.append(styled_table(trip_data))
    elements.append(Spacer(1, 20))

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

    elements.append(styled_table(expense_data))
    elements.append(Spacer(1, 20))

    summary = [
        ["Sr. No.", "Particular", "Amount"],
        ["1", "Total Round Trip Fare", f"₹ {total_fare:.2f}"],
        ["2", "Total Expenses", f"₹ {total_expenses:.2f}"],
        ["3", "Net Profit", f"₹ {profit:.2f}"],
        ["4", "Advance Received", f"₹ {advance:.2f}"],
        ["5", "Pending Payment", f"₹ {pending_payment:.2f}"],
    ]

    elements.append(styled_table(summary))
    elements.append(Spacer(1, 20))

    if uploaded_files:
        elements.append(Paragraph("<b>Bill Attachments</b>", styles['Heading2']))
        elements.append(Spacer(1, 10))
        for file in uploaded_files:
            img = Image(file, width=4 * inch, height=4 * inch)
            elements.append(img)
            elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer
