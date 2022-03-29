import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn import cluster as c
from PIL import Image



#read data
@st.cache( allow_output_mutation = True )
def get_data( path ):
    data = pd.read_excel( path )


    return data


######## Calculo do Modelo #########

x = get_data ( 'x.xlsx' )
# model definition
kmeans = c.KMeans (init = 'random', n_clusters = 6,n_init = 10, max_iter = 300, random_state = 42)

# model training
kmeans.fit( x )

#clustering
labels = kmeans.labels_
########################################



image = Image.open('plusoft3.png')
st.image(image)
st.title('Bem vindo ao case de  Análise da Plusoft')


st.markdown('Escolha abaixo os valores do novo município:')


######## botões do municipio #####################

a = st.slider('lat',min_value= 5.0, max_value=33.0, step=0.1  )
b = st.slider('long',min_value= 33.0, max_value= 72.0, step=0.01 )
c = st.slider('Área KM²',min_value=2.0, max_value=161445.0, step=1.5 )
d = st.slider('Densidade demográfica, 2000',min_value=0, max_value=12882, step=10)
e = st.slider('Distância à capital (km)',min_value=0, max_value=1475, step=100)
f = st.slider('Esperança de vida ao nascer, 2000',min_value=54, max_value=78, step=5)
g = st.slider('Mortalidade até um ano de idade, 2000',min_value=5, max_value=109, step=5)
h = st.slider('Taxa de fecundidade total, 2000',min_value=1.0, max_value=8.0, step=0.1)
i = st.slider('Percentual de pessoas de 25 anos ou mais analfabetas, 2000',min_value=2, max_value=70, step=1)
j = st.slider('Renda per Capita, 2000',min_value=28, max_value=955, step=50)
k = st.slider('Índice de Gini, 2000',min_value=0.0, max_value=1.0, step=0.01)
l = st.slider('Intensidade da indigência, 2000',min_value=0, max_value=88, step=5)
m = st.slider('Intensidade da pobreza, 2000',min_value=17, max_value=70, step=2)
n = st.slider('Índice de Desenvolvimento Humano Municipal, 2000',min_value=0.0, max_value=1.0, step=0.01)
o = st.slider('Taxa bruta de freqüência à escola, 2000',min_value=44, max_value=107, step=1)
p = st.slider('Taxa de alfabetização, 2000',min_value=39, max_value=99, step=1)
q = st.slider('Média de anos de estudo das pessoas de 25 anos ou mais de idade, 2000',min_value=0.0, max_value=9.0, step=0.1)
r = st.slider('População total, 2000',min_value=795, max_value=10434252, step=100000)
s = st.slider('População urbana, 2000',min_value=0, max_value=9813187, step=100)
t = st.slider('População rural, 2000',min_value=0, max_value=621065, step=100)
u = st.slider('cresc_popu_1991_2000',min_value= 0.0, max_value=4.0, step=0.01)
v = st.slider('receita_pop_mercado_2000',min_value=67619, max_value=6365311090, step=5000)


st.text('O município acima pertence ao grupo:')
st.write( kmeans.predict([[a,b,c,d,e,f,g,h,i,j,k,
                           l,m,n,o,p,q,r,s,t,u,v]]))


st.header( 'Base de Dados')


#load data
data = get_data ( 'df_plusoft.xlsx' )
st.dataframe( data.head() )

#plot map
st.title ( 'Mapa do Brasil com os grupos dos Municípios')
is_check = st.checkbox( 'Habilitar Mapa')

#filters
renda_min = int( data['Renda per Capita, 2000'].min () )
renda_max = int( data['Renda per Capita, 2000'].max () )
renda_avg = int( data['Renda per Capita, 2000'].mean () )

renda_slider = st.slider ('Renda per Capita',
                          renda_min,
                          renda_max,
                          renda_avg
                          )


if is_check:
    #select rows
    clusters = data[data['Renda per Capita, 2000'] <  renda_slider][['Código','Município',
                        'lat', 'long',
                  'Renda per Capita, 2000','cluster']]

    #draw map
    fig = px.scatter_mapbox( clusters,
                         lat = 'lat',
                         lon = 'long',
                         color = 'cluster',
                         text = 'Município',
                         size = 'cluster',
                         color_continuous_scale = px.colors.cyclical.IceFire,
                         size_max = 15,
                         zoom = 10
                 )

    fig.update_layout(mapbox_style= 'open-street-map')
    fig.update_layout (height= 600, margin = {'r':0, 'l':0, 'b':0, 't': 0})
    st.plotly_chart( fig)
