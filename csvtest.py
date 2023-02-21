import pandas as pd

url = "https://raw.githubusercontent.com/simonbaecke/Masterproef/main/csv%20p2.csv"
dataframe=pd.read_csv(url)
print(dataframe)
ids = list(dataframe['id'])

dataframe_id = dataframe.set_index('id') #originele dataframe niet aanpassen
idvalue={}
print(list(dataframe[0]))
for letter in ids:
    idvalue[letter]=dataframe_id.loc[letter,'value']
print(idvalue)