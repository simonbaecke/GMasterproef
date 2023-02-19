import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


# tree = ET.parse('persons.xml')
# root = tree.getroot()
# names = []
# for name in tree.iter('age'):
#     print(name)
#     names.append(name.text)

# print(names)

bestand = open('diagram.bpmn','r').read()
bs_data=BeautifulSoup(bestand,'xml')
b_name = bs_data.find_all('task')
for task in b_name:
    print(type(task))
    print(task.get('name'))

b_data=bs_data.find('dataObjectReference')


# b_idk = bs_data.find('task')
# print(b_idk)
# print(b_idk.get('name'))
