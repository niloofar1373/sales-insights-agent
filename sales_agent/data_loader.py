import os
import pandas as pd
from google.genai import types

# Resolve the dataset path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
csv_path = os.path.join(parent_dir, "data.csv")

print(f"Loading dataset from: {csv_path}...")
df = pd.read_csv(csv_path, encoding='ISO-8859-1')

# Preprocessing: convert dates and compute revenue
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce').fillna(0.0).astype(float)
df['Revenue'] = df['Quantity'] * df['UnitPrice']
print("Dataset loaded and preprocessed successfully.")

def get_dataset_summary() -> str:
    """Get general details about the transactional sales dataset.
    
    Returns a string containing the number of transactions, number of unique customers,
    date range covered, total revenue, and overall unique products.
    """
    num_transactions = df['InvoiceNo'].nunique()
    num_customers = df['CustomerID'].nunique(dropna=True)
    num_products = df['StockCode'].nunique()
    total_rev = df['Revenue'].sum()
    min_date = df['InvoiceDate'].min()
    max_date = df['InvoiceDate'].max()
    
    return (
        f"Dataset Summary:\n"
        f"- Total Transactions (InvoiceNo): {num_transactions:,}\n"
        f"- Unique Customers: {num_customers:,}\n"
        f"- Unique Products (StockCode): {num_products:,}\n"
        f"- Total Revenue: ${total_rev:,.2f}\n"
        f"- Date Range: {min_date.strftime('%Y-%m-%d') if not pd.isnull(min_date) else 'N/A'} "
        f"to {max_date.strftime('%Y-%m-%d') if not pd.isnull(max_date) else 'N/A'}"
    )

def get_top_products(n: int = 5) -> str:
    """Retrieve the top products by quantity sold and revenue.
    
    Args:
        n: The number of top products to retrieve (default is 5).
    """
    prod_grouped = df.groupby('Description').agg(
        quantity_sold=('Quantity', 'sum'),
        total_revenue=('Revenue', 'sum')
    ).reset_index()
    
    top_by_qty = prod_grouped.sort_values(by='quantity_sold', ascending=False).head(n)
    top_by_rev = prod_grouped.sort_values(by='total_revenue', ascending=False).head(n)
    
    result = f"Top {n} Products by Quantity Sold:\n"
    for idx, row in top_by_qty.iterrows():
        result += f"- {row['Description']}: {row['quantity_sold']:,} units sold\n"
        
    result += f"\nTop {n} Products by Revenue:\n"
    for idx, row in top_by_rev.iterrows():
        result += f"- {row['Description']}: ${row['total_revenue']:,.2f} revenue\n"
        
    return result

def get_top_customers(n: int = 5) -> str:
    """Retrieve the top customers by total spending/revenue.
    
    Args:
        n: The number of top customers to retrieve (default is 5).
    """
    cust_grouped = df[df['CustomerID'].notnull()].groupby('CustomerID').agg(
        total_spent=('Revenue', 'sum'),
        transaction_count=('InvoiceNo', 'nunique')
    ).reset_index()
    
    top_cust = cust_grouped.sort_values(by='total_spent', ascending=False).head(n)
    
    result = f"Top {n} Customers by Total Spending:\n"
    for idx, row in top_cust.iterrows():
        result += f"- Customer ID {int(row['CustomerID'])}: ${row['total_spent']:,.2f} (Transactions: {row['transaction_count']:,})\n"
        
    return result

def get_sales_by_country() -> str:
    """Retrieve sales and revenue breakdown by country."""
    country_grouped = df.groupby('Country').agg(
        total_revenue=('Revenue', 'sum'),
        transaction_count=('InvoiceNo', 'nunique')
    ).reset_index()
    
    top_countries = country_grouped.sort_values(by='total_revenue', ascending=False)
    
    result = "Sales Breakdown by Country:\n"
    for idx, row in top_countries.iterrows():
        result += f"- {row['Country']}: ${row['total_revenue']:,.2f} (Transactions: {row['transaction_count']:,})\n"
        
    return result

def query_sales_by_date_range(start_date: str, end_date: str) -> str:
    """Retrieve aggregate sales metrics within a specific date range.
    
    Args:
        start_date: Start date string formatted as YYYY-MM-DD.
        end_date: End date string formatted as YYYY-MM-DD.
    """
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
    except Exception as e:
        return f"Error: Invalid date format. Please use YYYY-MM-DD. Details: {e}"
        
    filtered_df = df[(df['InvoiceDate'] >= start) & (df['InvoiceDate'] <= end)]
    
    if filtered_df.empty:
        return f"No sales data found between {start_date} and {end_date}."
        
    total_rev = filtered_df['Revenue'].sum()
    units_sold = filtered_df['Quantity'].sum()
    unique_cust = filtered_df['CustomerID'].nunique(dropna=True)
    transactions = filtered_df['InvoiceNo'].nunique()
    
    return (
        f"Sales from {start_date} to {end_date}:\n"
        f"- Total Revenue: ${total_rev:,.2f}\n"
        f"- Quantity Sold: {units_sold:,} units\n"
        f"- Unique Customers: {unique_cust:,}\n"
        f"- Transactions: {transactions:,}"
    )

def search_products(search_term: str) -> str:
    """Search for products by name/description and show their sales summary.
    
    Args:
        search_term: The search query string (case-insensitive).
    """
    filtered_df = df[df['Description'].astype(str).str.contains(search_term, case=False, na=False)]
    
    if filtered_df.empty:
        return f"No products found matching '{search_term}'."
        
    prod_grouped = filtered_df.groupby('Description').agg(
        quantity_sold=('Quantity', 'sum'),
        total_revenue=('Revenue', 'sum')
    ).reset_index()
    
    top_matches = prod_grouped.sort_values(by='total_revenue', ascending=False).head(10)
    
    result = f"Top matching products for '{search_term}':\n"
    for idx, row in top_matches.iterrows():
        result += f"- {row['Description']}: ${row['total_revenue']:,.2f} revenue ({row['quantity_sold']:,} units sold)\n"
        
    return result

