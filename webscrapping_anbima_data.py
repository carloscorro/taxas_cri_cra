import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pylab as pl
from datetime import datetime
import numpy as np

#Aqui fazemos o request do link
url = "https://www.anbima.com.br/pt_br/informar/precos-e-indices/precos/taxas-de-cri-e-cra/taxas-de-cri-e-cra.htm"
r = requests.get(url)

soup = BeautifulSoup(r.text, "lxml")

table = soup.find("table", class_ = "custom-anbi-ui-table")

#Separamos os títulos da tabela e Criamos o Data Frame colocando os Títulos
headers = table.find_all("th")

titles = []

for i in headers:
    title = i.text
    titles.append(title)

df = pd.DataFrame(columns=titles)

#Separamos as linhas da tabela e fazemos a concatação junto ao Data Frame
rows = table.find_all("tr")

for i in rows[1:]:
    data = i.find_all("td")
    row = [tr.text for tr in data]
    l = len(df)
    df.loc[l] = row

#Renomeando coluna da Data
df = df.rename(columns={'Data de Referência' : 'Data'})

#Investendo os dados pela data
df = df[::-1]

#Converter colunas de datas que estão em STR para DateTime
formato = "%d/%M/%Y"
df_data = df.Data.apply(lambda linha: datetime.strptime(linha, formato).date())
df['Data'] = df_data
df_vencimento = df.Vencimento.apply(lambda linha: datetime.strptime(linha, formato).date())
df['Vencimento'] = df_vencimento

#Convertendo as colunas de Str para Float
def converter_float(dp):
    if dp != "":
        return float(dp)
    else:
        return ""

lista_colunas = ['Taxa Compra', 'Taxa Venda', 'Taxa Indicativa', 'Desvio Padrão', 'PU', '% PU Par', 'Duration']

for coluna in lista_colunas:
    #Convertendo os valores da coluna de Str para Float
    df[coluna] = df[coluna].str.replace(',','.')
    df[coluna] = df[coluna].apply(converter_float)
    #Eliminando valores vazios do dataframe
    filtro = df[coluna] != ''
    df = df[filtro]

#Fltrar os benchmarks atráves de uma função
pos_ipca ="IPCA"
pos_cdi = "DI"
hibrido_ipca = "IPCA"
hibrido_cdi = "DI"

def extrair_benchmark(Benchmark):
    if Benchmark.endswith(pos_ipca) == True:
        return "Pós - IPCA"
    elif Benchmark.endswith(pos_cdi) == True:
        return "Pós - DI"
    elif Benchmark.startswith(hibrido_ipca) == True:
        return "IPCA +"
    elif Benchmark.startswith(hibrido_cdi) == True:
        return "CDI +"
    else:
        return ""

#Extrair as taxas atráves de uma função
def extrair_taxas(Benchmark):
    if Benchmark.endswith(pos_ipca) == True:
        return "Pós - IPCA"
    elif Benchmark.endswith(pos_cdi) == True:
        taxa = Benchmark[0:-7]
        return taxa
    elif Benchmark.startswith(hibrido_ipca) == True:
        taxa = Benchmark[6:-1]
        return taxa
    elif Benchmark.startswith(hibrido_cdi) == True:
        taxa = Benchmark[5:-1]
        return taxa
    else:
        return ""
    
#Sumarizar duration em anos

def duration_em_anos(duration):
    if duration < 252:
        return 1
    elif duration > 252 and duration <= 504:
        return 2
    elif duration > 504 and duration <= 756:
        return 3
    elif duration > 756 and duration <= 1008:
        return 4
    elif duration > 1008 and duration <= 1260:
        return 5
    elif duration > 1260 and duration <= 1512:
        return 6
    elif duration > 1512 and duration <= 1764:
        return 7
    elif duration > 1764 and duration <= 2016:
        return 8
    elif duration > 2016 and duration <= 2268:
        return 9
    elif duration > 2268 and duration <= 2520:
        return 10
    elif duration > 2520 and duration <= 2772:
        return 11
    else:
        return 12
    
df['Benchmark'] = df["Índice / Correção"].apply(extrair_benchmark)
df['taxa'] = df["Índice / Correção"].apply(extrair_taxas)
df['duration_anos'] = df["Duration"].apply(duration_em_anos)

coluna = 'taxa'
#Convertendo os valores da coluna de Str para Float
df[coluna] = df[coluna].str.replace(',','.')
df[coluna] = df[coluna].apply(converter_float)
#Eliminando valores vazios do dataframe
filtro = df[coluna] != ''
df = df[filtro]

#Criando uma coluna Quantidade que irá ter o valor 1
df['Quantidade'] = np.where(df['Benchmark'] == 'IPCA +', 1, 1)

#Pegando a data atual dos dados 
datas = df.Data.unique()
data_hoje = datas[-1]

#Filtrando os dados pela data atual
df_hoje = df[df['Data'].isin([data_hoje])]

#Criando CSV do DataFrame tratado
df_hoje.to_csv("df.csv")

######################=================#####################

# #Filtrando pelo Benchmark
# filtro = df['Benchmark'] == "Pós - DI"
# df_filtro = df[filtro]
# df_filtro

#Conferindo se há valores vazios nas colunas
# df_hoje[(df_hoje['Duration']=='')].count()
# df_hoje[(df_hoje['Desvio Padrão']=='')].count()
# df_hoje[(df_hoje['Taxa Compra']=='')].count()

# #Definindo as colunas para o gráfico
# dados_x = 'duration_anos'
# dados_y = df['duration_anos'].value_counts()

# #Plotar gráfico de dispersão
# plt.scatter(df_hoje[dados_x], df_hoje[dados_y], color='blue')
# plt.xlabel(dados_x)
# plt.ylabel(dados_y)
# plt.show()

# df_hoje.columns

# FILTRANDO COLUNA POR CONDIÇÃO
# busca = ['']
# df = df[df['Desvio Padrão'].isin(busca)]

#Filtrar dados a partir do código do ativo
# filtro_cra = 'CRA021004NV'

# df_graph = df.loc[df['Código'] == filtro_cra]
# df_bid_ask = df_graph[['Data', 'Taxa Compra', 'Taxa Venda']]
# bid = df_bid_ask['Taxa Compra']
# ask = df_bid_ask['Taxa Venda']
# data = df_bid_ask['Data']
# pu = df_graph['PU']
# desvio = df_graph['DP']

# plt.plot(data, desvio, label = "Desvio Padrão") 
# plt.legend() 
# plt.show()

# plt.plot(data, pu, label = "PU") 
# plt.legend() 
# plt.show()

# plt.plot(data, bid, label = "bid") 
# plt.plot(data, ask, label = "ask") 
# plt.legend() 
# plt.show()

# print(df_graph.columns)
# print(df_graph[['Data', 'PU']])