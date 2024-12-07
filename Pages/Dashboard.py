import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("cleaned_budget_data.csv")

# Streamlit app
st.title("Data Visualization")

st.success("Expenses which bring a change to the government’s assets or liabilities (such as construction of roads or recovery of loans) are :orange[capital expenses], and all other expenses are :blue[revenue expenses] (such as payment of salaries or interest payments).")

# Filters
st.sidebar.header("Filters")

# Group Filter (Choose between Ministry or Budget Category)
group_filter = st.sidebar.radio("Choose Filter Type:", ["Ministry", "Budget Category"])

# Apply Filtering
if group_filter == "Ministry":
    selected_ministry = st.sidebar.multiselect("Select Ministry", options=df["Ministry"].unique())
    if not selected_ministry:
        selected_ministry = df["Ministry"].unique()
    filtered_df = df[df["Ministry"].isin(selected_ministry)]
    group_col = "Ministry"
else:
    selected_Budget_Category = st.sidebar.multiselect("Select Budget Category", options=df["Budget_Category"].unique())
    if not selected_Budget_Category:
        selected_Budget_Category = df["Budget_Category"].unique()
    filtered_df = df[df["Budget_Category"].isin(selected_Budget_Category)]
    group_col = "Budget_Category"

# Grouped Data
grouped_df = filtered_df.groupby(group_col).agg(
    Total_Budget=("Budget_2023_Total", "sum"),
    Capital_Budget=("Budget_2023_Capital", "sum"),
    Revenue_Budget=("Budget_2023_Revenue", "sum")
).reset_index()

# Charts
st.info(f"Total Budget Analysis by **{group_filter}**")
if group_filter == "Ministry":
    st.info(f"Total Budget of Ministries **(Selected Ministries: {len(selected_ministry)})**")
else:
    st.info(f"Total Budget of Budget Categories **(Selected Categories: {len(selected_Budget_Category)})**")


# Sunburst Chart
if group_filter == "Ministry":
    fig = px.sunburst(filtered_df, path=["Ministry", "Budget_Category"], values="Budget_2023_Total", title="Budget Breakdown by Ministry and Category", color="Budget_2023_Total")
else:
    fig = px.sunburst(filtered_df, path=["Budget_Category", "Ministry"], values="Budget_2023_Total", title="Budget Breakdown by Category and Ministry", color="Budget_2023_Total")
st.plotly_chart(fig)

st.markdown("---")

# Revenue vs. Capital Budget Scatter Plot
if group_filter == "Ministry":
    st.info(f"Total Budget of Ministries **(Selected Ministries: {len(selected_ministry)})**")
else:
    st.info(f"Total Budget of Budget Categories **(Selected Categories: {len(selected_Budget_Category)})**")

fig = px.scatter(grouped_df, x="Revenue_Budget", y="Capital_Budget", color=group_col, title=f"Revenue vs. Capital Budget by {group_filter}")
st.plotly_chart(fig)

st.markdown("---")

# Budget Distribution Pie Chart

if group_filter == "Ministry":
    st.info(f"Top **{min(10, len(grouped_df['Ministry'].unique()))}** Ministries by Total Budget")
else:
    st.info(f"Total Budget of Budget Categories **(Selected Categories: {len(selected_Budget_Category)})**")

top_10 = grouped_df.nlargest(10, "Total_Budget")
fig = px.pie(top_10, names=group_col, values="Total_Budget", title=f"Total Budget Distribution by {group_filter}")
st.plotly_chart(fig)

st.markdown("---")

# Revenue and Capital Bar Chart

if group_filter == "Ministry":
    st.info(f"Total Budget of Ministries **(Selected Ministries: {len(selected_ministry)})**")
else:
    st.info(f"Total Budget of Budget Categories **(Selected Categories: {len(selected_Budget_Category)})**")
 

fig = px.bar(grouped_df, x=group_col, y=["Revenue_Budget", "Capital_Budget"], title=f"Revenue and Capital Budgets by {group_filter}", barmode="stack")
st.plotly_chart(fig)

st.markdown("---")

# Top 10 Entities by Total Budget

if group_filter == "Ministry":
    st.info(f"Total Budget of Ministries **(Selected Ministries: {len(selected_ministry)})**")
else:
    st.info(f"Total Budget of Budget Categories **(Selected Categories: {len(selected_Budget_Category)})**")
  

top_10 = grouped_df.nlargest(10, "Total_Budget")
fig = px.bar(top_10, x=group_col, y="Total_Budget", title=f"Top {group_filter} by Total Budget", labels={"Total_Budget": "Total Budget (₹)"})
st.plotly_chart(fig)

st.markdown("---")

# Total Budget Revenue of Ministries
st.info(f"Total Budget **Revenue** of Ministries **(Top 10 Ministries)**")
top_10_Revenue = df.groupby("Ministry")["Budget_2023_Revenue"].sum().nlargest(10).reset_index()
fig = px.pie(top_10_Revenue, names="Ministry", values="Budget_2023_Revenue", title="Total Budget Revenue of Top 10 Ministries")
st.plotly_chart(fig)

st.markdown("---")

# Total Budget Capital of Ministries (Top 10)
st.info(f"Total Budget **Capital** of Ministries **(Top 10 Ministries)**")
top_10_capital = df.groupby("Ministry")["Budget_2023_Capital"].sum().nlargest(10).reset_index()
fig = px.pie(top_10_capital, names="Ministry", values="Budget_2023_Capital", title="Total Budget Capital of Top 10 Ministries")
st.plotly_chart(fig)

st.markdown("---")

# Conclusions
st.info("**📌 Conclusions**")

# Highest Budget Entity
highest_entity = grouped_df[group_col].iloc[grouped_df["Total_Budget"].idxmax()]
highest_budget = grouped_df["Total_Budget"].max()
highest_capital = grouped_df["Capital_Budget"].iloc[grouped_df["Total_Budget"].idxmax()]
highest_revenue = grouped_df["Revenue_Budget"].iloc[grouped_df["Total_Budget"].idxmax()]

st.success(f"🔸 **Highest {group_filter}**: **{highest_entity}**")
st.text(f"Total Budget: ₹{highest_budget:,.2f}")
st.text(f"Capital Budget: ₹{highest_capital:,.2f}")
st.text(f"Revenue Budget: ₹{highest_revenue:,.2f}")

# Lowest Budget Entity
lowest_entity = grouped_df[group_col].iloc[grouped_df["Total_Budget"].idxmin()]
lowest_budget = grouped_df["Total_Budget"].min()
lowest_capital = grouped_df["Capital_Budget"].iloc[grouped_df["Total_Budget"].idxmin()]
lowest_revenue = grouped_df["Revenue_Budget"].iloc[grouped_df["Total_Budget"].idxmin()]

st.warning(f"🔹 **Lowest {group_filter}**: **{lowest_entity}**")
st.text(f"Total Budget: ₹{lowest_budget:,.2f}")
st.text(f"Capital Budget: ₹{lowest_capital:,.2f}")
st.text(f"Revenue Budget: ₹{lowest_revenue:,.2f}")

# Footer
st.sidebar.info("Use the filters to customize the charts!")

st.markdown("---")
st.info("Built with Streamlit and Plotly.")
