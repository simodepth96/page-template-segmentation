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

# Upload dataset
st.write("## Upload your dataset")
uploaded_file = st.file_uploader("Upload file (CSV or XLSX)", type=["csv", "xlsx"])

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
        if st.button("Export Cleaned and Segmented Data as CSV"):
            csv = df2.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # B64 encoding for data
            href = f'<a href="data:file/csv;base64,{b64}" download="Cleaned_Segmented_Data.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

        st.dataframe(df2.head())

        # Data Viz
        st.write("### Data Visualization")

        # Segmentation based on user choice
        segmented_df = df2.groupby(category_level)['Clicks'].count().reset_index()
        segmented_df.rename(columns={'Clicks': 'Clicks'}, inplace=True)
        segmented_df = segmented_df.sort_values(by='Clicks', ascending=False)

        # Display segmented data
        st.write(f"#### {category_level} by Clicks")
        st.dataframe(segmented_df.head())

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
            
            # Export as CSV
            if st.button("Export Pareto Result as CSV"):
                csv = result.to_csv('Pareto_Result.csv', index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # B64 encoding for data
                href = f'<a href="data:file/csv;base64,{b64}" download="Pareto_Result.csv">Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)

except KeyError as e:
    st.error(f"Error: {e}. Please choose a valid category level.")
