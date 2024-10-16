import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Page configuration
st.set_page_config(page_title="DividendComparatorApp", page_icon="📈", layout="wide")

# Application title
st.title("🌟 DividendComparatorApp")

# API endpoint
API_ENDPOINT = "http://localhost:8501"  # Update this if your FastAPI server is on a different address

# Fetch company list from API
@st.cache_data
def get_company_list():
    response = requests.get(f"{API_ENDPOINT}/company_list")
    return response.json()

COMPANY_INFO = get_company_list()

# Color mapping for sectors
SECTOR_COLORS = {
    'Technology': '#1f77b4',
    'Consumer Goods': '#ff7f0e',
    'Energy': '#2ca02c',
    'Telecommunications': '#d62728',
    'Finance': '#9467bd',
    'Health': '#8c564b',
    'Utilities': '#e377c2',
    'Real Estate': '#7f7f7f',
    'Industrials': '#bcbd22',
    'Food and Beverages': '#17becf'
}

# User interface
st.sidebar.header("📊 Configuration")

# Sector filter
sectors = list(set(company['sector'] for company in COMPANY_INFO.values()))
selected_sectors = st.sidebar.multiselect(
    "Select sectors:",
    options=sectors,
    default=sectors
)

# Company multiselect
company_options = {name: symbol for symbol, info in COMPANY_INFO.items() for name in [info['name']] if info['sector'] in selected_sectors}
selected_companies = st.sidebar.multiselect(
    "Select companies (maximum 10):",
    options=list(company_options.keys()),
    default=list(company_options.keys())[:6],
    max_selections=10
)

months = st.sidebar.slider("Select the range of months", 6, 12, 6)

if st.sidebar.button("Generate Comparison") and selected_companies:
    with st.spinner('Fetching data...'):
        selected_symbols = ','.join([company_options[name] for name in selected_companies])
        response = requests.get(f"{API_ENDPOINT}/dividend_comparison/{months}?symbols={selected_symbols}")
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['data']).T
            company_info = data['company_info']
            
            # Graph
            fig = px.line(df, x=df.index, y=df.columns, 
                          title=f"Cumulative Dividend Return (Last {months} months)",
                          labels={"value": "Cumulative Return ($)", "variable": "Company"},
                          line_shape="linear")
            
            # Update line colors based on sector
            for trace in fig.data:
                symbol = trace.name
                sector = company_info[symbol]['sector']
                trace.line.color = SECTOR_COLORS.get(sector, '#000000')
            
            # Update hover template to show full company name
            for trace in fig.data:
                symbol = trace.name
                company_name = company_info[symbol]['name']
                trace.hovertemplate = f"{company_name}<br>Date: %{{x}}<br>Value: %{{y:.2f}}<extra></extra>"
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Total return table
            st.subheader("📝 Total return at the end of the period:")
            final_return = df.iloc[-1].sort_values(ascending=False)
            final_return_df = pd.DataFrame({
                "Symbol": final_return.index,
                "Company Name": [company_info[symbol]['name'] for symbol in final_return.index],
                "Sector": [company_info[symbol]['sector'] for symbol in final_return.index],
                "Total Return ($)": final_return.values
            })
            st.table(final_return_df)
            
            # Fetch and display sector averages
            response_avg = requests.get(f"{API_ENDPOINT}/sector_averages/{months}")
            if response_avg.status_code == 200:
                sector_data = response_avg.json()['data']
                sector_df = pd.DataFrame(sector_data).T
                
                st.subheader("📊 Sector Averages")
                fig_sector = px.line(sector_df, x=sector_df.index, y=sector_df.columns,
                                     title=f"Average Cumulative Dividend Return by Sector (Last {months} months)",
                                     labels={"value": "Average Cumulative Return ($)", "variable": "Sector"},
                                     line_shape="linear")
                
                for trace in fig_sector.data:
                    sector = trace.name
                    trace.line.color = SECTOR_COLORS.get(sector, '#000000')
                
                st.plotly_chart(fig_sector, use_container_width=True)
        else:
            st.error(f"Error fetching data: {response.text}")
else:
    st.info("👈 Please select at least one company and click 'Generate Comparison' in the sidebar.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by Adrián Lazzarini")
st.sidebar.markdown("Data provided by Yahoo Finance")