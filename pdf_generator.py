from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

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
    elements.append(Spacer(1, 12))

    data = [
        ["Date", str(trip_date)],
        ["Source", source],
        ["Destination", destination],
        ["Material", material],
        ["Rate per Tonne", f"₹ {rate}"],
        ["Weight", f"{weight} Tonnes"],
        ["Total Freight", f"₹ {total_freight}"],
        ["Advance", f"₹ {advance}"],
        ["Pending Payment", f"₹ {pending_payment}"],
        ["Total Expenses", f"₹ {total_expenses}"],
        ["Profit", f"₹ {profit}"],
    ]

    table = Table(data, colWidths=[200, 250])
    elements.append(table)
    elements.append(Spacer(1, 20))

    if uploaded_files:
        elements.append(Paragraph("<b>Bill Attachments</b>", styles['Heading2']))
        elements.append(Spacer(1, 10))

        for file in uploaded_files:
            img = Image(file, width=4*inch, height=4*inch)
            elements.append(img)
            elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer
