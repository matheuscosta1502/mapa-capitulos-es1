import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mapa de Capítulos no ES", layout="wide")
st.title("📍 Mapa de Municípios com Capítulo no Espírito Santo")

file = st.file_uploader("Envie a planilha Excel", type=["xlsx"])

if file:
    df = pd.read_excel(file, sheet_name="Planilha1")

    df['Tem Capítulo'] = df[['GCE-ES', 'OFEX']].notna().any(axis=1)
    df = df[df['Tem Capítulo']]

    municipios_com_capitulo = df['Município'].tolist()

    coords = pd.read_csv("https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/municipios.csv")
    coords_es = coords[coords['Estado'] == 'ES']
    mapa = coords_es[coords_es['Nome_Município'].isin(municipios_com_capitulo)]

    if not mapa.empty:
        fig = px.scatter_mapbox(
            mapa,
            lat="Latitude",
            lon="Longitude",
            hover_name="Nome_Município",
            zoom=6,
            height=600
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum município encontrado no mapa.")
