import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import seaborn as sns
import matplotlib.pyplot as plt

# App Config
st.set_page_config(page_title="E-commerce Sales Dashboard", layout="wide")

# Custom CSS for styling header and footer
st.markdown("""
    <style>
    /* Style metric cards */
    div[data-testid="metric-container"] {
        background-color: #f0f2f6; /* Light grey background */
        border: 1px solid #d0d0d0; /* Light border */
        padding: 10px; /* Spacing */
        border-radius: 10px; /* Rounded corners */
        color: black; /* Text color */
        text-align: center; /* Center alignment */
    }
    footer {visibility: hidden;} /* Hide footer */
    /* Add custom footer */
    #custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        color: black;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
        border-top: 1px solid #d0d0d0;
    }
    /* Header styling */
    #app-header {
        font-family: Arial, sans-serif;
        font-size: 36px;
        font-weight: bold;
        padding: 10px 0;
        text-align: center;
        color: #003366;
        margin-bottom: 0;
    }
    #app-subtitle {
        font-size: 18px;
        color: #555555;
        text-align: center;
        margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("<div id='app-header'>🛒 E-commerce Sales Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div id='app-subtitle'>Analyze your sales and customer data with advanced insights</div>", unsafe_allow_html=True)
st.markdown("---")  # Divider

# File Upload
uploaded_file = st.sidebar.file_uploader("📂 Upload your E-commerce CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file)

        # Validate if the file has data
        if df.empty:
            st.error("❌ The uploaded file is empty. Please upload a valid CSV file.")
            st.stop()

    except pd.errors.EmptyDataError:
        st.error("❌ The uploaded file is empty or invalid. Please upload a valid CSV file.")
        st.stop()

    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {e}")
        st.stop()

    # Data Validation
    required_columns = ['Order Date', 'Sales', 'Profit', 'Quantity']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"❌ Missing columns: {', '.join(missing_columns)}. Please upload a valid file.")
        st.stop()

    # Preprocessing
    df['Order Date'] = pd.to_datetime(df.get('Order Date'), errors='coerce')
    df['Sales'] = pd.to_numeric(df.get('Sales'), errors='coerce')
    df['Profit'] = pd.to_numeric(df.get('Profit'), errors='coerce')
    df['Quantity'] = pd.to_numeric(df.get('Quantity'), errors='coerce')
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)

    # Sidebar Filters
    st.sidebar.header("🔍 Filter")
    date_range = st.sidebar.date_input("📅 Select Date Range", value=[df['Order Date'].min(), df['Order Date'].max()])
    if len(date_range) == 2:
        df = df[(df['Order Date'] >= pd.Timestamp(date_range[0])) & (df['Order Date'] <= pd.Timestamp(date_range[1]))]

    search_customer = st.sidebar.text_input("🔍 Search by Customer Name")
    if search_customer:
        df = df[df['Customer Name'].str.contains(search_customer, case=False, na=False)]

    search_product = st.sidebar.text_input("🔍 Search by Product")
    if search_product:
        df = df[df['Product'].str.contains(search_product, case=False, na=False)]

    regions = df['Region'].dropna().unique() if 'Region' in df.columns else []
    selected_region = st.sidebar.multiselect("🌍 Select Region", regions, default=regions)

    categories = df['Category'].dropna().unique() if 'Category' in df.columns else []
    selected_category = st.sidebar.multiselect("📦 Select Category", categories, default=categories)

    # Apply filters
    filtered_df = df.copy()
    if 'Region' in df.columns and selected_region:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_region)]
    if 'Category' in df.columns and selected_category:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_category)]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your filters.")
        st.stop()

    # Metrics Section
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = filtered_df['Order ID'].nunique() if 'Order ID' in filtered_df.columns else len(filtered_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Total Sales", f"₹{total_sales:,.0f}", help="Total revenue generated from sales")
    col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}", help="Total profit earned")
    col3.metric("🛍️ Total Orders", f"{total_orders}", help="Total number of unique orders")

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview", "Products", "Regions", "Customers", "Visualizations", "Forecasting"])

    # Advanced Visualizations
    with tab1:
        st.subheader("📅 Sales & Profit Trends")
        col1, col2 = st.columns(2)

        with col1:
            sales_trend = filtered_df.groupby('Month')['Sales'].sum().reset_index()
            fig = px.line(sales_trend, x='Month', y='Sales', markers=True, title="Monthly Sales")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            profit_trend = filtered_df.groupby('Month')['Profit'].sum().reset_index()
            fig = px.line(profit_trend, x='Month', y='Profit', markers=True, title="Monthly Profit", color_discrete_sequence=['green'])
            st.plotly_chart(fig, use_container_width=True)

    # Product Analysis
    with tab2:
        st.subheader("📦 Product Analysis")
        product_summary = filtered_df.groupby('Product')[['Sales', 'Profit', 'Quantity']].sum().sort_values(by='Sales', ascending=False)
        st.dataframe(product_summary)

        top_products = product_summary.reset_index().head(10)
        fig = px.bar(top_products, x='Product', y='Sales', title="Top Products by Sales", color='Sales')
        st.plotly_chart(fig, use_container_width=True)

    # Regional Insights
    with tab3:
        if 'Region' in df.columns:
            st.subheader("🌍 Regional Analysis")
            region_summary = filtered_df.groupby('Region')[['Sales', 'Profit']].sum().sort_values(by='Sales', ascending=False)
            st.dataframe(region_summary)

            fig = px.pie(region_summary, names=region_summary.index, values='Sales', title="Sales Distribution by Region")
            st.plotly_chart(fig, use_container_width=True)

    # Customer Dashboard
    with tab4:
        if 'Customer Name' in df.columns:
            st.subheader("👤 Customer Analysis")
            customer_summary = filtered_df.groupby('Customer Name')[['Sales', 'Profit']].sum().sort_values(by='Sales', ascending=False)
            st.dataframe(customer_summary.head(10))

            # Add a bar chart for top customers
            top_customers = customer_summary.reset_index().head(10)
            fig = px.bar(top_customers, x='Customer Name', y='Sales', title="Top Customers by Sales", color='Sales')
            st.plotly_chart(fig, use_container_width=True)

    # Additional Visualizations
    with tab5:
        st.subheader("📊 Additional Visualizations")
        scatter_fig = px.scatter(filtered_df, x='Sales', y='Profit', color='Category', title="Sales vs Profit by Category")
        st.plotly_chart(scatter_fig, use_container_width=True)

        correlation_matrix = filtered_df[['Sales', 'Profit', 'Quantity']].corr()
        st.write("### Correlation Matrix")
        fig, ax = plt.subplots()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # Forecasting
    with tab6:
        st.subheader("📈 Sales Forecasting")
        if 'Sales' in filtered_df.columns:
            # Resample data to monthly sales
            sales_data = filtered_df[['Order Date', 'Sales']].set_index('Order Date').resample('M').sum()

            if len(sales_data) >= 24:  # Ensure at least 24 months of data for a 12-month seasonal period
                model = ExponentialSmoothing(sales_data['Sales'], seasonal='add', seasonal_periods=12).fit()
                forecast = model.forecast(steps=6)
                st.line_chart(forecast)
            elif len(sales_data) >= 6:  # Use simpler model for at least 6 months of data
                model = ExponentialSmoothing(sales_data['Sales'], trend='add', seasonal=None).fit()
                forecast = model.forecast(steps=6)
                st.line_chart(forecast)
                st.warning("⚠️ Using non-seasonal forecasting due to insufficient data for seasonal analysis.")
            else:
                st.warning("⚠️ Not enough data to generate a forecast. Please upload a dataset with more records.")
        else:
            st.error("❌ Sales data is missing in the dataset. Please upload a valid file.")

    # Download Summary
    st.sidebar.header("📥 Download Summary")
    summary = filtered_df.groupby('Product')[['Sales', 'Profit']].sum().sort_values(by='Sales', ascending=False)
    st.sidebar.download_button("Download Product Summary CSV", data=summary.to_csv().encode(), file_name="summary.csv", mime='text/csv')

else:
    st.info("Please upload a CSV file to start the dashboard analysis.")

# Footer
st.markdown(
    """
    <style>
        #custom-footer {
            font-size: 14px;
            color: #666;
            text-align: center;
            margin-top: 50px;
            padding: 10px;
            border-top: 1px solid #ddd;
        }
        #custom-footer a {
            color: #0073e6;
            text-decoration: none;
            font-weight: bold;
        }
        #custom-footer a:hover {
            text-decoration: underline;
        }
        #custom-footer .team {
            display: flex;
            justify-content: center;
            gap: 3px;
        }
    </style>
    <div id='custom-footer'>
        <div class="team">
            Developed by<a href='https://www.linkedin.com/in/im-mayankverma/' target='_blank'>Mayank</a>
        </div>
        <div>
            <span>© 2025. All rights reserved.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
