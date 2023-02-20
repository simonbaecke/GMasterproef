from urllib.request import urlopen
import csv
import pandas as pd

url = "https://raw.githubusercontent.com/simonbaecke/Masterproef/main/csvtest_p2.csv"
dataframe=pd.read_csv(url)
print(dataframe)


dataframe.set_index('id',inplace=True)
valueneeded = dataframe.loc['a','value']
print(valueneeded)




# invoer = urlopen(url)
# data = invoer.read().decode('utf-8')
