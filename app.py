import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Personal Finance Tracker", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/finance-tracker',
        'Report a bug': "https://github.com/yourusername/finance-tracker/issues",
        'About': "# Personal Finance Tracker\nA simple app to track your income and expenses."
    }
)

# Add custom CSS
st.markdown("""
<style>
    /* Main title animation */
    .title-animation {
        animation: fadeIn 1.5s ease-in;
    }
    
    /* Card-like containers */
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    
    /* Hover effect for transaction rows */
    .dataframe tbody tr:hover {
        background-color: #f0f2f6 !important;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
        padding: 20px;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #4CAF50;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for transactions
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        columns=['Date', 'Type', 'Category', 'Amount', 'Description']
    )

def main():
    # Wrap title in a div with animation class
    st.markdown('<div class="title-animation"><h1>💰 Personal Finance Tracker</h1></div>', 
                unsafe_allow_html=True)
    
    # Sidebar for adding transactions
    with st.sidebar:
        st.header("Add New Transaction")
        
        # Input fields
        date = st.date_input("Date", datetime.now())
        trans_type = st.selectbox("Type", ["Income", "Expense"])
        
        # Different categories based on transaction type
        if trans_type == "Income":
            categories = ["Salary", "Freelance", "Investments", "Other Income"]
        else:
            categories = ["Food", "Transportation", "Housing", "Utilities", 
                         "Entertainment", "Shopping", "Healthcare", "Other"]
            
        category = st.selectbox("Category", categories)
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        description = st.text_input("Description")
        
        if st.button("Add Transaction"):
            new_transaction = pd.DataFrame({
                'Date': [date],
                'Type': [trans_type],
                'Category': [category],
                'Amount': [amount],
                'Description': [description]
            })
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_transaction], 
                ignore_index=True
            )
            st.success("Transaction added successfully!")

    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("📊 Transaction Summary")
        if not st.session_state.transactions.empty:
            # Calculate total income and expenses
            total_income = st.session_state.transactions[
                st.session_state.transactions['Type'] == 'Income'
            ]['Amount'].sum()
            
            total_expenses = st.session_state.transactions[
                st.session_state.transactions['Type'] == 'Expense'
            ]['Amount'].sum()
            
            balance = total_income - total_expenses
            
            # Wrap metrics in styled containers
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3>Total Income: ${total_income:,.2f}</h3>
                </div>
                <div class="metric-card">
                    <h3>Total Expenses: ${total_expenses:,.2f}</h3>
                </div>
                <div class="metric-card">
                    <h3>Balance: ${balance:,.2f}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Category-wise breakdown
            st.subheader("Category Breakdown")
            category_data = st.session_state.transactions.groupby('Category')['Amount'].sum()
            fig = px.pie(values=category_data.values, names=category_data.index)
            st.plotly_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.subheader("📝 Recent Transactions")
        if not st.session_state.transactions.empty:
            st.dataframe(
                st.session_state.transactions.sort_values('Date', ascending=False),
                hide_index=True
            )
        else:
            st.info("No transactions added yet. Use the sidebar to add transactions!")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
  

