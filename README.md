# E-commerce Sales and Customer Dashboard

![Dashboard Preview](dashboard.png)

Analyze e-commerce sales and customer data with interactive filters, product/category breakdowns, and exportable summaries.

## Features
- **Upload CSV**: Drag-and-drop or browse (<=200 MB).
- **Filters**: Date range, customer name, product, region, and category.
- **KPIs**: Total Sales, Total Profit, Total Orders.
- **Visuals**: Monthly Sales and Monthly Profit trends; tabs for Products, Regions, Customers, Visualizations, and Forecasting.
- **Exports**: Download product summary CSV.

## Tech Stack
- Python (100%)
- Streamlit (UI), Pandas (data), Plotly/Matplotlib (charts) — adjust if different.

## Getting Started
1. **Clone**
   ```bash
   git clone https://github.com/im-mayankverma/E-Commerce-Sales-and-Customer-Dashboard.git
   cd E-Commerce-Sales-and-Customer-Dashboard
   ```
2. **Set up environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Run app**
   ```bash
   streamlit run app.py  # update entrypoint if different
   ```
4. **Use it**
   - Upload your e-commerce CSV.
   - Apply filters (date, customer, product, region, category).
   - View KPIs and charts; download summaries.

## Data Expectations
- CSV with columns like: `order_date`, `customer_name`, `product`, `category`, `region`, `sales`, `profit`, `orders` (customize to your schema).
- Ensure dates parse correctly; align column names with the app’s code if different.

## Project Structure
- `app.py` — Streamlit app entrypoint.
- `requirements.txt` — Python dependencies.
- `sample_sales_data.csv` — Example dataset (if included).
- Add more sections as needed (e.g., `src/`, `data/`, `assets/`).

## Configuration
- Default settings in `app.py` (filters, date formats, currency).
- Environment variables (if any): document them here.

## Troubleshooting
- **Large file**: keep under 200 MB; sample smaller slices if needed.
- **Date parsing**: ensure consistent date format in CSV.
- **Missing columns**: align CSV headers with expected schema.

## Roadmap / Ideas
- Add more visualizations (category mix, cohort retention, RFM).
- Forecasting enhancements.
- Theming and localization.
- CI for linting/tests.

## Author
Developed by Mayank (@im-mayankverma).
