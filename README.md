# Split-Ease
Team Name: Error 404 Squad
Team Member:
1. Francisa Thankachan - Government Model Engineering College
2. Annada S - Government Model Engineering College

HOSTED PROJECT LINK

PROJECT DESCRIPTION
Splitwise is a bill-splitting and expense-sharing app that helps groups of people track shared expenses and settle debts easily. It is commonly used by friends, roommates, travel groups, and couples to keep track of who paid for what and who owes whom.

THE PROBLEM STATEMENT
How can we simplify and organize the process of splitting expenses and managing shared finances among groups of people?

THE SOLUTION
Develop a website that simplifies and organizes shared expense management.

SplitEase is a bill-splitting website that helps groups manage shared expenses easily. Users can add expenses, specify participants, and track who owes whom. It calculates individual shares and maintains transparent records, eliminating manual calculations. The app simplifies debt settlements by minimizing transactions, ensuring fair and efficient repayments. Features like expense reminders and custom splits make it versatile for situations like trips, dinners, or rent sharing. It enhances transparency, reduces social discomfort in money matters, and keeps relationships smooth by ensuring fairness. It's a practical tool for friends, roommates, or any group sharing costs.

TECHNICAL
Technologies/Components Used

For Software:
~Languages Used:
Python → Backend logic and database handling
SQL (MySQL) → Database management and storage

~Frameworks Used:
Streamlit → Web-based UI for a lightweight, interactive experience

~Libraries Used:
mysql-connector-python → Connect and interact with MySQL
datetime → Handling timestamps for transactions

~Tools Used:
MySQL Server → Database management
Streamlit → Web framework for UI
VS Code → IDE for development

For Hardware:
~Main Components:
Laptop / PC → For development

~Specifications:
Processor: Minimum Intel i3 / Ryzen 3 (Recommended i5+ for performance)
RAM: At least 4GB (8GB+ recommended for smooth execution)
Storage: At least 10GB free space (for database and logs)

~Tools Required:
XAMPP / MySQL Workbench → For managing MySQL database
Git & GitHub → For version control

Implementation
For Software:

1.Database Setup (MySQL)
>Create tables for users, groups, expenses, and settlements
>Establish relationships using foreign keys
>Use transactions to handle settlements safely

2️.Backend (Python + Streamlit)
>User Authentication (Register/Login with session handling)
>Expense Tracking (Add/view individual & group expenses)
>Group Expense Calculation (Splitting costs and settlement logic)

3️.Frontend (Streamlit UI Enhancements)
>Custom CSS Styling (Better UI experience)
>Navigation & Sidebar Menu (For better usability)
>Dynamic Data Display (Show expenses & settlements interactively)

4️.Testing & Debugging
>Test expense calculations
>Verify user login & group settlements
>Ensure database connections are secure

RUN
streamlit run Split-Ease.py

PROJECT DOCUMENTATION

SplitEase is a website designed to simplify managing and splitting expenses among friends, family, or groups. It helps users track shared costs, calculate balances, and settle up payments, making group spending transparent and easy.

Purpose:
To provide a platform where users can efficiently split and track shared expenses.

Features:
>Create Groups: Users can create groups (e.g., family, roommates, friends) to manage shared expenses.
>Add Expenses: Users can add expenses with details like amount, date, description, and the people involved.
>Split Expenses: The app allows for automatic or manual splitting of expenses across group members.
>Track Balances: The app calculates who owes what and who is owed.
>Settle Debts: It provides users with options to pay or settle their debts easily.
>Notifications: Notify users when expenses are added or when balances change.
>Currency Support: Supports multiple currencies for international use.
>Reports: Provides expense reports to see spending patterns.

SCREENSHOTS






