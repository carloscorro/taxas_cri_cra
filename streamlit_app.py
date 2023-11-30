import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pylab as pl
from datetime import datetime
import streamlit as st
import plotly.express as px
import altair as alt
import numpy as np
from streamlit_option_menu import option_menu
# from numerize.numerize import numerize
# import time
# from streamlit_extras.metric_cards import style_metric_cards
# st.set_option('deprecation.showPyplotGlobalUse', False)
# import plotly.graph_objs as go

st.set_page_config(layout='wide')

df = pd.read_csv('df.csv', sep=',', index_col=0)
df_search = pd.read_csv('df_search.csv', sep=',', index_col=0)

def Home(ativo):
    
    if ativo == "CRA":
        #Filtrando pelo Benchmark
        df_cra = df.loc[df['Código'].str.startswith('CRA', na=False)]

    if ativo =="CRI":
        #Filtrando pelo Benchmark
        df_cra = df.loc[df['Código'].str.startswith('CRA', na=False) == False]

    #Filtrando pelo Benchmark
    filtro = df_cra['Benchmark'] == "IPCA +"
    df_cra_ipca = df_cra[filtro]
    filtro = df_cra['Benchmark'] == "CDI +"
    df_cra_cdi = df_cra[filtro]
    filtro = df_cra['Benchmark'] == "Pós - DI"
    df_cra_pos_di = df_cra[filtro]

    #Criando um DataFrame agrupando pela quantidade a coluna Risco de Crédito
    empresa_total = df_cra.groupby('Emissor')[['Quantidade']].sum().reset_index()
    empresa_total = empresa_total.sort_values(by='Quantidade', ascending=False).reset_index()
    empresa_total = empresa_total.head(20)
    empresa_total = empresa_total.drop(columns='index')

    emissor_total = df_cra.groupby('Risco de Crédito')[['Quantidade']].sum().reset_index()
    emissor_total = emissor_total.sort_values(by='Quantidade', ascending=False).reset_index()
    emissor_total = emissor_total.head(20)
    emissor_total = emissor_total.drop(columns='index')

    #Criando um DataFrame agrupando pela quantidade as colunas Benchmark e Duration
    benchmark_total = df_cra.groupby(['Benchmark', 'duration_anos'])[['Quantidade']].sum().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        tab1, tab2 = st.tabs(['Empresas', 'Emissores'])
        with tab1:
            chart = alt.Chart(emissor_total).mark_bar().encode(
            x=alt.X('Risco de Crédito', sort=None),
            y="Quantidade",
            )

            st.altair_chart(chart, theme="streamlit", use_container_width=True)

        with tab2:
            chart = alt.Chart(empresa_total).mark_bar().encode(
            x=alt.X('Emissor', sort=None),
            y="Quantidade",
            )

            st.altair_chart(chart, theme="streamlit", use_container_width=True)

    with col2:
        tab1, tab2 = st.tabs(['Benchmarks', 'Taxa - CDI +'])

        with tab1:
            benchmark = alt.Chart(benchmark_total).mark_bar(size=30).encode(
                x='duration_anos',
                y='Quantidade',
                color='Benchmark'
            )
            st.altair_chart(benchmark, theme='streamlit', use_container_width=True)

        with tab2:
            chart = alt.Chart(df_cra_ipca).transform_fold(
            ['Taxa Compra', 'Taxa Venda', 'Taxa Indicativa'],
            as_=['Experiment', 'Measurement']
                ).mark_bar(
            opacity=0.3,
            binSpacing=0
                ).encode(
            alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)),
            alt.Y('count()', stack=None),
            alt.Color('Experiment:N')
                )
            st.altair_chart(chart, theme="streamlit", use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        chart_ipca = alt.Chart(df_cra_ipca).mark_boxplot(size=40).encode(
        x='duration_anos',
        y='taxa')
        chart_cdi = alt.Chart(df_cra_cdi).mark_boxplot(extent='min-max').encode(
        x='duration_anos',
        y='taxa')
        chart_pos_di = alt.Chart(df_cra_pos_di).mark_boxplot(extent='min-max').encode(
        x='duration_anos',
        y='taxa')

        tab3, tab4, tab5 = st.tabs(['Taxa - IPCA +', 'Taxa - CDI +', 'Taxa - Pós DI'])

        with tab3:
            st.altair_chart(chart_ipca, theme="streamlit", use_container_width=True)
        with tab4:
            st.altair_chart(chart_cdi, theme="streamlit", use_container_width=True)
        with tab5:
            st.altair_chart(chart_pos_di, theme="streamlit", use_container_width=True)

    with col4:
        tab1, tab2, tab3 = st.tabs(['Taxa - IPCA +', 'Taxa - CDI +', 'Taxa - Pós DI'])
        
        with tab1:
            chart = alt.Chart(df_cra_ipca).mark_circle(size=60).encode(
            x='Duration',
            y='taxa',
            ).interactive()

            st.altair_chart(chart, theme='streamlit', use_container_width=True)
        with tab2:
            chart = alt.Chart(df_cra_cdi).mark_circle(size=60).encode(
            x='Duration',
            y='taxa',
            ).interactive()

            st.altair_chart(chart, theme='streamlit', use_container_width=True)
        with tab3:
            chart = alt.Chart(df_cra_pos_di).mark_circle(size=60).encode(
            x='Duration',
            y='taxa',
            ).interactive()

            st.altair_chart(chart, theme='streamlit', use_container_width=True)

def search():
    # Filtrar dados a partir do código do ativo
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    text_input = st.text_input(
    "Digite o Código do Ativo: 👇",
    placeholder="Exemplo: CRA021004NV",
    )

    if st.button("Buscar", type="primary") == True:
        if text_input == "":
            st.write('O campo está vazio. Preencha por favor.')
        else:
            if text_input in df_search['Código'].values:
                df_graph = df_search.loc[df_search['Código'] == text_input]
                df_bid_ask = df_graph[['Data', 'Taxa Compra', 'Taxa Venda']]
                # bid = df_bid_ask['Taxa Compra']
                # ask = df_bid_ask['Taxa Venda']
                # data = df_bid_ask['Data']
                # pu = df_graph['PU']
                # desvio = df_graph['Desvio Padrão']
                

                chart = alt.Chart(df_graph).mark_line().encode(
                    x=alt.X("Data"),
                    y=alt.Y("Desvio Padrão")
                )

                st.altair_chart(chart, theme="streamlit", use_container_width=True)

                # xrule = (
                #     alt.Chart()
                #     .mark_rule(color="cyan", strokeWidth=2)
                #     .encode(x=alt.datum(alt.DateTime(year=2006, month="November")))
                # )

                # yrule = (
                #     alt.Chart().mark_rule(strokeDash=[12, 6], size=2).encode(y=alt.datum(350))
                # )

                df_graph
            else:
                st.write("Código do ativo não foi encontrato na base de dados!")

    # plt.plot(data, pu, label = "PU") 
    # plt.legend() 
    # plt.show()

    # plt.plot(data, bid, label = "bid") 
    # plt.plot(data, ask, label = "ask") 
    # plt.legend() 
    # plt.show()

#Menu Bar
def sideBar():
    selected=option_menu(
        menu_title= "Dashboard - Mercado Secundário",
        options=["CRA", "CRI","Pesquisar"],
        icons=['boxes', 'buildings','search'],
        menu_icon = 'cast',
        default_index = 0,
        orientation="horizontal"
    )
    if selected=="CRA":
        papel = "CRA"
        Home(papel)

    if selected=="CRI":
        papel = "CRI"
        Home(papel)

    if selected=="Pesquisar":
        search()

sideBar()