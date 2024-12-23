import streamlit as st
import pandas as pd
import plotly.express as px
import base64

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
    df2 = df_cleaned.dropna()

    return df2

# Streamlit App
st.title("Page Template Segmentation and Data Analysis")

st.markdown(
    "This app allows you to grasp top-traffic driving areas of a website."
    "In this space, you'll have all your site URLs broken down into page templates and grouped by Clicks."
)

# File Upload
st.markdown("---")
uploaded_file = st.file_uploader("\ud83d\udcc4 Upload a CSV/XLSX file with the following headers: Page,Clicks, Impressions, CTR, Position", type=["csv", "xlsx"])

st.sidebar.subheader("\ud83d\udd0f Use Cases")
st.sidebar.markdown(
    """
    - Preliminary sampling of traffic-driving page templates for a Core Web Vitals analysis
    - Explorative analysis of popular page templates of a brand-new website prior technical SEO deep dives
    """
)

st.sidebar.subheader("\ud83d\udcaa Strengths")
st.sidebar.markdown(
    """
    - Identify the top-traffic driving page templates of a website
    - Zoom in on 20% of page templates bringing in 80% of organic traffic
    - Works with large datasets, returns bar chart and lets you export the segmented output
    """
)

# Dropdown for selecting category level
category_level = st.selectbox("Choose Category Level", ["Country", "Main category", "Sub category"])

# Placeholder for Pareto Analysis activation
st.write("Click the button below to run a Pareto Analysis and export the result.")
pareto_button = st.button("Pareto Analysis")

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

        # Apply data cleaning and segmentation
        df2 = clean_and_segment_data(df)

        # Display the cleaned and segmented dataset
        st.write("### Cleaned and Segmented Data")

        # Export button for Cleaned and Segmented Data
        if st.button("Export Cleaned and Segmented Data as Excel"):
            excel_file = df2.to_excel('Cleaned_Segmented_Data.xlsx', index=False)
            b64 = base64.b64encode(open('Cleaned_Segmented_Data.xlsx', 'rb').read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Cleaned_Segmented_Data.xlsx">Download Excel</a>'
            st.markdown(href, unsafe_allow_html=True)

        st.dataframe(df2.head())

        # Data Viz
        st.write("### Data Visualization")

        # Segmentation based on user choice
        segmented_df = df2.groupby(category_level)['Clicks'].count().reset_index()
        segmented_df.rename(columns={'Clicks': 'Clicks'}, inplace=True)
        segmented_df = segmented_df.sort_values(by='Clicks', ascending=False)

        # Bar chart
        st.write(f"#### Bar Chart - {category_level} by Clicks")
        st.plotly_chart(px.bar(segmented_df.head(10), x=category_level, y='Clicks', labels={'Clicks': 'Clicks Count'}))

        if pareto_button:
            # Apply Pareto
            num_column = 'Clicks'
            df2['cum_sum'] = df2[num_column].cumsum(skipna=True)
            df2['cum_perc'] = 100 * df2['cum_sum'] / df2[num_column].sum()
            df2['cum_perc'] = df2['cum_perc'].astype(int)
            result = df2[df2['cum_perc'] <= 80][['Page', 'Clicks', 'Impressions', 'Country', 'Main category', 'Sub category', 'cum_perc']]
            result['cum_perc'] = result['cum_perc'].astype(str) + '%'

            # Save the result to an Excel file
            st.write("### Pareto Result")
            st.dataframe(result.head())

            # Export as Excel
            if st.button("Export Pareto Result as Excel"):
                result.to_excel('Pareto_Result.xlsx', index=False)
                b64 = base64.b64encode(open('Pareto_Result.xlsx', 'rb').read()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="Pareto_Result.xlsx">Download Excel</a>'
                st.markdown(href, unsafe_allow_html=True)

except KeyError as e:
    st.error(f"Error: {e}. Please choose a valid category level.")
