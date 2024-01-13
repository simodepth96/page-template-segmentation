import streamlit as st
import pandas as pd
import plotly.express as px

# Function to apply Pareto analysis
def pareto_analysis(df):
    num_column = 'Clicks'
    df['cum_sum'] = df[num_column].cumsum(skipna=True)
    df['cum_perc'] = 100 * df['cum_sum'] / df[num_column].sum()
    df['cum_perc'] = df['cum_perc'].astype(int)
    result = df[df['cum_perc'] <= 80][['Page', 'Clicks', 'Impressions', 'Country', 'Main category', 'Sub category', 'cum_perc']]
    result['cum_perc'] = result['cum_perc'].astype(str) + '%'
    return result

# Streamlit App
st.title("Pareto Analysis and Data Visualization")

# Upload dataset
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("### Original Dataset")
    st.dataframe(df.head())

    # Data cleaning
    filter_page = ['category', '#', 'blog', 'tag', 'author', 'wp-content', 'upload', 'Page', 'feed', 'legal', 'contact', 'sitemap', 'wp-login', 'wp-admin']
    df = df[~df['Page'].str.contains("|".join(filter_page))]
    df = df[df['Page'].map(lambda x: x.isascii())]

    # Pareto Analysis
    st.write("### Pareto Analysis Result")
    pareto_result = pareto_analysis(df)
    st.dataframe(pareto_result.head())

    # Save Pareto result to Excel
    st.markdown("### Download Pareto Analysis Result as Excel")
    st.markdown("[Download Pareto Analysis Result](sandbox:/path/Performance_df.xlsx)")

    # Data Visualization
    st.write("### Data Visualization")

    # First level: Country
    country = df2.groupby('Country')['Clicks'].count().reset_index()
    country.rename(columns={'Clicks': 'Clicks'}, inplace=True)
    country = country.sort_values(by='Clicks', ascending=False)
    st.plotly_chart(px.histogram(country.head(10), x='Country', y='Clicks'))

    # Second level: Main Category
    main_category = df2.groupby('Main category')['Clicks'].count().reset_index()
    main_category.rename(columns={'Clicks': 'Clicks'}, inplace=True)
    main_category = main_category.sort_values(by='Clicks', ascending=False)
    st.plotly_chart(px.histogram(main_category.head(10), x='Main category', y='Clicks'))

    # Third level: Sub Category
    sub_df = df2.groupby('Sub category')['Clicks'].count().reset_index()
    sub_df.rename(columns={'Clicks': 'Clicks'}, inplace=True)
    sub_df = sub_df.sort_values(by='Clicks', ascending=False)
    st.plotly_chart(px.histogram(sub_df.head(10), x='Sub category', y='Clicks'))
