import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pylab as pl
from datetime import datetime
import streamlit as st
import plotly.express as px
import altair as alt
import numpy as np

st.set_page_config(layout='wide')

df = pd.read_csv('df.csv', sep=',', index_col=0)

df['Quantidade'] = np.where(df['Benchmark'] == 'IPCA +', 1, 1)

lista_ativos = ['CRA', 'CRI']

#Filtrando pelo Benchmark
df_cra = df.loc[df['Código'].str.startswith('CRA', na=False)]
df_cri = df.loc[df['Código'].str.startswith('CRA', na=False) == False]

#Filtrando pelo Benchmark
filtro = df_cra['Benchmark'] == "IPCA +"
df_cra_ipca = df_cra[filtro]
filtro = df_cra['Benchmark'] == "CDI +"
df_cra_cdi = df_cra[filtro]
filtro = df_cra['Benchmark'] == "Pós - DI"
df_cra_pos_di = df_cra[filtro]

df_cra_ipca = df_cra_ipca.round(decimals=0)
df_cra_cdi = df_cra_cdi.round(decimals=0)
df_cra_pos_di = df_cra_pos_di.round(decimals=0)

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
# tipo_ativo = st.sidebar.selectbox("Ativo", lista_ativos)

emissor_total = df.groupby('Risco de Crédito')[['Quantidade']].sum().reset_index()
emissor_total = emissor_total.sort_values(by='Quantidade', ascending=False).reset_index()
emissor_total = emissor_total.head(10)
emissor_total = emissor_total.drop(columns='index')

benchmark_total = df_cra.groupby(['Benchmark', 'duration_anos'])[['Quantidade']].sum().reset_index()

col1, col2 = st.columns(2)

with col1:
    tab1, tab2 = st.tabs(['Top 10 - Emissores', 'CRI'])
    with tab1:
        chart = alt.Chart(emissor_total).mark_bar().encode(
        x='Risco de Crédito',
        y="Quantidade",
        )

        st.altair_chart(chart, theme="streamlit", use_container_width=True)

with col2:
    chart_ipca = alt.Chart(df_cra_ipca).mark_boxplot(extent='min-max').encode(
        x='taxa',
        y='duration_anos')
    chart_cdi = alt.Chart(df_cra_cdi).mark_boxplot(extent='min-max').encode(
        x='taxa',
        y='duration_anos')
    chart_pos_di = alt.Chart(df_cra_pos_di).mark_boxplot(extent='min-max').encode(
        x='taxa',
        y='duration_anos')

    tab3, tab4, tab5 = st.tabs(['Taxa - IPCA +', 'Taxa - CDI +', 'Taxa - Pós DI'])

    with tab3:
        st.altair_chart(chart_ipca, theme="streamlit", use_container_width=True)
    with tab4:
        st.altair_chart(chart_cdi, theme="streamlit", use_container_width=True)
    with tab5:
        st.altair_chart(chart_pos_di, theme="streamlit", use_container_width=True)

col3, col4 = st.columns(2)

with col3:
        benchmark = alt.Chart(benchmark_total).mark_bar(size=40).encode(
            x='duration_anos',
            y='Quantidade',
            color='Benchmark'
        )
        st.altair_chart(benchmark, theme='streamlit', use_container_width=True)
        # fig_dur_cra = px.bar(df_cra, x='duration_anos', y='Quantidade', color='Benchmark')
        # # fig_dur_cri = px.bar(df_cri, x='duration_anos', y='duration_anos', color='Benchmark', title='CRI - Quantidade de ativos por Duration', width=580)
        # col1.plotly_chart(fig_dur_cra)
        # # col2.plotly_chart(fig_dur_cri)