import streamlit as st
import mysql.connector
from datetime import datetime
import Function as fun
import css 

# Streamlit
css.load_css()

st.title("SplitEase")
menu = ["Login", "Register", "Add Expense", "View Expenses","Add Group Name And Members","Add Group Expense","Settle Group Expenses","Settle Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create an Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Register"):
        fun.register_user(username, password)
        #st.success("Registered successfully! Please login.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user = fun.login_user(username, password)
        if user:
            st.session_state["user_id"] = user[0]
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

elif choice == "Add Expense" and "user_id" in st.session_state:
    st.subheader("Add an Expense")
    amount = st.number_input("Amount", min_value=0.01, format="%.2f")
    description = st.text_area("Description")
    if st.button("Add Expense"):
        fun.add_expense(st.session_state["user_id"], amount, description)
        #st.success("Expense added successfully!")

elif choice == "View Expenses" and "user_id" in st.session_state:
    st.subheader("Your Expenses")
    expenses = fun.view_expenses(st.session_state["user_id"])
    for expense in expenses:
        st.write(f"💸 {expense[0]} - {expense[1]} ({expense[2]})")

if choice == "Add Group Name And Members" and "user_id" in st.session_state:
    st.subheader("Create a Group")
    group_name = st.text_input("Group Name")
    members = st.text_area("Enter usernames of group members (comma-separated)").split(",")
    members = [m.strip() for m in members if m.strip()]
    if st.button("Create Group"):
        fun.add_group(group_name, members)

elif choice == "Add Group Expense" and "user_id" in st.session_state:
    st.subheader("Add a Group Expense")
    group_name = st.text_input("Group Name")
    username = st.text_input("Your Username")
    amount = st.number_input("Amount", min_value=0.01, format="%.2f")
    description = st.text_area("Description")
    if st.button("Add Expense"):
        fun.add_group_expense(group_name, username, amount, description)

 

elif choice == "Settle Group Expenses" and "user_id" in st.session_state:
    st.subheader("Settle Group Expenses")
    group_name = st.text_input("Enter Group Name")
    
    if st.button("Settle Expenses"):
        settlements = fun.settle_group_expenses(group_name)
        fun.show_settlement_summary(settlements)

elif choice == "Settle Up" and "user_id" in st.session_state:
    st.subheader("Settle an Expense")
    payer_username = st.text_input("Your Username")
    payee_username = st.text_input("Payee Username")
    amount = st.number_input("Amount", min_value=0.01, format="%.2f")
    if st.button("Settle Up"):
        fun.settle_expense(payer_username, payee_username, amount)
