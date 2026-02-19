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
    page_title="Visão Culinária - Sunflora",
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

# Melhores culinárias
def culinarias(df1, cuisine):

    aux = (
        df1[df1['cuisines'] == cuisine]
        .groupby(['restaurant_name', 'country', 'city', 'currency'])
        .agg(
            custo_p_dois=('average_cost_for_two', 'mean'),
            media_avaliacoes=('aggregate_rating', 'mean'),
            total_avaliacoes=('votes', 'sum'),
            menor_id=('restaurant_id', 'min')
        )
        .sort_values(by=['media_avaliacoes', 'menor_id'], ascending=[False, True])
        .reset_index()
    )

    if aux.empty:
        st.metric(cuisine, "Sem dados")
        return

    top1 = aux.iloc[0]

    st.metric(
        f'{cuisine} : {top1['restaurant_name']}',
        f"{top1['media_avaliacoes']:.1f}/5.0",
        help=f"""
        País: {top1['country']} \n
        Cidade: {top1['city']} \n
        Média de prato para duas pessoas: {top1['custo_p_dois']:.0f} \n
        Moeda: {top1['currency']} \n
        Total de avaliações: {top1['total_avaliacoes']} 
        """
    )

# ------------------------------------------------

# Dataframe melhores restaurantes
def metric5(df1):
    cols = ['restaurant_id', 'restaurant_name',
            'country', 'city', 'cuisines',
            'average_cost_for_two', 
            'aggregate_rating', 'votes']

    df1_aux = (
        df1.loc[:, cols].drop_duplicates(subset='restaurant_id')
                        .sort_values('aggregate_rating', ascending=False)
                        .head(top_n)
    )
    st.dataframe(df1_aux, use_container_width=True)

# ------------------------------------------------

def melhores_culinarias(df1_filtrado, top_n):
    df1_aux = (
        df1.groupby('cuisines')
        .agg(media_avaliacoes=('aggregate_rating', 'mean'),
                qtd_restaurantes=('restaurant_id', 'count')
        )
        .query('qtd_restaurantes >= 10')
        .sort_values(by='media_avaliacoes', ascending=False)
        .reset_index()
        .head(top_n)
    )
    fig = px.bar(df1_aux,
                 x = 'cuisines',
                 y = 'media_avaliacoes',
                 text = 'media_avaliacoes',
                 text_auto = '.2f',
                 labels = {'cuisines': 'Culinárias',
                        'media_avaliacoes': 'Média de Avaliações'}
    )
    return fig
    
# ------------------------------------------------

def piores_culinarias(df1_filtrado, top_n):
    df1_aux = (
        df1.groupby('cuisines')
        .agg(media_avaliacoes=('aggregate_rating', 'mean'),
                qtd_restaurantes=('restaurant_id', 'count')
        )
        .query('qtd_restaurantes >= 10')
        .sort_values(by='media_avaliacoes', ascending=True)
        .reset_index()
        .head(top_n)
    )
    fig = px.bar(df1_aux,
                 x = 'cuisines',
                 y = 'media_avaliacoes',
                 text = 'media_avaliacoes',
                 text_auto = '.2f',
                 labels = {'cuisines': 'Culinárias',
                          'media_avaliacoes': 'Média de avaliações'}
    )
    return fig

# =========================
#       Barra Lateral
# =========================

st.header( '🏙️ Visão Culinária - Sunflora' )

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

# Filtro Top_n
top_n = st.sidebar.slider( '### Selecione a quantidade de restaurantes que deseja analisar', 1, 20, 10 )

# Filtro por Culinária
st.sidebar.markdown( '### Selecione os tipos de culinária' )
culinarias_disponiveis = ['American', 'Arabian', 'BBQ', 'Brazilian', 
                          'Home-made', 'Japanese', 'Italian']
culinarias_selecionadas = st.sidebar.multiselect('Culinárias', culinarias_disponiveis,
                                                 default=culinarias_disponiveis)

# Filtragem do DataFrame
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df1_filtrado = df1[
    (df1['country'].isin(paises_selecionados)) &
    (df1['cuisines'].isin(culinarias_selecionadas))
    ]

st.sidebar.markdown( '''---''' )
st.sidebar.markdown( '## Powered by Gabe' )

# =========================
#     Layout Principal
# =========================

tab1, tab2, tab3 = st.tabs(['Visão Culinária', '-', '-'])

with tab1:
    with st.container():
        st.markdown( '### Os melhores restaurantes pelas principais culinárias' )

        cuisines = ['American', 'Arabian', 'Brazilian', 'Italian', 'Japanese']

        cols = st.columns(len(cuisines))

        for col, cuisine in zip(cols, cuisines):
            with col:
                culinarias(df1_filtrado, cuisine)

with tab1:
    with st.container():
        st.markdown( f'### Top {top_n} Restaurantes' )
        metric5(df1_filtrado)

with tab1:
    with st.container():
        col1, col2 = st.columns(2)

    with col1:
        st.markdown( f'### Top {top_n} Melhores culinárias' )
        fig = melhores_culinarias(df1_filtrado, top_n)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown( f'### Top {top_n} Piores culinárias' )
        fig = piores_culinarias(df1_filtrado, top_n)
        st.plotly_chart(fig, use_container_width=True)
    




