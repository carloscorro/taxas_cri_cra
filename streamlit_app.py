import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pylab as pl
from datetime import datetime
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')

df = pd.read_csv('df.csv', sep=',', index_col=0)

lista_ativos = ['CRA', 'CRI']

#Filtrando pelo Benchmark
df_cra = df.loc[df['Código'].str.startswith('CRA', na=False)]
df_cri = df.loc[df['Código'].str.startswith('CRA', na=False) == False]

# #Criando um dataframe da quantidade de ativos por duration do CRA
# dur_anos_cra = df_cra['duration_anos'].value_counts()
# lista_qtd_cra = df_cra['duration_anos'].value_counts().to_dict()

# duration_cra = list(lista_qtd_cra.keys())
# lista_qtd_cra = list(lista_qtd_cra.values())

# dur_qtd_cra = {'Duration': duration_cra,
#         'Qtd.' : lista_qtd_cra}

# df_dur_cra = pd.DataFrame(dur_qtd_cra)
# df_dur_cra = df_dur_cra.sort_values(by='Duration', ascending=False)

# #Criando um dataframe da quantidade de ativos por duration do CRI
# dur_anos_cri = df_cri['duration_anos'].value_counts()
# lista_qtd_cri = df_cri['duration_anos'].value_counts().to_dict()

# duration_cri = list(lista_qtd_cri.keys())
# lista_qtd_cri = list(lista_qtd_cri.values())

# dur_qtd = {'Duration': duration_cri,
#         'Qtd.' : lista_qtd_cri}

# df_dur_cri = pd.DataFrame(dur_qtd)
# df_dur_cri = df_dur_cri.sort_values(by='Duration', ascending=False)

#Criando um filtro no sidebar por ativo
tipo_ativo = st.sidebar.selectbox("Ativo", lista_ativos)

col1, col2 = st.columns(2)
fig_dur_cra = px.bar(df_cra, x='duration_anos', y='duration_anos', color='Benchmark', title='CRA - Quantidade de ativos por Duration', width=580)
fig_dur_cri = px.bar(df_cri, x='duration_anos', y='duration_anos', color='Benchmark', title='CRI - Quantidade de ativos por Duration', width=580)
col1.plotly_chart(fig_dur_cra)
col2.plotly_chart(fig_dur_cri)