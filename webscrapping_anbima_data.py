import requests
import pandas as pd
from bs4 import BeautifulSoup

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

# Iremos filtrar os benchmarks 
pos_ipca ="IPCA"
pos_cdi = "DI"
hibrido_ipca = "IPCA"
hibrido_cdi = "DI"
  
# boolean series retornan com Falso no lugar de NaN 
bool_series_pos_ipca = df["Índice / Correção"].str.endswith(pos_ipca, na = False)
bool_series_pos_cdi = df["Índice / Correção"].str.endswith(pos_cdi, na = False)
bool_series_hibrido_ipca = df["Índice / Correção"].str.endswith(hibrido_ipca, na = False)
bool_series_hibrido_cdi = df["Índice / Correção"].str.endswith(hibrido_cdi, na = False)

df_pos_fixado = df[bool_series_pos_ipca]

print(df_pos_fixado["Índice / Correção"])
print(len(df_pos_fixado))