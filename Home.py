import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home - Sunflora",
    page_icon="📊",
    layout='centered',
)

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

st.markdown( "## 🌻 Sunflora Growth Dashboard")

st.markdown(
    """
    Este Growth Dashboard foi desenvolvido para o acompanhamento estratégico das métricas de crescimento da plataforma Sunflora.

    O objetivo é fornecer uma visão clara, interativa e orientada a dados sobre o 
    desempenho dos restaurantes cadastrados, permitindo análises por país, cidade e tipo de culinária.
    """
)
st.markdown("")

st.markdown( '### Como utilizar este Dashboard:' )

st.markdown('')

st.markdown( 'O painel está dividido em quatro visões principais, cada uma com um objetivo específico de análise:' )
st.markdown(
    """
    - Visão Geral:
        Aqui contém um panorama completo da plataforma.
        - Mapa de distribuição dos restaurantes por países
        - Indicadores globais da base de dados
    """
)

st.markdown('')

st.markdown(
    """
    - Visão Países:
        Apresenta a análise aprofundada por país.
        - Comparação de desempenho entre países
        - Avaliação do volume de restaurantes
        - Análise de avaliação e engajamento
    """
)   

st.markdown('')

st.markdown(
    """
    - Visão Cidade:
        Apresenta a análise aprofundada por cidades.
        - Identificação de cidades com maior concentração de restaurantes
        - Comparação de avaliações médias
    """
)

st.markdown('')

st.markdown(
    """
    - Visão Culinária:
        Análise segmentada por tipo de culinária
        - Identificação de melhores restaurantes
        - Comparação de avaliações médias
    """
)

st.markdown('')

st.markdown( '### Filtros Interativos' )

st.markdown('')

st.markdown(
     """
        Este dashboard conta com filtros interativos na barra lateral permitindo análises por:
        - Seleção de países
        - Seleção de tipos de culinária
        - Definição da quantidade de restaurantes analisados

        Os gráficos adaptados e atualizados com base nas seleções realizadas,
        garantindo uma análise personalizada e interativa.
    """
)