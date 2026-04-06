# Supply Chain Analytics Dashboard

A Python-based data analysis system for supply chain optimization.

## 📊 What This Project Does

Analyzes inventory data to provide actionable insights:
- **Inventory Value Analysis**: Identifies high-value products
- **Stock Level Monitoring**: Alerts when products are running low
- **Demand Forecasting**: Identifies fastest-moving products
- **Supplier Analysis**: Determines critical suppliers

## 📈 Dashboard Features

The visualization dashboard displays:
1. **Inventory Value by Product** - Budget and risk management
2. **Days of Stock** - Stockout prevention alerts
3. **Daily Demand** - Identifies profit drivers
4. **Supplier Value Analysis** - Relationship priorities

## 🔴 Key Insights from Current Data

- **Total Inventory Value**: $95,750
- **Critical Product**: Laptop (only 22.5 days of stock)
- **Most Critical Supplier**: TechSupply Co (44% of total value)
- **Highest Demand**: USB Cable (15 units/day)

## 💻 Technologies Used

- **Python 3.14**
- **Pandas** - Data analysis
- **Matplotlib & Seaborn** - Data visualization

## 🚀 How to Use

1. Ensure you have Python installed
2. Install dependencies: `pip install pandas matplotlib seaborn`
3. Run the analysis:
```
   python visualize_analysis.py
```
4. Dashboard will be saved as `supply_chain_dashboard.png`

## 📁 Files

- `supply_chain.csv` - Sample inventory data
- `inventory_analysis.py` - Basic analysis script
- `advanced_analysis.py` - Advanced metrics and insights
- `visualize_analysis.py` - Dashboard generation
- `supply_chain_dashboard.png` - Generated dashboard

## 📌 Next Steps

- Add real company data
- Implement forecasting models
- Create automated reporting
- Deploy as web dashboard
## SQL Module (SQLite)
Built a supply chain database from scratch and wrote analyst-level queries.

- supply_chain_sql.py — database setup, CREATE tables, INSERT data, basic SELECT
- sql_02_filtering.py — WHERE, AND/OR, ORDER BY
- sql_03_aggregations.py — SUM, AVG, COUNT, GROUP BY, HAVING
- sql_04_joins.py — INNER JOIN across 3 tables (orders, products, suppliers)
- sql_05_analyst_report.py — CASE statements, subqueries, full performance report

Key outputs:
- Stock level classification (Critical / Low / Healthy / Overstocked)
- Supplier performance ranking by total spend and lead time
- Full order report with action flags and supplier speed rating
- Summary: $95,650 total spend across 8 orders, 9.5 day avg lead time
## Author

Kato Vianney- Data Analyst | Supply Chain Analytics Specialist.
