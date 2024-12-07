import streamlit as st
import pandas as pd

# Load cleaned data and remove any null values
df = pd.read_csv("cleaned_budget_data.csv").dropna()

# Sidebar Filter for Budget Category
st.sidebar.header("Filter by Budget Category")
selected_category = st.sidebar.multiselect(
    "Select Budget Category", options=df["Budget_Category"].dropna().unique(), default=df["Budget_Category"].dropna().unique()
)

# Apply filter to the data
filtered_df = df[df["Budget_Category"].isin(selected_category)]

# Title and Introduction
st.title(":blue[Financial Data Analytics]")
st.markdown("""
### Analyze India's Budget Allocations
Explore insights into government spending across various ministries.
""")

# Dataset Overview
st.success("Raw Dataset Overview")
st.info("""
The dataset contains detailed information on the budget allocations for different ministries in the Indian government. 
You can filter the data based on budget categories to see specific insights.
""")
st.dataframe(filtered_df)
st.success("Summary Statistics")
st.info(f"**Total Ministries Selected:** {len(filtered_df['Ministry'].unique())}")
st.info(f"**Total Budget (in Cr):** ₹{round(filtered_df['Budget_2023_Total'].sum(), 2)}")

# Key Insights Header
st.header("Key Insights")
st.info("Here are some key insights based on your selections:")

# Top 5 Ministries by Budget Allocation
top_ministries = filtered_df.groupby("Ministry")["Budget_2023_Total"].sum().nlargest(5)
st.success("Top 5 Ministries by Total Budget Allocation")
st.table(top_ministries)

# Ministries with Least Budget Allocation
least_ministries = filtered_df.groupby("Ministry")["Budget_2023_Total"].sum().nsmallest(5)
st.success("Ministries with Least Total Budget Allocation")
st.table(least_ministries)

# Revenue and Capital Budget Metrics
st.success("Total Revenue and Capital Budgets")
st.info(f"**Total Revenue Budget:** ₹{filtered_df['Budget_2023_Revenue'].sum():,.2f} Cr")
st.info(f"**Total Capital Budget:** ₹{filtered_df['Budget_2023_Capital'].sum():,.2f} Cr")

# Revenue and Capital Budget Breakdown by Ministry
st.subheader("Revenue and Capital Budget Breakdown")
st.info("This bar chart shows the distribution of Revenue and Capital Budgets across selected ministries.")
revenue_capital_by_ministry = filtered_df.groupby("Ministry")[['Budget_2023_Revenue', 'Budget_2023_Capital']].sum()
st.bar_chart(revenue_capital_by_ministry)

# Conclusion Section - Dynamic
st.success("Conclusion")

# Dynamic Top Ministry (Largest Budget)
ministry_budget = filtered_df.groupby("Ministry")["Budget_2023_Total"].sum().nlargest(1)
ministry = ministry_budget.index[0]
budget = ministry_budget.values[0]

# Dynamic Least Ministry (Smallest Budget)
least_ministry_budget = filtered_df.groupby("Ministry")["Budget_2023_Total"].sum().nsmallest(1)
least_ministry = least_ministry_budget.index[0]
least_budget = least_ministry_budget.values[0]

st.info(f"""
- The **Top Ministry** with the largest budget allocation is **{ministry}** with a total budget of ₹{budget:,.2f} Cr.
- The **Ministry with the least budget allocation** is **{least_ministry}** with a total budget of ₹{least_budget:,.2f} Cr.
- The **Revenue Budget** represents operational expenses and is ₹{filtered_df['Budget_2023_Revenue'].sum():,.2f} Cr.
- The **Capital Budget** focuses on infrastructure investment and is ₹{filtered_df['Budget_2023_Capital'].sum():,.2f} Cr.
""")
