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
    page_title="Visão Países - Sunflora",
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

# Restaurantes cadastrados
def restaurantes_cadastrados(df1) : 
    df1_aux = (
        df1.groupby('country')['restaurant_id']
           .nunique()
           .sort_values(ascending=False)
           .reset_index()   
    )
    fig = px.bar(df1_aux,
           x = 'country',
           y = 'restaurant_id',
           text_auto= True,
           labels = {'country': 'Países',
                     'restaurant_id': 'Número de restaurantes'}
    )
    return fig

# ------------------------------------------------

# Cidades cadastradas
def cidades_cadastradas(df1) :
    df1_aux = (
        df1.groupby('country')['city']
           .nunique()
           .sort_values(ascending=False)
           .reset_index()
    )
    fig = px.bar(df1_aux,
                 x = 'country',
                 y = 'city',
                 text_auto = True,
                 labels = {'country': 'Países',
                           'city': 'Cidades'}
    )
    return fig

# ------------------------------------------------

# Média de avaliações
def qtd_avaliacoes(df1):
    df1_aux = (
        df1.groupby('country')['votes']
           .mean()
           .sort_values(ascending=False)
           .reset_index()
           .round()
    )
    fig = px.bar(df1_aux,
                 x = 'country',
                 y = 'votes',
                 text_auto = True,
                 labels = {'country': 'Países',
                           'votes': 'Quantidade de avaliações'}
    )
    return fig

# ------------------------------------------------

# Custo médio de prato para duas pessoas
def custo_medio_p_dois(df1):
    df1_aux = (
        df1.groupby('country')['average_cost_for_two']
           .mean()
           .sort_values(ascending=False)
           .reset_index()
           .round()
    )
    fig = px.bar(df1_aux,
                 x = 'country',
                 y = 'average_cost_for_two',
                 text_auto = True,
                 labels = {'country': 'Países',
                           'average_cost_for_two': 'Custo médio para duas pessoas'}
    )
    return fig

# =========================
#       Barra Lateral
# =========================

st.header( '🌎 Visão Países - Sunflora' )

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

st.sidebar.markdown('''---''')

# Filtro por Países
st.sidebar.markdown( '### Selecione os países que deseja analisar' )

paises_disponiveis = sorted(df1['country'].unique())
paises_selecionados = st.sidebar.multiselect('Países', paises_disponiveis, 
                                             default=paises_disponiveis)

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

tab1, tab2, tab3 = st.tabs(['Visão Países', '-', '-'])

with tab1:
    st.container()
    st.markdown( '### Restaurantes cadastrados' )
    fig = restaurantes_cadastrados(df1_filtrado)
    st.plotly_chart(fig, use_container_width=True)

with tab1:
    st.container()
    st.markdown( '### Cidades registradas' )
    fig = cidades_cadastradas(df1_filtrado)
    st.plotly_chart(fig, use_container_width=True)

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown( '### Média de avaliações registradas' )
        fig = qtd_avaliacoes(df1_filtrado)
        st.plotly_chart( fig, use_container_width=True )
    
    with col2:
        st.markdown( '### Custo médio de prato para duas pessoas' )
        fig = custo_medio_p_dois(df1_filtrado)
        st.plotly_chart( fig, use_container_width=True )
