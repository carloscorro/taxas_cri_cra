import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.anbima.com.br/pt_br/informar/precos-e-indices/precos/taxas-de-cri-e-cra/taxas-de-cri-e-cra.htm"
r = requests.get(url)

soup = BeautifulSoup(r.text, "lxml")

table = soup.find("table", class_ = "custom-anbi-ui-table")

headers = table.find_all("th")

# print(headers)

titles = []

for i in headers:
    title = i.text
    titles.append(title)

df = pd.DataFrame(columns=titles)

rows = table.find_all("tr")

for i in rows[1:]:
    data = i.find_all("td")
    row = [tr.text for tr in data]
    l = len(df)
    df.loc[l] = row

print(df)



# print(titles)