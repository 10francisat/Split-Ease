import streamlit as st
import mysql.connector
from datetime import datetime


def create_connection():
    return mysql.connector.connect(host='localhost',user='Francisa', password='2007',database='SplitEase')


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    #users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      username VARCHAR(255) UNIQUE NOT NULL,
                      password VARCHAR(255) NOT NULL)''')
    #expenses table
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      user_id INT,
                      amount DECIMAL(10,2),
                      description TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users(id))''')
    #user_groups
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_groups (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      name VARCHAR(255) UNIQUE NOT NULL)''')
    #group_expenses
    cursor.execute('''CREATE TABLE IF NOT EXISTS group_expenses (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      group_id INT,
                      user_id INT,
                      amount DECIMAL(10,2),
                      description TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (group_id) REFERENCES user_groups(id),
                      FOREIGN KEY (user_id) REFERENCES users(id))''')
    #settlements
    cursor.execute('''CREATE TABLE IF NOT EXISTS settlements (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      payer_id INT,
                      payee_id INT,
                      amount DECIMAL(10,2),
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (payer_id) REFERENCES users(id),
                      FOREIGN KEY (payee_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        st.success("User registered successfully! Please Login")
    except mysql.connector.IntegrityError:
        st.error("Username already exists. Please choose a different one.")
    finally:
        conn.close()

def get_user_id(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def add_expense(user_id, amount, description):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, description) VALUES (%s, %s, %s)",
            (user_id, amount, description),
        )
        conn.commit()
        st.success("Expense added successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        conn.close()

def view_expenses(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount, description, created_at FROM expenses WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses


def add_group(name, members):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_groups (name) VALUES (%s)", (name,))
        for member in members:
            user_id = get_user_id(member)
            if user_id:
                cursor.execute("INSERT INTO group_members (group_name, user_id) VALUES (%s, %s)", (name, user_id))
        conn.commit()
        st.success("Group added successfully with existing members!  \n [Unregistered usernames will be automatically removed]")
    except mysql.connector.IntegrityError:
        st.error("Group name already exists. Please choose a different one.")
    finally:
        conn.close()

def get_group_id(group_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user_groups WHERE name=%s", (group_name,))
    group = cursor.fetchone()
    conn.close()
    return group[0] if group else None

def add_group_expense(group_name, username, amount, description):
    group_id = get_group_id(group_name)
    user_id = get_user_id(username)
    
    if group_id and user_id:
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO group_expenses (group_id, user_id, amount, description) VALUES (%s, %s, %s, %s)",
                (group_id, user_id, amount, description)
            )
            conn.commit()
            st.success("Group expense added successfully!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            conn.close()
    else:
        st.error("Group or user not found.")

def calculate_group_balances(group_name):

    group_id = get_group_id(group_name)
    if not group_id:
        st.error("Group not found.")
        return {}

    # Retrieve all expenses for the group
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, SUM(amount) FROM group_expenses WHERE group_id=%s GROUP BY user_id", (group_id,))
    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        st.error("No expenses found for this group.")
        return {}

    # Calculate total expenses and equal share for each user
    total_expense = sum(exp[1] for exp in expenses)
    equal_share = total_expense / len(expenses)

    balances = {}
    for user_id, amount in expenses:
        balances[user_id] = amount - equal_share

    return balances
def settle_group_expenses(group_name):
    balances = calculate_group_balances(group_name)
    if not balances:
        return []

    owes = []
    owed = []
    
    conn = create_connection()
    cursor = conn.cursor()

    # Convert user IDs to usernames
    user_id_to_name = {}
    cursor.execute("SELECT id, username FROM users")
    for user_id, username in cursor.fetchall():
        user_id_to_name[user_id] = username

    conn.close()

    for user_id, balance in balances.items():
        username = user_id_to_name.get(user_id, f"User {user_id}")  # Default if not found
        if balance < 0:  
            owes.append((username, -balance))
        elif balance > 0:  
            owed.append((username, balance))

    settlements = []
    i, j = 0, 0
    while i < len(owes) and j < len(owed):
        payer, amount_owed = owes[i]
        payee, amount_owed_to_them = owed[j]

        amount_to_settle = min(amount_owed, amount_owed_to_them)
        settlements.append((payer, payee, amount_to_settle))

        owes[i] = (payer, amount_owed - amount_to_settle)
        owed[j] = (payee, amount_owed_to_them - amount_to_settle)

        if owes[i][1] == 0:
            i += 1
        if owed[j][1] == 0:
            j += 1

    return settlements

def show_settlement_summary(settlements):
    if not settlements:
        st.write("✅ All balances are settled. No transactions needed.")
    else:
        st.write("💰 **Settlements:**")
        for payer, payee, amount in settlements:
            st.write(f"🔹 **{payer}** owes **{payee}** Rs.{amount:.2f}")

def settle_expense(payer_username, payee_username, amount):
    payer_id = get_user_id(payer_username)
    payee_id = get_user_id(payee_username)
    if not payer_id or not payee_id:
        st.error("Invalid payer or payee username.")
        return
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO settlements (payer_id, payee_id, amount) VALUES (%s, %s, %s)", (payer_id, payee_id, amount))
    conn.commit()
    conn.close()
    st.success("Settlement recorded successfully!")


def get_expense_summary():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, SUM(amount) FROM expenses GROUP BY user_id")
    summary = cursor.fetchall()
    conn.close()
    return summary
