# 1. Problema de Negócio
A Sunflora é uma empresa de tecnologia que opera no modelo de Marketplace, conectando restaurantes a consumidores finais em escala global. A plataforma facilita o encontro entre o cliente e seu restaurante desejado, centralizando informações cruciais como localização, tipos de culinária, disponibilidade de reservas, serviços de entrega e avaliações de usuários.

Recentemente, a empresa passou por uma renovação em sua liderança e o novo CEO identificou que, apesar do crescimento acelerado da base de dados, a companhia carece de visibilidade clara sobre seus principais KPIs de expansão e desempenho.
Você foi contratado como Analista de Dados e o objetivo foi transformar esse volume de dados brutos em inteligência estratégica, respondendo a perguntas fundamentais sobre o ecossistema da empresa e consolidando esses indicadores em um dashboard centralizado para apoiar decisões mais assertivas e rápidas.

# 2. O Desafio (Métricas de Negócio)
Para fornecer a visão 360° solicitada pelo CEO, o projeto foi estruturado para responder às seguintes perguntas:

## Geral
Quantos restaurantes únicos estão registrados?

Quantos países únicos estão registrados?

Quantas cidades únicas estão registradas?

Qual o total de avaliações feitas?

Qual o total de tipos de culinária registrados?

## Pais
Qual o nome do país que possui mais cidades registradas?

Qual o nome do país que possui mais restaurantes registrados?

Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?

Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?

Qual o nome do país que possui a maior quantidade de avaliações feitas?

Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?

Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?

Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?

Qual o nome do país que possui, na média, a maior nota média registrada?

Qual o nome do país que possui, na média, a menor nota média registrada?

Qual a média de preço de um prato para dois por país?

## Cidade
Qual o nome da cidade que possui mais restaurantes registrados?

Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?

Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?

Qual o nome da cidade que possui o maior valor médio de um prato para dois?

Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?

Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?

Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?

Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

## Restaurantes
Qual o nome do restaurante que possui a maior quantidade de avaliações?

Qual o nome do restaurante com a maior nota média?

Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?

Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?

Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?

Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?

Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?

Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

## Tipos de Culinária
Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?

Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?

Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?

Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?

Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?

Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?

Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?

Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?

Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?

Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?

Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?

Qual o tipo de culinária que possui a maior nota média?

Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?

# 3. Estratégia da Solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:

## 1. Visão das métricas dos países
a. Restaurantes registrados por país.
b. Cidades registradas por país.
c. Média de avaliações feitas por país.
d. Média de preço de um prato para duas pessoas por país.

## 2. Visão das métricas das cidades
a. Top 10 cidades com mais restaurantes na base de dados.
b. Top 7 cidades com restaurantes com média acima de 4.
c. Top 7 cidades com restaurantes com média abaixo de 2.5.
d. Top 15 cidades com mais restaurantes de tipos culinários distintos.

## 3. Visão das métricas de culinária
a. Melhores restaurantes pelas principais culinárias.
b. Top restaurantes.
c. Top melhores tipos de culinária.
d. Top piores tipos de culinária.

# 4. Top 3 Insights de Dados
Segmentação de Mercado: Indonésia e Austrália apresentam os maiores custos médios por refeição para duas pessoas, indicando restaurantes mais luxuosos voltado ao público de alto poder aquisitivo.

Qualidade Geográfica: Cidades com avaliações acima de 4,0 concentram-se em países desenvolvidos, refletindo consumidores mais ativos e padrões competitivos elevados

Fator de Confiança: Restaurantes com notas máximas geralmente possuem um volume superior a 200 avaliações, correlacionando alta qualidade com alto engajamento.

# 5. Produto Final
O resultado deste projeto é um painel online interativo, permitindo que o CEO acesse KPIs que auxiliem em sua tomada de decisões.

Acesse o Dashboard aqui: https://sunflora.streamlit.app/

# 6. Próximos Passos
Refinar e reduzir o número de métricas para maior foco operacional.

Implementar filtros temporais e geográficos avançados.

Desenvolver modelos preditivos de churn de restaurantes.
