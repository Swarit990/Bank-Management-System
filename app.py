
import json
import secrets
import string
from pathlib import Path

import streamlit as st

# ---------------- CONFIGURATION ----------------

DATABASE = Path(__file__).with_name("data.json")
MAX_DEPOSIT = 10000


# ---------------- DATABASE FUNCTIONS ----------------

def load_data():
    if not DATABASE.exists():
        DATABASE.write_text("[]", encoding="utf-8")
        return []

    try:
        with open(DATABASE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        st.error("Unable to read data.json.")
        return []


def save_data():
    temp_file = DATABASE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(st.session_state.accounts, file, indent=4)

    temp_file.replace(DATABASE)


def generate_account_number():
    existing = {
        account["accountNo."]
        for account in st.session_state.accounts
    }

    while True:
        number = "AC" + "".join(
            secrets.choice(string.ascii_uppercase + string.digits)
            for _ in range(8)
        )

        if number not in existing:
            return number


def authenticate(account_number, pin):
    for account in st.session_state.accounts:
        if (
            account["accountNo."] == account_number.strip().upper()
            and account["pin"] == pin
        ):
            return account

    return None


# ---------------- STREAMLIT SETUP ----------------

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide"
)

if "accounts" not in st.session_state:
    st.session_state.accounts = load_data()

accounts = st.session_state.accounts

st.title("🏦 Bank Management System")
st.caption("Manage your accounts using Python and Streamlit.")

st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select an operation",
    [
        "Dashboard",
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",
        "Update Account",
        "Delete Account"
    ]
)


# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.header("Dashboard")

    col1, col2 = st.columns(2)

    col1.metric("Total Accounts", len(accounts))

    total_balance = sum(
        float(account["balance"]) for account in accounts
    )

    col2.metric("Total Balance", f"₹{total_balance:,.2f}")

    if accounts:
        st.subheader("Account Overview")

        st.dataframe(
            [
                {
                    "Name": account["name"],
                    "Account Number": account["accountNo."],
                    "Balance": account["balance"]
                }
                for account in accounts
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No accounts found. Create your first account.")


# ---------------- CREATE ACCOUNT ----------------

elif menu == "Create Account":

    st.header("Create a New Account")

    with st.form("create_form"):

        name = st.text_input("Full Name")
        age = st.number_input(
            "Age", min_value=1, max_value=120, value=18
        )
        email = st.text_input("Email Address")
        pin = st.text_input(
            "Create 4-Digit PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button("Create Account")

    if submit:

        if not name.strip():
            st.error("Please enter your name.")

        elif age < 18:
            st.error("You must be at least 18 years old.")

        elif "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            st.error("Please enter a valid email address.")

        elif not (pin.isdigit() and len(pin) == 4):
            st.error("PIN must contain exactly 4 digits.")

        else:
            account = {
                "name": name.strip(),
                "age": int(age),
                "email": email.strip(),
                "pin": pin,
                "accountNo.": generate_account_number(),
                "balance": 0.0
            }

            accounts.append(account)
            save_data()

            st.success("Account created successfully!")

            st.code(account["accountNo."])
            st.write("Name:", account["name"])
            st.write("Email:", account["email"])
            st.info("Save your account number for future transactions.")


# ---------------- DEPOSIT MONEY ----------------

elif menu == "Deposit Money":

    st.header("Deposit Money")

    with st.form("deposit_form"):

        account_number = st.text_input("Account Number")
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
        amount = st.number_input(
            "Deposit Amount (₹)",
            min_value=0.0,
            value=100.0,
            step=100.0
        )

        submit = st.form_submit_button("Deposit Money")

    if submit:

        account = authenticate(account_number, pin)

        if not account:
            st.error("Incorrect account number or PIN.")

        elif amount <= 0:
            st.error("Amount must be greater than zero.")

        elif amount > MAX_DEPOSIT:
            st.error("Maximum deposit per transaction is ₹10,000.")

        else:
            account["balance"] += amount
            save_data()

            st.success(f"₹{amount:,.2f} deposited successfully!")
            st.metric("Updated Balance", f"₹{account['balance']:,.2f}")


# ---------------- WITHDRAW MONEY ----------------

elif menu == "Withdraw Money":

    st.header("Withdraw Money")

    with st.form("withdraw_form"):

        account_number = st.text_input("Account Number")
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
        amount = st.number_input(
            "Withdrawal Amount (₹)",
            min_value=0.0,
            value=100.0,
            step=100.0
        )

        submit = st.form_submit_button("Withdraw Money")

    if submit:

        account = authenticate(account_number, pin)

        if not account:
            st.error("Incorrect account number or PIN.")

        elif amount <= 0:
            st.error("Amount must be greater than zero.")

        elif amount > account["balance"]:
            st.error("Insufficient balance.")

        else:
            account["balance"] -= amount
            save_data()

            st.success(f"₹{amount:,.2f} withdrawn successfully!")
            st.metric("Remaining Balance", f"₹{account['balance']:,.2f}")


# ---------------- SHOW DETAILS ----------------

elif menu == "Show Details":

    st.header("Account Details")

    with st.form("details_form"):

        account_number = st.text_input("Account Number")
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)

        submit = st.form_submit_button("Show Details")

    if submit:

        account = authenticate(account_number, pin)

        if not account:
            st.error("Incorrect account number or PIN.")

        else:
            st.success("Account verified.")

            st.write("**Name:**", account["name"])
            st.write("**Age:**", account["age"])
            st.write("**Email:**", account["email"])
            st.write("**Account Number:**", account["accountNo."])
            st.metric("Available Balance", f"₹{account['balance']:,.2f}")


# ---------------- UPDATE ACCOUNT ----------------

elif menu == "Update Account":

    st.header("Update Account Details")

    with st.form("update_form"):

        account_number = st.text_input("Account Number")
        pin = st.text_input("Current PIN", type="password", max_chars=4)

        submit = st.form_submit_button("Verify Account")

    if submit:

        account = authenticate(account_number, pin)

        if not account:
            st.error("Incorrect account number or PIN.")

        else:
            st.session_state.edit_account_number = account["accountNo."]
            st.rerun()

    account_number = st.session_state.get("edit_account_number")

    if account_number:

        account = next(
            (
                a for a in accounts
                if a["accountNo."] == account_number
            ),
            None
        )

        if account:

            with st.form("edit_details_form"):

                new_name = st.text_input(
                    "Name", value=account["name"]
                )

                new_email = st.text_input(
                    "Email", value=account["email"]
                )

                new_pin = st.text_input(
                    "New PIN (leave blank to keep current)",
                    type="password",
                    max_chars=4
                )

                submit_update = st.form_submit_button("Save Changes")

            if submit_update:

                if not new_name.strip():
                    st.error("Name cannot be empty.")

                elif (
                    "@" not in new_email
                    or "." not in new_email.rsplit("@", 1)[-1]
                ):
                    st.error("Enter a valid email address.")

                elif new_pin and not (
                    new_pin.isdigit() and len(new_pin) == 4
                ):
                    st.error("New PIN must contain 4 digits.")

                else:
                    account["name"] = new_name.strip()
                    account["email"] = new_email.strip()

                    if new_pin:
                        account["pin"] = new_pin

                    save_data()

                    del st.session_state.edit_account_number

                    st.success("Account updated successfully!")
                    st.rerun()


# ---------------- DELETE ACCOUNT ----------------

elif menu == "Delete Account":

    st.header("Delete Account")

    with st.form("delete_form"):

        account_number = st.text_input("Account Number")
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)

        confirm = st.checkbox(
            "I confirm that I want to delete this account."
        )

        submit = st.form_submit_button("Delete Account")

    if submit:

        account = authenticate(account_number, pin)

        if not account:
            st.error("Incorrect account number or PIN.")

        elif not confirm:
            st.warning("Please confirm account deletion.")

        elif account["balance"] != 0:
            st.error(
                "Withdraw the remaining balance before deleting the account."
            )

        else:
            accounts.remove(account)
            save_data()

            st.success("Account deleted successfully!")
