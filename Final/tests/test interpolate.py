import pandas as pd
import numpy as np

# Create the dataframe from the JSON
data = {"hergebruik":[20,40],"1":[1,2],"2":[3,4],"3":[5,6],"4":[7,8]}
df = pd.DataFrame(data)

# Set the index to 'hergebruik'
df.set_index('hergebruik', inplace=True)

#input
hergebruik = input()
df.loc[hergebruik] = [np.nan for x in list(df.columns)]
hemelwaterput = input()
df[hemelwaterput]=np.nan

#convert to float and sort
df.columns = [float(x) for x in list(df.columns)]
df = df.sort_values("hergebruik")
df = df.sort_index(axis=1)

#interpolate
a = df.interpolate(method="values")
b=a.interpolate(method="values",axis=1)
print(b)
print(b.loc[hergebruik,hemelwaterput])

