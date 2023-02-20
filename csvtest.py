from urllib.request import urlopen
import csv
import pandas as pd

url = "https://raw.githubusercontent.com/simonbaecke/Masterproef/main/csv%20p2.csv"
dataframe=pd.read_csv(url)
print(dataframe)


dataframe.set_index('id',inplace=True)
empty = {}
for letter in 'abcdef':
    print(letter)
    empty[letter]=dataframe.loc[letter,'value']
a = dataframe.loc['a','value']
print(empty)




# invoer = urlopen(url)
# data = invoer.read().decode('utf-8')
