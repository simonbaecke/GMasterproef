from urllib.request import urlopen

url = "https://raw.githubusercontent.com/simonbaecke/Masterproef/main/csvtest.csv"
invoer = urlopen(url)
data = invoer.read().decode('utf-8')
print(data)