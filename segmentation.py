import streamlit as st
import pandas as pd
import plotly.express as px

# Function to apply data cleaning and segmentation
def clean_and_segment_data(df):
    # Data cleaning
    filter_page = ['category', '#', 'blog', 'tag', 'author', 'wp-content', 'upload', 'Page', 'feed', 'legal', 'contact', 'sitemap', 'wp-login', 'wp-admin']
    df_cleaned = df[~df['Page'].str.contains("|".join(filter_page))]
    df_cleaned = df_cleaned[df_cleaned['Page'].map(lambda x: x.isascii())]

    # Segmentation
    df_cleaned['Country'] = df_cleaned['Page'].str.split('/').str[3]
    df_cleaned['Main category'] = df_cleaned['Page'].str.split('/').str[4]
    df_cleaned['Sub category'] = df_cleaned['Page'].str.split('/').str[5]
    df_cleaned['Main category'] = df_cleaned['Main category'].fillna('Homepage')

    return df_cleaned

# Streamlit App
st.title("Clicks Data Analysis")

# Upload dataset
uploaded_file = st.file_uploader("Upload file (CSV or XLSX)", type=["csv", "xlsx"])

# Choose segmentation level
segmentation_level = st.selectbox("Choose Segmentation Level", ["Country", "Main category", "Sub category"])

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

        # Apply data cleaning and segmentation
        df2 = clean_and_segment_data(df)

        # Display the cleaned and segmented dataset
        st.write("### Cleaned and Segmented Data")
        st.dataframe(df2.head())

        # Data Viz
        st.write("### Data Visualization")

        # Segmentation based on user choice
        segmented_df = df2.groupby(segmentation_level)['Clicks'].count().reset_index()
        segmented_df.rename(columns={'Clicks': 'Clicks'}, inplace=True)
        segmented_df = segmented_df.sort_values(by='Clicks', ascending=False)

        # Display segmented data
        st.write(f"#### {segmentation_level} Segmentation")
        st.dataframe(segmented_df.head())

        # Bar chart
        st.write(f"#### Bar Chart - {segmentation_level} Segmentation")
        st.plotly_chart(px.bar(segmented_df.head(10), x=segmentation_level, y='Clicks', labels={'Clicks': 'Clicks Count'}))
except KeyError as e:
    st.error(f"Error: {e}. Please choose a valid segmentation level.")
