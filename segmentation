import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import plotly.express as px

# Load data from uploaded file
def load_data(file):
    if file is not None:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            st.error("Invalid file format. Please upload a CSV or XLSX file.")
            return None
        return df
    return None

# Perform data processing and visualization
def process_and_visualize_data(df):
    if df is not None:
        # Data cleaning
        df = df[df['Page'].map(lambda x: x.isascii())]

        # Segmentation
        df['Parent category'] = df['Page'].str.split('/').str[3]
        df['sub category'] = df['Page'].str.split('/').str[4]
        df.fillna('Homepage', inplace=True)
        df.to_excel('segmentation.xlsx', index=False)

        # Data viz
        parent_df = df['Parent category'].value_counts().reset_index()
        parent_df.columns = ['Parent category', 'Count']
        sub_df = df['sub category'].value_counts().reset_index()
        sub_df.columns = ['sub category', 'Count']

        # Plot most frequent categories
        st.markdown("### Top 10 Parent Categories")
        st.plotly_chart(px.histogram(parent_df.head(10), x='Parent category', y='Count'))

        st.markdown("### Top 10 Sub Categories")
        st.plotly_chart(px.histogram(sub_df.head(10), x='sub category', y='Count'))

# Streamlit UI
st.title("Page Template Segmentation and Visualization")

# Upload CSV or Excel file
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

# Process and visualize data on button click
if st.button("Process and Visualize Data") and uploaded_file is not None:
    # Load data
    data = load_data(uploaded_file)
    
    # Process and visualize data
    process_and_visualize_data(data)
