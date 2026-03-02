from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def styled_table(data):
    table = Table(data, colWidths=[60, 200, 150])
    table.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ])
    return table


def generate_pdf(trip_date, source, destination, material,
                 rate, weight, total_freight,
                 advance, pending_payment,
                 diesel, toll, food, driver, other,
                 total_expenses, profit,
                 uploaded_files):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Omkar Transport - Trip Report</b>", styles['Title']))
    elements.append(Spacer(1, 20))

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

    elements.append(styled_table(trip_data))
    elements.append(Spacer(1, 20))

    payment_data = [
        ["Sr. No.", "Particular", "Amount"],
        ["1", "Advance Received", f"₹ {advance:.2f}"],
        ["2", "Pending Payment", f"₹ {pending_payment:.2f}"],
    ]

    elements.append(styled_table(payment_data))
    elements.append(Spacer(1, 20))

    expense_data = [
        ["Sr. No.", "Expense Type", "Amount"],
        ["1", "Diesel", f"₹ {diesel:.2f}"],
        ["2", "Toll", f"₹ {toll:.2f}"],
        ["3", "Food", f"₹ {food:.2f}"],
        ["4", "Driver Charges", f"₹ {driver:.2f}"],
        ["5", "Other", f"₹ {other:.2f}"],
        ["6", "Total Expenses", f"₹ {total_expenses:.2f}"],
    ]

    elements.append(styled_table(expense_data))
    elements.append(Spacer(1, 20))

    profit_data = [
        ["Sr. No.", "Description", "Amount"],
        ["1", "Total Freight", f"₹ {total_freight:.2f}"],
        ["2", "Total Expenses", f"₹ {total_expenses:.2f}"],
        ["3", "Net Profit", f"₹ {profit:.2f}"],
    ]

    elements.append(styled_table(profit_data))
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
