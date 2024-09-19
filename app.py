import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="DividendComparatorApp", page_icon="📈", layout="wide")

# Título de la aplicación
st.title("🌟 DividendComparatorApp")

# Información de las compañías
COMPANY_INFO = {
    'T': 'AT&T Inc.',
    'O': 'Realty Income Corporation',
    'PG': 'Procter & Gamble Company',
    'JNJ': 'Johnson & Johnson',
    'XOM': 'Exxon Mobil Corporation',
    'KO': 'The Coca-Cola Company',
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'INTC': 'Intel Corporation',
    'IBM': 'International Business Machines Corporation',
    'CSCO': 'Cisco Systems, Inc.',
    'TXN': 'Texas Instruments Incorporated'
}

@st.cache_data
def get_dividend_data(symbol, months):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date, end=end_date)
    dividends = hist['Dividends']
    
    try:
        current_price = stock.info['currentPrice']
    except:
        current_price = hist['Close'].iloc[-1]
    
    shares = 1000 / current_price  # Asumiendo una inversión inicial de $1000
    
    monthly_dividends = dividends.resample('M').sum()
    cumulative_dividends = (monthly_dividends * shares).cumsum()
    
    return cumulative_dividends, COMPANY_INFO.get(symbol, 'Unknown Company')

# Interfaz de usuario
st.sidebar.header("📊 Configuración")

# Multiselect para elegir las compañías
selected_companies = st.sidebar.multiselect(
    "Seleccione las compañías (máximo 6):",
    options=list(COMPANY_INFO.keys()),
    default=list(COMPANY_INFO.keys())[:6],
    max_selections=6
)

months = st.sidebar.slider("Seleccione el rango de meses", 6, 12, 6)

if st.sidebar.button("Generar Comparación") and selected_companies:
    with st.spinner('Obteniendo datos...'):
        data = {}
        company_names = {}
        for symbol in selected_companies:
            try:
                dividend_data, company_name = get_dividend_data(symbol, months)
                data[symbol] = dividend_data
                company_names[symbol] = company_name
            except Exception as e:
                st.error(f"Error al obtener datos para {symbol}: {str(e)}")
        
        if data:
            df = pd.DataFrame(data)
            
            # Gráfico
            fig = px.line(df, x=df.index, y=df.columns, 
                          title=f"Retorno Acumulado de Dividendos (Últimos {months} meses)",
                          labels={"value": "Retorno Acumulado ($)", "variable": "Compañía"},
                          line_shape="linear")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de retorno total
            st.subheader("📝 Retorno total al final del período:")
            final_return = df.iloc[-1].sort_values(ascending=False)
            final_return_df = pd.DataFrame({
                "Símbolo": final_return.index,
                "Nombre de la Compañía": [company_names[symbol] for symbol in final_return.index],
                "Retorno Total ($)": final_return.values
            })
            st.table(final_return_df)
else:
    st.info("👈 Por favor, seleccione al menos una compañía y haga clic en 'Generar Comparación' en la barra lateral.")

# Pie de página
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado por Adrián Lazzarini")
st.sidebar.markdown("Datos proporcionados por Yahoo Finance")