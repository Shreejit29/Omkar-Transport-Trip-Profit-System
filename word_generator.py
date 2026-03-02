from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from io import BytesIO

def generate_word(trip_date, source, destination, material,
                  rate, weight, total_freight,
                  advance, pending_payment,
                  diesel, toll, food, driver, other,
                  total_expenses, profit):

    doc = Document()

    doc.add_heading("Omkar Transport - Trip Report", level=1)

    doc.add_paragraph(f"Date: {trip_date}")
    doc.add_paragraph(f"Source: {source}")
    doc.add_paragraph(f"Destination: {destination}")
    doc.add_paragraph(f"Material: {material}")

    doc.add_heading("Freight Details", level=2)
    doc.add_paragraph(f"Rate per Tonne: ₹ {rate}")
    doc.add_paragraph(f"Weight: {weight} Tonnes")
    doc.add_paragraph(f"Total Freight: ₹ {total_freight}")

    doc.add_heading("Payment Details", level=2)
    doc.add_paragraph(f"Advance: ₹ {advance}")
    doc.add_paragraph(f"Pending Payment: ₹ {pending_payment}")

    doc.add_heading("Expenses", level=2)
    doc.add_paragraph(f"Diesel: ₹ {diesel}")
    doc.add_paragraph(f"Toll: ₹ {toll}")
    doc.add_paragraph(f"Food: ₹ {food}")
    doc.add_paragraph(f"Driver: ₹ {driver}")
    doc.add_paragraph(f"Other: ₹ {other}")
    doc.add_paragraph(f"Total Expenses: ₹ {total_expenses}")

    doc.add_heading("Profit Summary", level=2)
    doc.add_paragraph(f"Net Profit: ₹ {profit}")

    doc.add_paragraph("\nSignature: _______________________")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
