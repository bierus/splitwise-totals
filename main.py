import pandas as pd
import plotly.express as px
import streamlit as st

# Set up the Streamlit app
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
    df = df[df["Date"].dt.year >= 2022]  # Filter for years >= 2022

    # Create a bar chart using Plotly
    fig = px.bar(
        (df.groupby(by=["Category", df['Date'].dt.year])["Cost"].sum() / 12).reset_index(),
        x="Date", y="Cost", color="Category", height=800)

    # Display the bar chart in Streamlit
    st.plotly_chart(fig)
