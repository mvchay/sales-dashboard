import streamlit as st
import sqlite3
import pandas as pd
import os

# Fix path using project root relative to this file's location
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'Northwind_small.sqlite'))
conn = sqlite3.connect(DB_PATH)

st.set_page_config(page_title="Northwind Sales Dashboard", layout="wide")

st.title("📊 Northwind Sales Dashboard")
st.markdown("Analyze revenue by month, product, category, and region.")

# --- KPI Queries ---

# Total Revenue
total_revenue = pd.read_sql_query("""
SELECT SUM(UnitPrice * Quantity) AS Revenue
FROM OrderDetail;
""", conn).iloc[0, 0]

# Total Orders
total_orders = pd.read_sql_query("SELECT COUNT(*) AS TotalOrders FROM [Order];", conn).iloc[0, 0]

# Total Customers
total_customers = pd.read_sql_query("SELECT COUNT(DISTINCT Id) AS TotalCustomers FROM Customer;", conn).iloc[0, 0]

# Top Customer
top_customer = pd.read_sql_query("""
SELECT cu.ContactName, SUM(od.UnitPrice * od.Quantity) AS TotalSpent
FROM OrderDetail od
JOIN [Order] o ON od.OrderId = o.Id
JOIN Customer cu ON o.CustomerId = cu.Id
GROUP BY cu.ContactName
ORDER BY TotalSpent DESC
LIMIT 1;
""", conn)

top_customer_name = top_customer.iloc[0]['ContactName']
top_customer_value = top_customer.iloc[0]['TotalSpent']

# --- KPI Cards ---
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("🧾 Total Orders", f"{total_orders}")
col3.metric("👥 Total Customers", f"{total_customers}")
col4.metric("🏆 Top Customer", f"{top_customer_name}", f"${top_customer_value:,.2f}")


# Sidebar filters (we can add more later)
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select a Country", ["All"] + sorted(pd.read_sql("SELECT DISTINCT Country FROM Customer", conn)['Country'].tolist()))

# -------------------------------
# 🔍 Drilldown View Section
# -------------------------------



# Step 1: Category Revenue (Filtered by Country)
query_drill_category = f"""
SELECT 
    c.CategoryName,
    SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
FROM 
    OrderDetail od
JOIN 
    [Order] o ON od.OrderId = o.Id
JOIN 
    Customer cu ON o.CustomerId = cu.Id
JOIN 
    Product p ON od.ProductId = p.Id
JOIN 
    Category c ON p.CategoryId = c.Id
{"WHERE cu.Country = '" + selected_country + "'" if selected_country != "All" else ""}
GROUP BY 
    c.CategoryName
ORDER BY 
    TotalRevenue DESC;
"""

drill_cat_df = pd.read_sql_query(query_drill_category, conn)



st.markdown(f"### 📦 Category Revenue {'🌍 All Countries' if selected_country == 'All' else f'🇨🇭 {selected_country} Only'}")
st.bar_chart(drill_cat_df.set_index('CategoryName'))

#Drill Down
st.markdown("## 🔍 Drilldown View: Country → Category → Products")
selected_category = st.selectbox("Select a Category", drill_cat_df['CategoryName'])

# Step 2: Top Products in Selected Category & Country
query_drill_products = f"""
SELECT 
    p.ProductName,
    SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
FROM 
    OrderDetail od
JOIN 
    [Order] o ON od.OrderId = o.Id
JOIN 
    Customer cu ON o.CustomerId = cu.Id
JOIN 
    Product p ON od.ProductId = p.Id
JOIN 
    Category c ON p.CategoryId = c.Id
WHERE 
    c.CategoryName = '{selected_category}'
    {"AND cu.Country = '" + selected_country + "'" if selected_country != "All" else ""}
GROUP BY 
    p.ProductName
ORDER BY 
    TotalRevenue DESC
LIMIT 10;
"""

drill_prod_df = pd.read_sql_query(query_drill_products, conn)

st.markdown(f"### 🧾 Top Products in '{selected_category}' ({selected_country if selected_country != 'All' else 'All Countries'})")
st.bar_chart(drill_prod_df.set_index('ProductName'))


# Sample query (monthly sales)
query = """
SELECT strftime('%Y-%m', OrderDate) AS Month, 
       SUM(UnitPrice * Quantity) AS TotalSales
FROM OrderDetail od
JOIN [Order] o ON od.OrderId = o.Id
GROUP BY Month
ORDER BY Month;
"""
monthly_df = pd.read_sql_query(query, conn)

# Line chart for Monthly Sales
st.subheader("📈 Monthly Total Sales")
st.line_chart(monthly_df.set_index('Month'))

#Montly Sales Download Button
st.download_button(
    label="⬇️ Download Monthly Sales CSV",
    data=monthly_df.to_csv(index=False),
    file_name='monthly_sales.csv',
    mime='text/csv'
)


# Top 5 Best-Selling Products
st.subheader("🔥 Top 5 Best-Selling Products")

query_top_products = """
SELECT 
    p.ProductName,
    SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
FROM 
    OrderDetail od
JOIN 
    Product p ON od.ProductId = p.Id
GROUP BY 
    p.ProductName
ORDER BY 
    TotalRevenue DESC
LIMIT 5;
"""

top_products_df = pd.read_sql_query(query_top_products, conn)
st.bar_chart(top_products_df.set_index('ProductName'))

# Top Products Download Button
st.download_button(
    label="⬇️ Download Top Products CSV",
    data=top_products_df.to_csv(index=False),
    file_name='top_products.csv',
    mime='text/csv'
)


# Revenue by Product Category
st.subheader("📦 Revenue by Product Category")

query_category_sales = """
SELECT 
    c.CategoryName,
    SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
FROM 
    OrderDetail od
JOIN 
    Product p ON od.ProductId = p.Id
JOIN 
    Category c ON p.CategoryId = c.Id
GROUP BY 
    c.CategoryName
ORDER BY 
    TotalRevenue DESC;
"""

cat_df = pd.read_sql_query(query_category_sales, conn)
st.bar_chart(cat_df.set_index('CategoryName'))

#Category Sales Download Button
st.download_button(
    label="⬇️ Download Category Sales CSV",
    data=cat_df.to_csv(index=False),
    file_name='category_sales.csv',
    mime='text/csv'
)


# Revenue by Country (with Filter)
st.subheader("🌍 Revenue by Country")

# Adjust SQL if a country is selected
if selected_country != "All":
    query_country = f"""
    SELECT cu.Country, SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
    FROM OrderDetail od
    JOIN [Order] o ON od.OrderId = o.Id
    JOIN Customer cu ON o.CustomerId = cu.Id
    WHERE cu.Country = '{selected_country}'
    GROUP BY cu.Country;
    """
else:
    query_country = """
    SELECT cu.Country, SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
    FROM OrderDetail od
    JOIN [Order] o ON od.OrderId = o.Id
    JOIN Customer cu ON o.CustomerId = cu.Id
    GROUP BY cu.Country
    ORDER BY TotalRevenue DESC;
    """

country_df = pd.read_sql_query(query_country, conn)
st.bar_chart(country_df.set_index('Country'))

#Country Revenue Download Button
st.download_button(
    label=f"⬇️ Download Revenue by {'Selected Country' if selected_country != 'All' else 'All Countries'}",
    data=country_df.to_csv(index=False),
    file_name='country_sales.csv',
    mime='text/csv'
)


conn.close()