def draft_insights_report(topic: str = None, start_date: str = None, end_date: str = None) -> str:
    """Draft a sales insights or analysis report directly.
    
    This tool should be used when the user asks for an insights report or analysis report.
    It drafts a report containing a trend summary, key findings, and recommended actions.
    
    Args:
        topic: A product category or search term to focus the report on (optional).
        start_date: Start date string formatted as YYYY-MM-DD (optional).
        end_date: End date string formatted as YYYY-MM-DD (optional).
    """
    # 1. Gather numbers
    filtered_df = df
    date_desc = "All Time"
    
    if start_date or end_date:
        try:
            if start_date:
                start = pd.to_datetime(start_date)
                filtered_df = filtered_df[filtered_df['InvoiceDate'] >= start]
            if end_date:
                end = pd.to_datetime(end_date)
                filtered_df = filtered_df[filtered_df['InvoiceDate'] <= end]
            date_desc = f"{start_date or 'Start'} to {end_date or 'End'}"
        except Exception as e:
            return f"Error parsing dates: {e}"
            
    if topic:
        filtered_df = filtered_df[filtered_df['Description'].astype(str).str.contains(topic, case=False, na=False)]
        topic_desc = f"Focus Topic: '{topic}'"
    else:
        topic_desc = "All Categories"
        
    if filtered_df.empty:
        return f"No sales data found matching Topic: '{topic}' and Date Range: {date_desc}."
        
    total_rev = filtered_df['Revenue'].sum()
    units_sold = filtered_df['Quantity'].sum()
    unique_cust = filtered_df['CustomerID'].nunique(dropna=True)
    transactions = filtered_df['InvoiceNo'].nunique()
    
    # Get top products for the filtered dataset
    prod_grouped = filtered_df.groupby('Description').agg(
        quantity_sold=('Quantity', 'sum'),
        total_revenue=('Revenue', 'sum')
    ).reset_index()
    top_products_df = prod_grouped.sort_values(by='total_revenue', ascending=False).head(3)
    
    # Build Top Products Markdown Table
    if top_products_df.empty:
        top_products_table = "*No products found.*"
    else:
        top_products_table = "| Product | Revenue | Units Sold |\n| :--- | :--- | :--- |\n"
        for idx, row in top_products_df.iterrows():
            top_products_table += f"| {row['Description']} | ${row['total_revenue']:,.2f} | {row['quantity_sold']:,} |\n"
        
    # Get top countries for the filtered dataset
    country_grouped = filtered_df.groupby('Country').agg(
        total_revenue=('Revenue', 'sum'),
        transaction_count=('InvoiceNo', 'nunique')
    ).reset_index()
    top_countries_df = country_grouped.sort_values(by='total_revenue', ascending=False).head(3)
    
    # Build Top Countries Markdown Table
    if top_countries_df.empty:
        top_countries_table = "*No countries found.*"
        top_countries_str = "None"
    else:
        top_countries_table = "| Country | Revenue | Transactions |\n| :--- | :--- | :--- |\n"
        for idx, row in top_countries_df.iterrows():
            top_countries_table += f"| {row['Country']} | ${row['total_revenue']:,.2f} | {row['transaction_count']:,} |\n"
        top_countries_str = ", ".join(top_countries_df['Country'].tolist())
    
    # 2. Draft the report
    draft = (
        f"# Sales Insights & Analysis Report\n"
        f"**Scope**: {topic_desc} | **Date Range**: {date_desc}\n\n"
        f"## 1. Trend Summary\n"
        f"- **Total Revenue**: ${total_rev:,.2f}\n"
        f"- **Units Sold**: {units_sold:,} units\n"
        f"- **Transactions**: {transactions:,} orders\n"
        f"- **Unique Customers**: {unique_cust:,} customers\n"
        f"- **Average Order Value**: ${total_rev / transactions:,.2f}\n\n"
        f"## 2. Key Findings\n"
        f"### Top Performing Products\n\n"
        f"{top_products_table}\n\n"
        f"### Top Countries\n\n"
        f"{top_countries_table}\n\n"
        f"## 3. Recommended Business Actions\n"
    )
    
    if topic:
        draft += (
            f"1. **Inventory Management**: Ensure sufficient stock of the top performing '{topic}' items to prevent stockouts.\n"
            f"2. **Targeted Campaigns**: Run promotional campaigns for '{topic}' specifically in top countries.\n"
        )
    else:
        draft += (
            f"1. **High-Value Customer Outreach**: Design exclusive VIP retention programs targeting top-spending customers.\n"
            f"2. **Geographical Expansion**: Focus marketing efforts and logistics optimization on key countries: {top_countries_str}.\n"
        )
        
    draft += (
        f"3. **Pricing Review**: Review unit prices of low-volume, high-revenue products to optimize margins.\n"
    )
    
    return draft

def finalize_insights_report(report_text: str) -> str:
    """Finalize the approved or edited insights report.
    
    Use this tool only after the user has explicitly approved or provided edits to the draft report.
    
    Args:
        report_text: The finalized report text (approved draft or edited version).
    """
    return (
        f"### [APPROVED & FINALIZED REPORT]\n\n"
        f"{report_text}\n\n"
        f"*Report approved and finalized by human reviewer.*"
    )


