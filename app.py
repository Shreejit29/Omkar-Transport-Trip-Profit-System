import streamlit as st
from datetime import date
from word_generator import generate_word
from pdf_generator import generate_pdf

st.set_page_config(page_title="Omkar Transport Profit System")
st.title("🚛 Omkar Transport - Round Trip Profit Calculator")

# -----------------------
# Trip Date
# -----------------------
trip_date = st.date_input("Date of Trip", date.today())

# -----------------------
# Journey 1
# -----------------------
st.header("Journey 1 (Normal Trip)")

source1 = st.text_input("Source 1")
destination1 = st.text_input("Destination 1")
material1 = st.text_input("Material 1")
rate1 = st.number_input("Rate per Tonne 1", min_value=0.0)
weight1 = st.number_input("Weight (Tonnes) 1", min_value=0.0)

fare1 = rate1 * weight1
st.write(f"Fare 1: ₹ {fare1:.2f}")

# -----------------------
# Journey 2
# -----------------------
st.header("Journey 2 (Return Trip)")

source2 = st.text_input("Source 2")
destination2 = st.text_input("Destination 2")
material2 = st.text_input("Material 2")
rate2 = st.number_input("Rate per Tonne 2", min_value=0.0)
weight2 = st.number_input("Weight (Tonnes) 2", min_value=0.0)

fare2 = rate2 * weight2
st.write(f"Fare 2: ₹ {fare2:.2f}")

# -----------------------
# Total Fare
# -----------------------
total_fare = fare1 + fare2
st.write(f"# 🚛 Total Round Trip Fare: ₹ {total_fare:.2f}")

# -----------------------
# Payment Section
# -----------------------
st.header("Payment Details")

advance = st.number_input("Advance Received", min_value=0.0)
pending_payment = st.number_input("Pending Payment", min_value=0.0)

# -----------------------
# Expenses
# -----------------------
st.header("Trip Expenses (Combined)")

diesel = st.number_input("Diesel Expense", min_value=0.0)
toll = st.number_input("Toll Expense", min_value=0.0)
food = st.number_input("Food Expense", min_value=0.0)
driver = st.number_input("Driver Charges", min_value=0.0)

st.subheader("Other Expenses (Optional)")

if "other_expenses" not in st.session_state:
    st.session_state.other_expenses = []

if st.button("➕ Add Other Expense"):
    st.session_state.other_expenses.append({"name": "", "amount": 0.0})

for i, expense in enumerate(st.session_state.other_expenses):
    col1, col2 = st.columns(2)
    with col1:
        expense["name"] = st.text_input(f"Expense Name {i+1}", key=f"name_{i}")
    with col2:
        expense["amount"] = st.number_input(f"Amount {i+1}", min_value=0.0, key=f"amount_{i}")

other_total = sum(e["amount"] for e in st.session_state.other_expenses)

total_expenses = diesel + toll + food + driver + other_total
st.write(f"### Total Expenses: ₹ {total_expenses:.2f}")

# -----------------------
# Profit
# -----------------------
profit = total_fare - total_expenses
st.write(f"# ✅ Net Profit: ₹ {profit:.2f}")

# -----------------------
# Upload Bills
# -----------------------
uploaded_files = st.file_uploader(
    "Upload Bill Photos",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

safe_source = source1.replace(" ", "_")
safe_destination = destination2.replace(" ", "_")
file_base = f"{trip_date}_{safe_source}_{safe_destination}"

if st.button("Generate Word Report"):
    file = generate_word(
        trip_date,
        source1, destination1, material1, rate1, weight1, fare1,
        source2, destination2, material2, rate2, weight2, fare2,
        total_fare,
        advance, pending_payment,
        diesel, toll, food, driver,
        st.session_state.other_expenses,
        total_expenses, profit
    )
    st.download_button("Download Word Report", file, file_name=f"{file_base}.docx")

if st.button("Generate PDF Report"):
    file = generate_pdf(
        trip_date,
        source1, destination1, material1, rate1, weight1, fare1,
        source2, destination2, material2, rate2, weight2, fare2,
        total_fare,
        advance, pending_payment,
        diesel, toll, food, driver,
        st.session_state.other_expenses,
        total_expenses, profit,
        uploaded_files
    )
    st.download_button("Download PDF Report", file, file_name=f"{file_base}.pdf")
