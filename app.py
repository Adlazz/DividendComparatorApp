# app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import traceback

st.title("Comparación de Retorno de Dividendos")

# Obtener la lista de compañías disponibles
try:
    response = requests.get("http://localhost:8000/company_list")
    if response.status_code == 200:
        company_list = response.json()
    else:
        st.error(f"Error al obtener la lista de compañías: {response.text}")
        company_list = {}
except requests.RequestException as e:
    st.error(f"Error de conexión al obtener la lista de compañías: {str(e)}")
    company_list = {}

# Multiselect para elegir las compañías
selected_companies = st.multiselect(
    "Seleccione las compañías (máximo 6):",
    options=list(company_list.keys()),
    default=list(company_list.keys())[:6] if company_list else [],
    max_selections=6
)

months = st.slider("Seleccione el rango de meses", 6, 12, 6)

if st.button("Generar Comparación") and selected_companies:
    symbols = ",".join(selected_companies)
    try:
        response = requests.get(f"http://localhost:8000/dividend_comparison/{months}?symbols={symbols}")
        
        if response.status_code == 200:
            result = response.json()
            data = result["data"]
            company_names = result["company_names"]
            
            df = pd.DataFrame(data).T
            df.index = pd.to_datetime(df.index)
            
            fig = px.line(df, x=df.index, y=df.columns, 
                          title=f"Retorno Acumulado de Dividendos (Últimos {months} meses)",
                          labels={"value": "Retorno Acumulado ($)", "variable": "Compañía"},
                          line_shape="linear")
            
            st.plotly_chart(fig)
            
            st.write("Retorno total al final del período:")
            final_return = df.iloc[-1].sort_values(ascending=False)
            final_return_df = pd.DataFrame({
                "Símbolo": final_return.index,
                "Nombre de la Compañía": [company_names[symbol] for symbol in final_return.index],
                "Retorno Total ($)": final_return.values
            })
            st.table(final_return_df)
        else:
            st.error(f"Error al obtener los datos: {response.text}")
    except requests.RequestException as e:
        st.error(f"Error de conexión al generar la comparación: {str(e)}")
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        st.text(traceback.format_exc())
else:
    st.warning("Por favor, seleccione al menos una compañía.")

# Información de depuración
st.write("Información de depuración:")
st.write(f"Compañías seleccionadas: {selected_companies}")
st.write(f"Meses seleccionados: {months}")