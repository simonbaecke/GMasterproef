import pandas as pd

url = "https://raw.githubusercontent.com/simonbaecke/Masterproef/main/csv%20p2.csv"
dataframe=pd.read_csv("./public/parameters.csv")
ids = list(dataframe['id'])

dataframe_id = dataframe.set_index('id') #originele dataframe niet aanpassen
idvalue={}
for letter in ids:
    idvalue[letter]=dataframe_id.loc[letter,'value']