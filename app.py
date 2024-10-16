import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="DividendComparatorApp", page_icon="📈", layout="wide")

# Application title
st.title("🌟 DividendComparatorApp")

# Expanded company information
COMPANY_INFO = {
    # Technology
    'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology'},
    'MSFT': {'name': 'Microsoft Corporation', 'sector': 'Technology'},
    'GOOGL': {'name': 'Alphabet Inc.', 'sector': 'Technology'},
    'AMZN': {'name': 'Amazon.com Inc.', 'sector': 'Technology'},
    'NVDA': {'name': 'NVIDIA Corporation', 'sector': 'Technology'},
    'TSLA': {'name': 'Tesla, Inc.', 'sector': 'Technology'},
    'ADBE': {'name': 'Adobe Inc.', 'sector': 'Technology'},
    'CRM': {'name': 'Salesforce.com Inc.', 'sector': 'Technology'},
    'INTC': {'name': 'Intel Corporation', 'sector': 'Technology'},
    'CSCO': {'name': 'Cisco Systems, Inc.', 'sector': 'Technology'},
    
    # Consumer Goods
    'PG': {'name': 'Procter & Gamble Company', 'sector': 'Consumer Goods'},
    'KO': {'name': 'The Coca-Cola Company', 'sector': 'Consumer Goods'},
    'PEP': {'name': 'PepsiCo, Inc.', 'sector': 'Consumer Goods'},
    'COST': {'name': 'Costco Wholesale Corporation', 'sector': 'Consumer Goods'},
    'WMT': {'name': 'Walmart Inc.', 'sector': 'Consumer Goods'},
    'NKE': {'name': 'NIKE, Inc.', 'sector': 'Consumer Goods'},
    'MCD': {'name': 'McDonald\'s Corporation', 'sector': 'Consumer Goods'},
    'SBUX': {'name': 'Starbucks Corporation', 'sector': 'Consumer Goods'},
    'UL': {'name': 'Unilever PLC', 'sector': 'Consumer Goods'},
    'CL': {'name': 'Colgate-Palmolive Company', 'sector': 'Consumer Goods'},
    
    # Energy
    'XOM': {'name': 'Exxon Mobil Corporation', 'sector': 'Energy'},
    'CVX': {'name': 'Chevron Corporation', 'sector': 'Energy'},
    'SHEL': {'name': 'Shell plc', 'sector': 'Energy'},
    'BP': {'name': 'BP p.l.c.', 'sector': 'Energy'},
    'TTE': {'name': 'TotalEnergies SE', 'sector': 'Energy'},
    'COP': {'name': 'ConocoPhillips', 'sector': 'Energy'},
    'SLB': {'name': 'Schlumberger Limited', 'sector': 'Energy'},
    'EOG': {'name': 'EOG Resources, Inc.', 'sector': 'Energy'},
    'MPC': {'name': 'Marathon Petroleum Corporation', 'sector': 'Energy'},
    'VLO': {'name': 'Valero Energy Corporation', 'sector': 'Energy'},
    
    # Telecommunications
    'T': {'name': 'AT&T Inc.', 'sector': 'Telecommunications'},
    'VZ': {'name': 'Verizon Communications Inc.', 'sector': 'Telecommunications'},
    'TMUS': {'name': 'T-Mobile US, Inc.', 'sector': 'Telecommunications'},
    'CMCSA': {'name': 'Comcast Corporation', 'sector': 'Telecommunications'},
    'CHTR': {'name': 'Charter Communications, Inc.', 'sector': 'Telecommunications'},
    'VOD': {'name': 'Vodafone Group Plc', 'sector': 'Telecommunications'},
    'TEF': {'name': 'Telefónica, S.A.', 'sector': 'Telecommunications'},
    'AMX': {'name': 'América Móvil, S.A.B. de C.V.', 'sector': 'Telecommunications'},
    'BCE': {'name': 'BCE Inc.', 'sector': 'Telecommunications'},
    'ORAN': {'name': 'Orange S.A.', 'sector': 'Telecommunications'},
    
    # Finance
    'JPM': {'name': 'JPMorgan Chase & Co.', 'sector': 'Finance'},
    'BAC': {'name': 'Bank of America Corporation', 'sector': 'Finance'},
    'WFC': {'name': 'Wells Fargo & Company', 'sector': 'Finance'},
    'C': {'name': 'Citigroup Inc.', 'sector': 'Finance'},
    'GS': {'name': 'The Goldman Sachs Group, Inc.', 'sector': 'Finance'},
    'MS': {'name': 'Morgan Stanley', 'sector': 'Finance'},
    'BLK': {'name': 'BlackRock, Inc.', 'sector': 'Finance'},
    'AXP': {'name': 'American Express Company', 'sector': 'Finance'},
    'SCHW': {'name': 'The Charles Schwab Corporation', 'sector': 'Finance'},
    'USB': {'name': 'U.S. Bancorp', 'sector': 'Finance'},
    
    # Health
    'JNJ': {'name': 'Johnson & Johnson', 'sector': 'Health'},
    'UNH': {'name': 'UnitedHealth Group Incorporated', 'sector': 'Health'},
    'PFE': {'name': 'Pfizer Inc.', 'sector': 'Health'},
    'ABBV': {'name': 'AbbVie Inc.', 'sector': 'Health'},
    'MRK': {'name': 'Merck & Co., Inc.', 'sector': 'Health'},
    'LLY': {'name': 'Eli Lilly and Company', 'sector': 'Health'},
    'TMO': {'name': 'Thermo Fisher Scientific Inc.', 'sector': 'Health'},
    'ABT': {'name': 'Abbott Laboratories', 'sector': 'Health'},
    'DHR': {'name': 'Danaher Corporation', 'sector': 'Health'},
    'BMY': {'name': 'Bristol-Myers Squibb Company', 'sector': 'Health'},
    
    # Utilities
    'NEE': {'name': 'NextEra Energy, Inc.', 'sector': 'Utilities'},
    'DUK': {'name': 'Duke Energy Corporation', 'sector': 'Utilities'},
    'SO': {'name': 'The Southern Company', 'sector': 'Utilities'},
    'D': {'name': 'Dominion Energy, Inc.', 'sector': 'Utilities'},
    'AEP': {'name': 'American Electric Power Company, Inc.', 'sector': 'Utilities'},
    'EXC': {'name': 'Exelon Corporation', 'sector': 'Utilities'},
    'SRE': {'name': 'Sempra Energy', 'sector': 'Utilities'},
    'XEL': {'name': 'Xcel Energy Inc.', 'sector': 'Utilities'},
    'PEG': {'name': 'Public Service Enterprise Group Incorporated', 'sector': 'Utilities'},
    'WEC': {'name': 'WEC Energy Group, Inc.', 'sector': 'Utilities'},
    
    # Real Estate
    'AMT': {'name': 'American Tower Corporation', 'sector': 'Real Estate'},
    'PLD': {'name': 'Prologis, Inc.', 'sector': 'Real Estate'},
    'CCI': {'name': 'Crown Castle Inc.', 'sector': 'Real Estate'},
    'EQIX': {'name': 'Equinix, Inc.', 'sector': 'Real Estate'},
    'PSA': {'name': 'Public Storage', 'sector': 'Real Estate'},
    'O': {'name': 'Realty Income Corporation', 'sector': 'Real Estate'},
    'SPG': {'name': 'Simon Property Group, Inc.', 'sector': 'Real Estate'},
    'WELL': {'name': 'Welltower Inc.', 'sector': 'Real Estate'},
    'AVB': {'name': 'AvalonBay Communities, Inc.', 'sector': 'Real Estate'},
    'EQR': {'name': 'Equity Residential', 'sector': 'Real Estate'},
    
    # Industrials
    'HON': {'name': 'Honeywell International Inc.', 'sector': 'Industrials'},
    'UPS': {'name': 'United Parcel Service, Inc.', 'sector': 'Industrials'},
    'BA': {'name': 'The Boeing Company', 'sector': 'Industrials'},
    'CAT': {'name': 'Caterpillar Inc.', 'sector': 'Industrials'},
    'GE': {'name': 'General Electric Company', 'sector': 'Industrials'},
    'MMM': {'name': '3M Company', 'sector': 'Industrials'},
    'LMT': {'name': 'Lockheed Martin Corporation', 'sector': 'Industrials'},
    'RTX': {'name': 'Raytheon Technologies Corporation', 'sector': 'Industrials'},
    'DE': {'name': 'Deere & Company', 'sector': 'Industrials'},
    'FDX': {'name': 'FedEx Corporation', 'sector': 'Industrials'},
    
    # Materials
    'LIN': {'name': 'Linde plc', 'sector': 'Materials'},
    'SHW': {'name': 'The Sherwin-Williams Company', 'sector': 'Materials'},
    'APD': {'name': 'Air Products and Chemicals, Inc.', 'sector': 'Materials'},
    'ECL': {'name': 'Ecolab Inc.', 'sector': 'Materials'},
    'NEM': {'name': 'Newmont Corporation', 'sector': 'Materials'},
    'FCX': {'name': 'Freeport-McMoRan Inc.', 'sector': 'Materials'},
    'DOW': {'name': 'Dow Inc.', 'sector': 'Materials'},
    'DD': {'name': 'DuPont de Nemours, Inc.', 'sector': 'Materials'},
    'NUE': {'name': 'Nucor Corporation', 'sector': 'Materials'},
    'VMC': {'name': 'Vulcan Materials Company', 'sector': 'Materials'},
}

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
    'Materials': '#17becf'
}
@st.cache_data
def get_stock_data(symbol, months):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date, end=end_date)
    
    initial_price = hist['Close'].iloc[0]
    final_price = hist['Close'].iloc[-1]
    price_appreciation = (final_price - initial_price) / initial_price
    
    dividends = hist['Dividends']
    shares = 1000 / initial_price  # Assuming an initial investment of $1000
    
    monthly_dividends = dividends.resample('M').sum()
    cumulative_dividends = (monthly_dividends * shares).cumsum()
    total_dividends = cumulative_dividends.iloc[-1] if not cumulative_dividends.empty else 0
    
    dividend_yield = total_dividends / 1000  # Dividend yield based on initial $1000 investment
    total_return = price_appreciation + dividend_yield
    
    return {
        'price_appreciation': price_appreciation,
        'dividend_yield': dividend_yield,
        'total_return': total_return,
        'cumulative_dividends': cumulative_dividends
    }

