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
import inflection

# Importando o dataset
df = pd.read_csv( 'dataset/zomato.csv' )
df1 = df.copy()
df1 = df1.dropna()

# Configuração da página
st.set_page_config(
    page_title="Visão Cidades - Sunflora",
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

df1['country'] = df1['country_code'].map(COUNTRIES).fillna('Unknown')
df1['price_range'] = df1['price_range'].map(create_price_type)
df1["cuisines"] = df1["cuisines"].astype(str).apply(lambda x: x.split(",")[0])

# ---------------------------------------------------------

# Cidades com mais restaurantes
def top_cidades_restaurantes (df1, top_n):
    df1_aux = (
        df1.groupby(['city','country'])['restaurant_id']
           .nunique()
           .sort_values(ascending=False)
           .reset_index()
           .head(top_n)
    )
    fig = px.bar(
        df1_aux, 
        x = 'city', 
        y = 'restaurant_id',
        color = 'country',
        labels = {'city': 'Cidades', 
                'restaurant_id': 'Quantidade de restaurantes', 
                'country': 'Países'}
    )
    return fig

# ------------------------------------------------

# Rstaurantes com média acima de 4
def top_restaurantes_media_acima_4 (df1, top_n):
    df1_aux = (
        df1[df1['aggregate_rating'] >= 4]
        .groupby(['city', 'country'])
        .agg(
            qtd_restaurantes_acima_4 = ('restaurant_id', 'nunique'),
            avaliacao_media = ('aggregate_rating', 'mean'),
        )
        .sort_values('qtd_restaurantes_acima_4',ascending=False)
        .reset_index()
        .head(top_n)
    )
    fig = px.bar(
        df1_aux,
        x = 'city',
        y = 'qtd_restaurantes_acima_4',
        color = 'country',
        labels = {'city': 'Cidades',
                  'qtd_restaurantes_acima_4': 'Restaurantes',
                  'country': 'Países'}
     )
    return fig

# ------------------------------------------------

# Restaurantes com média acima de 2.5 
def top_restaurantes_media_acima_2_5 (df1, top_n):
    df1_aux = (
            df1[df1['aggregate_rating'] <= 2.5]
            .groupby(['city', 'country'])
            .agg(
                qtd_restaurantes_abaixo_25 = ('restaurant_id', 'nunique'),
                avaliacao_media = ('aggregate_rating', 'mean'),
            )
            .sort_values('qtd_restaurantes_abaixo_25',ascending=False)
            .reset_index()
            .head(top_n)
        )
    fig = px.bar(
        df1_aux,
        x = 'city',
        y = 'qtd_restaurantes_abaixo_25',
        color = 'country',
        labels = {'city': 'Cidades',
                  'qtd_restaurantes_abaixo_25': 'Restaurantes',
                  'country': 'Países'}
    )
    return fig

# ------------------------------------------------

# Cidades com mais tipos de culinária 
def top_cidades_mais_culinarias (df1, top_n):
    df1_aux = (
        df1.groupby(['city', 'country'])['cuisines']
           .nunique()
           .sort_values(ascending=False)
           .reset_index()
           .head(top_n)
    )
    fig = px.bar(
        df1_aux,
        x = 'city',
        y = 'cuisines',
        color = 'country',
        labels = {'city': 'Cidade',
                  'cuisines': 'Tipos de culinária',
                  'country': 'Países'}
    )
    return fig

# =========================
#       Barra Lateral
# =========================

st.header( '🏙️ Visão Cidades - Sunflora' )

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

st.sidebar.markdown( '''---''' )

# Filtro por Países
st.sidebar.markdown( '### Selecione os países que deseja analisar' )

paises_disponiveis = sorted(df1['country'].unique())
paises_selecionados = st.sidebar.multiselect('Países', paises_disponiveis, 
                                             default=paises_disponiveis)

# Filtro Top_n
top_n = st.sidebar.slider( '### Selecione a quantidade de cidades que deseja analisar', 1, 20, 10 )

# Filtragem do DataFrame
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df1_filtrado = df1[
    (df1['country'].isin(paises_selecionados))
]

st.sidebar.markdown( '''---''' )
st.sidebar.markdown( '## Powered by Gabe' )

# =========================
#     Layout Principal
# =========================

tab1, tab2, tab3 = st.tabs(['Visão Cidades', '-', '-'])

with tab1:
    with st.container():
        st.markdown( f'### Top {top_n} Cidades com mais restaurantes' )
        fig = top_cidades_restaurantes(df1_filtrado, top_n)
        st.plotly_chart(fig, use_container_width=True)

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown( f'### Top {top_n} Restaurantes com média de avaliação acima de 4.0' )
        fig = top_restaurantes_media_acima_4(df1_filtrado, top_n)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown( f'### Top {top_n} Restaurantes com média de avaliação abaixo de 2.5' )
        fig = top_restaurantes_media_acima_2_5(df1_filtrado, top_n)
        st.plotly_chart(fig, use_container_width=True)

with tab1:
    with st.container():
        st.markdown( '### Top 15 Cidades com mais tipos distintos de culinária' )
        fig = top_cidades_mais_culinarias(df1_filtrado, top_n)
        st.plotly_chart(fig, use_container_width=True)
