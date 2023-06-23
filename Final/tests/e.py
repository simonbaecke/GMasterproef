import math
import json

dic = {'a':50, 'b': 60}

lala = "a-b"
print(lala.format(**dic))

for key,value in dic.items():
    lala = lala.replace(key,str(value))
  
print(lala)