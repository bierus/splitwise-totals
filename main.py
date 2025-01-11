import pandas as pd
import plotly.express as px
import streamlit as st


def main() -> None:
    st.set_page_config(page_title='CSV Data Visualization', layout='wide')
    st.title('CSV Data Visualization App')

    # File uploader for CSV files
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Process the DataFrame
        df = df[:-1]  # Remove the last row
        df = df[df["Category"] != "Payment"]  # Filter out 'Payment' category
        df["Cost"] = df["Cost"].str.strip().astype(float)  # Convert Cost to float
        df["Date"] = pd.to_datetime(df["Date"])  # Convert Date to datetime
        start_year = st.selectbox("Start Year", options=df["Date"].dt.year.unique())
        df = df[df["Date"].dt.year >= start_year]  # Filter for years

        avg_cost_df = df.groupby(by=["Category", df["Date"].dt.year])["Cost"].sum() / 12
        avg_cost_fig = px.bar(avg_cost_df.reset_index(), x="Date", y="Cost", color="Category", height=800, title="Average Monthly Cost by Category")
        st.plotly_chart(avg_cost_fig)

        deepdive_year = st.selectbox("Deep Dive Year", options=df["Date"].dt.year.unique(), index=0)
        year_df = df[df["Date"].dt.year == deepdive_year]

        deepdive_fig = px.pie(year_df, names="Category", values="Cost", title=f"Total Cost in {deepdive_year}", height=800)
        st.plotly_chart(deepdive_fig)

        monthly_cost_fig = px.bar(year_df.groupby(by=df["Date"].dt.month)["Cost"].sum(), y="Cost", title=f"Monthly Cost in {deepdive_year}")
        st.plotly_chart(monthly_cost_fig)


if __name__ == '__main__':
    main()
