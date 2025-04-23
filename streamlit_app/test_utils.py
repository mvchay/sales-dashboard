
import pandas as pd
from query_tools import run_query, get_db_connection
from charts import plot_bar_chart, plot_line_chart

# ✅ Test 1: Basic query should return rows from Product table
def test_basic_product_query():
    df = run_query("SELECT * FROM Product LIMIT 5;")
    assert not df.empty, "❌ Product query returned empty"
    print("✅ test_basic_product_query passed")

# ✅ Test 2: Category revenue aggregation
def test_category_revenue():
    query = '''
    SELECT c.CategoryName, SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
    FROM OrderDetail od
    JOIN Product p ON od.ProductId = p.Id
    JOIN Category c ON p.CategoryId = c.Id
    GROUP BY c.CategoryName;
    '''
    df = run_query(query)
    assert 'CategoryName' in df.columns and 'TotalRevenue' in df.columns, "❌ Columns missing in category revenue result"
    assert not df.empty, "❌ No category revenue data found"
    print("✅ test_category_revenue passed")

# ✅ Test 3: Country revenue chart
def test_country_chart_generation():
    query = '''
    SELECT cu.Country, SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
    FROM OrderDetail od
    JOIN [Order] o ON od.OrderId = o.Id
    JOIN Customer cu ON o.CustomerId = cu.Id
    GROUP BY cu.Country;
    '''
    df = run_query(query)
    chart = plot_bar_chart(df, 'Country', 'TotalRevenue', 'Test Country Chart')
    assert chart is not None, "❌ Failed to generate country chart"
    print("✅ test_country_chart_generation passed")

# ✅ Test 4: Line chart from monthly sales
def test_monthly_sales_line_chart():
    query = '''
    SELECT strftime('%Y-%m', OrderDate) AS Month,
           SUM(UnitPrice * Quantity) AS TotalSales
    FROM OrderDetail od
    JOIN [Order] o ON od.OrderId = o.Id
    GROUP BY Month;
    '''
    df = run_query(query)
    chart = plot_line_chart(df, 'Month', 'TotalSales', 'Test Monthly Sales')
    assert chart is not None, "❌ Failed to generate line chart"
    print("✅ test_monthly_sales_line_chart passed")

# Run all tests
if __name__ == "__main__":
    test_basic_product_query()
    test_category_revenue()
    test_country_chart_generation()
    test_monthly_sales_line_chart()
