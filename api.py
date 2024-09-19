# api.py
from fastapi import FastAPI, HTTPException
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

app = FastAPI()

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

def get_dividend_data(symbol, months):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date, end=end_date)
    dividends = hist['Dividends']
    
    current_price = stock.info['currentPrice']
    shares = 1000 / current_price  # Asumiendo una inversión inicial de $1000
    
    monthly_dividends = dividends.resample('M').sum()
    cumulative_dividends = (monthly_dividends * shares).cumsum()
    
    return cumulative_dividends, COMPANY_INFO.get(symbol, 'Unknown Company')

@app.get("/dividend_comparison/{months}")
async def get_dividend_comparison(months: int, symbols: str):
    symbol_list = symbols.split(',')
    if len(symbol_list) > 6:
        raise HTTPException(status_code=400, detail="Maximum 6 companies allowed")
    
    data = {}
    company_names = {}
    for symbol in symbol_list:
        try:
            dividend_data, company_name = get_dividend_data(symbol, months)
            data[symbol] = dividend_data
            company_names[symbol] = company_name
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching data for {symbol}: {str(e)}")
    
    df = pd.DataFrame(data)
    df.index = df.index.strftime('%Y-%m-%d')
    
    return {"data": df.to_dict(orient='index'), "company_names": company_names}

@app.get("/company_list")
async def get_company_list():
    return COMPANY_INFO