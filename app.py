import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Personal Finance Tracker", layout="centered", page_icon="💰")

st.title("💸 Personal Finance Tracker")
st.write("Track your daily expenses and visualize spending trends.")

# File to store expenses
file_path = "expenses.csv"

# Load or create DataFrame
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])

# --- Input Fields ---
with st.form("expense_form"):
    col1, col2 = st.columns(2)
    with col1:
        expense_date = st.date_input("Date", date.today())
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
    amount = st.number_input("Amount", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = pd.DataFrame([[expense_date, category, amount]], columns=["Date", "Category", "Amount"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(file_path, index=False)
        st.success("✅ Expense added!")

# --- Expense Table ---
st.subheader("📊 Expense Table")
st.dataframe(df)

# --- Expense Summary ---
st.subheader("📈 Expense Summary by Category")
summary = df.groupby("Category")["Amount"].sum()
st.bar_chart(summary)

# --- Line chart by Date ---
df["Date"] = pd.to_datetime(df["Date"])
daily = df.groupby("Date")["Amount"].sum().reset_index()

st.subheader("📅 Daily Spending Trend")
fig, ax = plt.subplots()
ax.plot(daily["Date"], daily["Amount"], marker='o', color='green')
ax.set_xlabel("Date")
ax.set_ylabel("Total Amount")
ax.set_title("Spending Over Time")
st.pyplot(fig)
