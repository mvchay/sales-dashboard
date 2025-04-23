# 📊 Northwind Sales Dashboard

An end-to-end interactive dashboard built with **Python**, **SQL**, and **Streamlit**, using the classic Northwind dataset. This project includes full data analysis, KPI metrics, charts, drilldown filters, CSV export, and even test coverage for utilities and queries.

---

## ✅ What This Project Covers

1. **🔧 Setup**:
   - Organized project with modules, scripts, and reusable components
   - Virtual environment for clean package management

2. **🗃️ Data**:
   - SQLite version of the Northwind database
   - Includes tables: Products, Orders, Categories, Customers, etc.

3. **📊 Analysis & Features**:
   - Monthly sales trend
   - Top 5 products
   - Revenue by category and country
   - KPI cards (total revenue, top customer, etc.)
   - Drilldown: Country → Category → Top Products
   - CSV export functionality

4. **🧪 Testing**:
   - Reusable `charts.py` for plotting
   - Modular `query_tools.py` for SQL queries
   - Test script (`test_utils.py`) to validate DB connection, queries, and visual outputs

5. **🌐 Deployment**:
   - Ready for live sharing via [Streamlit Cloud](https://streamlit.io/cloud)

---

## 🗂️ Project Structure

```
sales-dashboard/
├── data/                     # Northwind_small.sqlite DB
├── notebooks/                # Optional Jupyter exploration
├── outputs/                  # Exported charts/CSVs
├── scripts/                  # DB connection scripts
│   ├── db_connect.py
│   └── __init__.py
├── streamlit_app/            # Main Streamlit dashboard
│   ├── app.py
│   ├── charts.py
│   ├── query_tools.py
│   └── __init__.py
├── test_utils.py             # Local test suite for utilities
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone & Set Up

```bash
git clone https://github.com/mvchay/sales-dashboard.git
cd sales-dashboard
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

```bash
streamlit run streamlit_app/app.py
```

Open in browser: http://localhost:8501

---

## 🧪 Run Tests

```bash
python test_utils.py
```

---

## 📦 Dataset Source

- [Northwind (SQLite)](https://github.com/jpwhite3/northwind-SQLite3)

---

## 🌍 Streamlit Cloud Deployment

After pushing to GitHub:
- Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
- Deploy with:
  - Repo: `your-username/sales-dashboard`
  - App file: `streamlit_app/app.py`

---

## 📬 Contributions

Feel free to fork and expand this! Ideas:
- Add time filters
- Add customer profiles
- Add product detail pages

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE)