@st.cache_data
def calculate_sector_averages(months):
    sector_data = {}
    for symbol, info in COMPANY_INFO.items():
        try:
            stock_data = get_stock_data(symbol, months)
            if info['sector'] not in sector_data:
                sector_data[info['sector']] = []
            sector_data[info['sector']].append(stock_data['total_return'])
        except Exception:
            pass  # Skip companies with errors
    
    sector_averages = {sector: sum(returns) / len(returns) for sector, returns in sector_data.items()}
    return sector_averages

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
        data = {}
        for company_name in selected_companies:
            symbol = company_options[company_name]
            try:
                stock_data = get_stock_data(symbol, months)
                data[symbol] = stock_data
            except Exception as e:
                st.error(f"Error fetching data for {company_name}: {str(e)}")
        
        if data:
            # Prepare data for the total return table
            total_return_data = []
            for symbol, stock_data in data.items():
                total_return_data.append({
                    "Symbol": symbol,
                    "Company Name": COMPANY_INFO[symbol]['name'],
                    "Sector": COMPANY_INFO[symbol]['sector'],
                    "Price Appreciation (%)": stock_data['price_appreciation'] * 100,
                    "Dividend Yield (%)": stock_data['dividend_yield'] * 100,
                    "Total Return (%)": stock_data['total_return'] * 100
                })
            
            total_return_df = pd.DataFrame(total_return_data)
            total_return_df = total_return_df.sort_values("Total Return (%)", ascending=False)
            
            # Display total return table
            st.subheader("📊 Total Return Analysis")
            st.table(total_return_df.style.format({
                "Price Appreciation (%)": "{:.2f}%",
                "Dividend Yield (%)": "{:.2f}%",
                "Total Return (%)": "{:.2f}%"
            }))
            
            # Prepare data for the cumulative dividends graph
            cumulative_dividends_data = {symbol: stock_data['cumulative_dividends'] for symbol, stock_data in data.items()}
            df_dividends = pd.DataFrame(cumulative_dividends_data)
            
            # Display cumulative dividends graph
            st.subheader("📈 Cumulative Dividends Over Time")
            fig_dividends = px.line(df_dividends, x=df_dividends.index, y=df_dividends.columns,
                                    title=f"Cumulative Dividends (Last {months} months)",
                                    labels={"value": "Cumulative Dividends ($)", "variable": "Company"},
                                    line_shape="linear")
            
            for trace in fig_dividends.data:
                symbol = trace.name
                sector = COMPANY_INFO[symbol]['sector']
                trace.line.color = SECTOR_COLORS.get(sector, '#000000')
                company_name = COMPANY_INFO[symbol]['name']
                trace.hovertemplate = f"{company_name}<br>Date: %{{x}}<br>Value: %{{y:.2f}}<extra></extra>"
            
            st.plotly_chart(fig_dividends, use_container_width=True)
            # Calculate and display sector averages
            sector_averages = calculate_sector_averages(months)
            
            st.subheader("📊 Sector Average Total Returns")
            sector_avg_df = pd.DataFrame(list(sector_averages.items()), columns=['Sector', 'Average Total Return'])
            sector_avg_df = sector_avg_df.sort_values('Average Total Return', ascending=False)
            
            fig_sector_avg = px.bar(sector_avg_df, x='Sector', y='Average Total Return',
                                    title=f"Average Total Return by Sector (Last {months} months)",
                                    labels={"Average Total Return": "Average Total Return (%)"})
            
            fig_sector_avg.update_traces(marker_color=[SECTOR_COLORS.get(sector, '#000000') for sector in sector_avg_df['Sector']])
            fig_sector_avg.update_layout(xaxis_tickangle=-45)
            
            st.plotly_chart(fig_sector_avg, use_container_width=True)
            
            st.table(sector_avg_df.style.format({
                "Average Total Return": "{:.2f}%"
            }).bar(subset=["Average Total Return"], color="#5fba7d"))
else:
    st.info("👈 Please select at least one company and click 'Generate Comparison' in the sidebar.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by Adrián Lazzarini")
st.sidebar.markdown("Data provided by Yahoo Finance")