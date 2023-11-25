import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pylab as pl
from datetime import datetime

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

# Iremos filtrar os benchmarks criando uma função
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

df['Benchmark'] = df["Índice / Correção"].apply(extrair_benchmark)
df['taxa'] = df["Índice / Correção"].apply(extrair_taxas)

filtro = df['Benchmark'] == "Pós - DI"
df_filtro = df[filtro]
df_filtro

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

#Pegando a data atual dos dados 
datas = df.Data.unique()
data_hoje = datas[-1]

#Filtrando pela dados pela data atual
df_hoje = df[df['Data'].isin([data_hoje])]

#Conferindo se há valores vazios nas colunas
# df_hoje[(df_hoje['Duration']=='')].count()
# df_hoje[(df_hoje['Desvio Padrão']=='')].count()
# df_hoje[(df_hoje['Taxa Compra']=='')].count()

#Definindo as colunas para o gráfico
coluna_a = 'Vencimento'
coluna_b = 'Desvio Padrão'

#Plotar gráfico de dispersão
plt.scatter(df_hoje[coluna_a], df_hoje[coluna_b], color='blue')
plt.xlabel(coluna_a)
plt.ylabel(coluna_b)
plt.show()

df_hoje.columns

df

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