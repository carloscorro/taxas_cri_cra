import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pylab as pl
from datetime import datetime
import streamlit as st
import plotly.express as px

df = pd.read_csv('df.csv', sep=',', index_col=0)
df

#Filtrando pelo Benchmark
df_cra = df.loc[df['Código'].str.startswith('CRA', na=False)]
df_cra
df_cri = df.loc[df['Código'].str.startswith('CRA', na=False) == False]
df_cri

#Criando um dataframe da quantidade de ativos por duration
dur_anos = df['duration_anos'].value_counts()
lista_qtd = df['duration_anos'].value_counts().to_dict()

duration = list(lista_qtd.keys())
lista_qtd = list(lista_qtd.values())

dur_qtd = {'Duration': duration,
        'Qtd.' : lista_qtd}

df_dur = pd.DataFrame(dur_qtd)
df_dur = df_dur.sort_values(by='Duration', ascending=False)

###
lista_ativo = ['CRA', 'CRI']

tipo_ativo = st.sidebar.selectbox("Ativo", lista_ativo)

col1, col2, col3 = st.columns(3)
fig_dur = px.bar(df_dur, x='Duration', y='Qtd.', title='Quantidade de ativos negociados por duration')
col1.plotly_chart(fig_dur)