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
segmentation_level = st.radio("Choose Segmentation Level", ["First Level", "Second Level", "Third Level"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    # Apply data cleaning and segmentation
    df2 = clean_and_segment_data(df)

    # Display the cleaned and segmented dataset
    st.write("### Cleaned and Segmented Data")
    st.dataframe(df2.head())

    # Data Viz
    st.write("### Data Visualization")

    # First level: Country
    if segmentation_level == "First Level":
        country = df2.groupby('Country')['Clicks'].count().reset_index()
        country.rename(columns={'Clicks': 'Clicks'}, inplace=True)
        country = country.sort_values(by='Clicks', ascending=False)
        st.plotly_chart(px.histogram(country.head(10), x='Country', y='Clicks'))

    # Second level: Main Category
    elif segmentation_level == "Second Level":
        main_category = df2.groupby('Main category')['Clicks'].count().reset_index()
        main_category.rename(columns={'Clicks': 'Clicks'}, inplace=True)
        main_category = main_category.sort_values(by='Clicks', ascending=False)
        st.plotly_chart(px.histogram(main_category.head(10), x='Main category', y='Clicks'))

    # Third level: Sub Category
    elif segmentation_level == "Third Level":
        sub_df = df2.groupby('Sub category')['Clicks'].count().reset_index()
        sub_df.rename(columns={'Clicks': 'Clicks'}, inplace=True)
        sub_df = sub_df.sort_values(by='Clicks', ascending=False)
        st.plotly_chart(px.histogram(sub_df.head(10), x='Sub category', y='Clicks'))
