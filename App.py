import pandas as pd
import streamlit as st

# 1. PAGE CONFIGURATION & STYLING
st.set_page_config(
    page_title="Imana Enterprise Core Banking",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better mobile & desktop UI
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    div[data-testid="stMetricValue"] { font-size: 1.3rem; font-weight: bold; color: #0d47a1; }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. INITIALIZE DATABASE / SESSION STATE
if "users" not in st.session_state:
    st.session_state.users = {
        "bakri": {"name": "Bakri", "role": "Maker"},
        "mamme": {"name": "Mamme", "role": "Manager"},
        "mahamad": {"name": "Mahamad", "role": "Checker"},
        "kalif": {"name": "Kalif", "role": "CEO"},
        "auditor": {"name": "Auditor User", "role": "Auditor"},
    }

if "capital" not in st.session_state:
    st.session_state.capital = {"CBE": 50000.0, "CBO": 30000.0, "Cash": 100000.0}

if "customers" not in st.session_state:
    st.session_state.customers = {
        "CUST01": {
            "name": "Ahmad Tarre",
            "gender": "Dhiira",
            "age": 28,
            "balance": 5000.0,
            "status": "Active",
        },
        "CUST02": {
            "name": "Kadiijaa Ali",
            "gender": "Dubartii",
            "age": 24,
            "balance": 2000.0,
            "status": "Active",
        },
    }

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "logged_user" not in st.session_state:
    st.session_state.logged_user = None


# 3. LOGIN / LOGOUT SYSTEM
def login_screen():
    st.markdown(
        "<h2 style='text-align: center; color: #0d47a1;'>🏦 Imana Enterprise App</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center;'>Core Banking System - Sign In</p>",
        unsafe_allow_html=True,
    )

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username").strip().lower()
            password = st.text_input("Password", type="password").strip().lower()
            btn_login = st.form_submit_button("Seeni (Login)")

            if btn_login:
                if (
                    username in st.session_state.users
                    and password == username
                ):
                    st.session_state.logged_user = st.session_state.users[
                        username
                    ]
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Username ykn Password dogoggora!")


if st.session_state.logged_user is None:
    login_screen()
else:
    user = st.session_state.logged_user

    # SIDEBAR CONTROL
    with st.sidebar:
        st.title("👤 User Profile")
        st.write(f"**Maqaa:** {user['name']}")
        st.write(f"**Ga'ee (Role):** {user['role']}")
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_user = None
            st.rerun()

    # HEADER CAPITAL DASHBOARD
    st.markdown("### 💰 Capital Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("CBE Balance", f"{st.session_state.capital['CBE']:,.2f} ETB")
    c2.metric("CBO Balance", f"{st.session_state.capital['CBO']:,.2f} ETB")
    c3.metric("Cash Balance", f"{st.session_state.capital['Cash']:,.2f} ETB")
    st.markdown("---")

    # 4. ROLE-BASED DASHBOARD ACCESS
    role = user["role"]

    # --- MAKER ROLE ---
    if role == "Maker":
        st.header("📝 Ga'ee Maker (Bakrii)")
        tab1, tab2 = st.tabs(
            ["➕ Maamila Galmeessuu", "💸 Transaction Galmeessuu"]
        )

        with tab1:
            with st.form("add_cust_form"):
                name = st.text_input("Maqaa Guutuu")
                gender = st.selectbox("Saala", ["Dhiira", "Dubartii"])
                age = st.number_input("Umrii", min_value=18, max_value=100, value=25)
                init_bal = st.number_input(
                    "Qarshii Ka'umsaa (ETB)", min_value=0.0, step=100.0
                )
                if st.form_submit_button("Maamila Galmeessi"):
                    if name:
                        cid = f"CUST{len(st.session_state.customers)+1:02d}"
                        st.session_state.customers[cid] = {
                            "name": name,
                            "gender": gender,
                            "age": age,
                            "balance": float(init_bal),
                            "status": "Pending",
                        }
                        st.success(
                            f"✅ Maamilli {name} ({cid}) galmaa'eera. Manager (Mamme) biratti Pending ta'ee jira."
                        )
                        st.rerun()
                    else:
                        st.error("Maaloo maqaa sirriitti galchaa!")

        with tab2:
            active_custs = {
                k: v
                for k, v in st.session_state.customers.items()
                if v["status"] == "Active"
            }
            if not active_custs:
                st.warning("Maamilli Active ta'e hin jiru.")
            else:
                with st.form("tx_entry_form"):
                    tx_type = st.selectbox(
                        "Akaakuu Hojii", ["Deposit", "Withdrawal", "Transfer"]
                    )
                    options = [
                        f"{k} - {v['name']} ({v['balance']:,.2f} ETB)"
                        for k, v in active_custs.items()
                    ]

                    from_c = st.selectbox("Maamila", options)
                    from_id = from_c.split(" - ")[0]

                    to_id = None
                    if tx_type == "Transfer":
                        to_c = st.selectbox("Gara Maamilaatti", options)
                        to_id = to_c.split(" - ")[0]

                    bank = "CBE"
                    if tx_type == "Deposit":
                        bank = st.selectbox("Baankii", ["CBE", "CBO"])

                    amount = st.number_input(
                        "Qarshii (ETB)", min_value=1.0, step=50.0
                    )

                    if st.form_submit_button("Transaction Ergi"):
                        cust_bal = st.session_state.customers[from_id][
                            "balance"
                        ]
                        if (
                            tx_type in ["Withdrawal", "Transfer"]
                            and amount > cust_bal
                        ):
                            st.error(
                                f"🚫 Balance maamilaa gahaa miti! Balance: {cust_bal:,.2f} ETB"
                            )
                        elif (
                            tx_type == "Withdrawal"
                            and amount > st.session_state.capital["Cash"]
                        ):
                            st.error("🚫 Cash Agent gahaa miti!")
                        else:
                            st.session_state.transactions.append(
                                {
                                    "id": len(st.session_state.transactions)
                                    + 1,
                                    "type": tx_type,
                                    "from": from_id,
                                    "to": to_id,
                                    "bank": bank if tx_type == "Deposit" else None,
                                    "amount": float(amount),
                                    "status": "Pending",
                                }
                            )
                            st.success(
                                "✅ Transaction ergameera. Checker (Mahamad) verify gochuu qaba."
                            )
                            st.rerun()

    # --- MANAGER ROLE ---
    elif role == "Manager":
        st.header("👔 Ga'ee Manager (Mamme)")
        st.subheader("Maamila Haaraa Approve Gochuu")
        pending_custs = [
            (k, v)
            for k, v in st.session_state.customers.items()
            if v["status"] == "Pending"
        ]

        if pending_custs:
            for cid, info in pending_custs:
                st.info(
                    f"🆔 **{cid}** | Maqaa: **{info['name']}** | Umrii: {info['age']} | Ka'umsa: {info['balance']:,.2f} ETB"
                )
                if st.button(f"Approve {cid}", key=f"app_{cid}"):
                    st.session_state.customers[cid]["status"] = "Active"
                    st.success(f"✅ Maamilli {info['name']} Approve ta'eera!")
                    st.rerun()
        else:
            st.write("✨ Maamilli Approve ta'uuf eegu hin jiru.")

    # --- CHECKER ROLE ---
    elif role == "Checker":
        st.header("🔍 Ga'ee Checker (Mahamad)")
        st.subheader("Transactions Verify Gochuu")
        pending_tx = [
            t for t in st.session_state.transactions if t["status"] == "Pending"
        ]

        if pending_tx:
            for tx in pending_tx:
                c_name = st.session_state.customers[tx["from"]]["name"]
                st.warning(
                    f"🔢 **#{tx['id']}** | Maamila: **{c_name}** | Type: **{tx['type']}** | Qarshii: **{tx['amount']:,.2f} ETB**"
                )
                if st.button(f"Verify #{tx['id']}", key=f"ver_{tx['id']}"):
                    tx["status"] = "Verified"
                    st.success(f"✅ Transaction #{tx['id']} Verified ta'eera!")
                    st.rerun()
        else:
            st.write("✨ Transaction Verify ta'uuf eegu hin jiru.")

    # --- CEO ROLE ---
    elif role == "CEO":
        st.header("👑 Ga'ee CEO (Kalif)")
        st.subheader("Final Transaction Approval")
        verified_tx = [
            t
            for t in st.session_state.transactions
            if t["status"] == "Verified"
        ]

        if verified_tx:
            for tx in verified_tx:
                c_name = st.session_state.customers[tx["from"]]["name"]
                st.success(
                    f"🔢 **#{tx['id']}** | Maamila: **{c_name}** | Type: **{tx['type']}** | Qarshii: **{tx['amount']:,.2f} ETB**"
                )
                if st.button(f"Approve #{tx['id']}", key=f"ceo_{tx['id']}"):
                    amt = tx["amount"]
                    fid = tx["from"]

                    if tx["type"] == "Deposit":
                        st.session_state.customers[fid]["balance"] += amt
                        st.session_state.capital[tx["bank"]] += amt
                    elif tx["type"] == "Withdrawal":
                        st.session_state.customers[fid]["balance"] -= amt
                        st.session_state.capital["Cash"] -= amt
                    elif tx["type"] == "Transfer":
                        st.session_state.customers[fid]["balance"] -= amt
                        st.session_state.customers[tx["to"]]["balance"] += amt

                    tx["status"] = "Approved"
                    st.success(f"🎉 Transaction #{tx['id']} Approved ta'eera!")
                    st.rerun()
        else:
            st.write("✨ Transaction Approval CEO'f eegu hin jiru.")

    # --- AUDITOR ROLE ---
    elif role == "Auditor":
        st.header("📊 Ga'ee Auditor")
        st.subheader("Reports & Statements")
        cust_id = st.selectbox(
            "Maamila Filadhu", list(st.session_state.customers.keys())
        )
        if cust_id:
            c = st.session_state.customers[cust_id]
            st.write(
                f"**Maqaa:** {c['name']} | **Status:** {c['status']} | **Current Balance:** {c['balance']:,.2f} ETB"
            )

            c_txs = [
                t
                for t in st.session_state.transactions
                if (t["from"] == cust_id or t["to"] == cust_id)
                and t["status"] == "Approved"
            ]
            if c_txs:
                st.dataframe(pd.DataFrame(c_txs), use_container_width=True)
            else:
                st.info("Transaction approved ta'e hin jiru.")

    # 5. GLOBAL CUSTOMER DATABASE TABLE
    st.markdown("---")
    st.subheader("📋 Core Customer Database")
    df_customers = pd.DataFrame.from_dict(
        st.session_state.customers, orient="index"
    )
    st.dataframe(df_customers, use_container_width=True)
