import pandas as pd

payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
first_table = payload[0]
second_table = payload[1]

df = first_table

df.to_csv("S&P500-Symbols.csv", columns=['Symbol'] ,index=False,header=False)
