# Bibliotecas necessárias
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import datetime
from PIL import Image
import folium
from folium.plugins import MarkerCluster
import inflection

# Importando o dataset
df = pd.read_csv( 'dataset/zomato.csv' )
df1 = df.copy()
df1 = df1.dropna()

# Configuração da página
st.set_page_config(
    page_title="Visão Geral - Sunflora",
    page_icon="🌻",
    layout='wide')

# Funções e Dicionários
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America"}

def country_name(country_id):
    return COUNTRIES.get(country_id, "Unknown")
# ---------------------------------------------------------
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

def color_name(color_code):
    return COLORS(color_code)
# ---------------------------------------------------------
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
# ---------------------------------------------------------
def rename_columns(df):
    df1 = df.copy()

    df1.columns = (
        df1.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
    )
    return df1
# ---------------------------------------------------------

df1 = rename_columns(df1)

df1['cores'] = df1['rating_color'].map(COLORS).fillna('Unknown')
df1['country'] = df1['country_code'].map(COUNTRIES).fillna('Unknown')
df1['price_range'] = df1['price_range'].map(create_price_type)
df1["cuisines"] = df1["cuisines"].astype(str).apply(lambda x: x.split(",")[0])

# ---------------------------------------------------------

# Restaurantes cadastrados
def restaurantes(df1):
    restaurantes_unicos = df1['restaurant_id'].nunique()
    st.metric('', restaurantes_unicos)

# ---------------------------------------------------------

# Países cadastrados
def paises(df1):
    paises_unicos = df1['country'].nunique()
    st.metric('', paises_unicos)

# ---------------------------------------------------------

# Cidades cadastradas
def cidades(df1):
    cidades_unicas = df1['city'].nunique()
    st.metric('', cidades_unicas)

# ---------------------------------------------------------

# Total de avaliações
def avaliacoes(df1):
    total_avaliacoes = f"{df1['votes'].sum():,}".replace(",", ".")
    st.metric('',total_avaliacoes)

# ---------------------------------------------------------

# Tipos de culinária
def culinaria(df1):
    tipos_culinaria = df1['cuisines'].nunique()
    st.metric('', tipos_culinaria)

# ---------------------------------------------------------

# Criação do mapa
def mapa_sunflora(df1):
    f = folium.Figure(width=1920, height=1080) # Cria o mapa
    m = folium.Map(max_bounds=True).add_to(f) # Adiciona os marcadores
    marker_cluster = MarkerCluster().add_to(m) # Agrupa os marcadores

    for _, line in df1.iterrows():   # Pega todos os restaurantes e as colunas que selecionamos logo abaixo, 
                                     # pegando os dados das linhas que escrevemos abaixo

        name = line['restaurant_name']
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = line["cores"]

# Esta parte é a janela que aparece quando o pin é clicado no mapa 

        html = f"""
        <p><strong>{name}</strong></p>
        <p>Price: {price_for_two},00 ({currency}) para dois</p>
        <p>Type: {cuisine}</p>
        <p>Aggregate Rating: {rating}/5.0</p>
        """

        popup = folium.Popup(html, max_width=500)  # Janela Pop-up
    
    # Marcadores no mapa
        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(
                color=color,
                icon="cutlery", # Definição de ícone no mapa (cutlery -> talher)
                prefix="fa"     # Biblioteca do folium possui inúmeros ícones
            ),
        ).add_to(marker_cluster)

    # Exibe o mapa
    folium_static(m, width=1024, height=768)

# =========================
#       Barra Lateral
# =========================

st.header( '🏠 Visão Geral - Sunflora' )

with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        image = Image.open( 'sunflora.png' )
        st.image(image, width=135)

    st.markdown(
        "<h2 style='text-align: center;'>Sunflora</h2>",
        unsafe_allow_html=True)
    st.markdown(
        "<h4 style='text-align: center;'>Seu delivery favorito a poucos cliques!</h4>",
        unsafe_allow_html=True)
    
st.sidebar.markdown ( '''---''' )
st.sidebar.markdown( '### Powered by Gabe' )

# =========================
#     Layout Principal
# =========================

tab1, tab2, tab3 = st.tabs(['Visão Geral', '-', '-'])

with tab1:
    st.container()
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text( 'Restaurantes cadastrados' )
        restaurantes(df1)
    
    with col2:
        st.text( 'Países cadastradas' )
        paises(df1)
    
    with col3:
        st.text( 'Cidades cadastradas' )
        cidades(df1)

    with col4:
        st.text( 'Total de avaliações registradas' )
        avaliacoes(df1)

    with col5:
        st.text( 'Opções de culinária' )
        culinaria(df1)

with tab1:
    with st.container():
        st.markdown( '### Distribuição dos restaurantes por países' )
        mapa_sunflora(df1)