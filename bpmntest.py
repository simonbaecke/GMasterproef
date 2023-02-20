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
start = bs_data.startEvent
print(start['name'])

start_outgoingstring = start.outgoing.text
print(start_outgoingstring)

next = bs_data.find_all(string=start_outgoingstring)
inenuit = []

for tag in next:
    # print(tag.parent.parent.prettify())
    inenuit.append(tag.parent.parent)
# print(inenuit)
for tag in inenuit:
    a = tag.find('incoming',string=start_outgoingstring)
    if a is not None:
        print(a.prettify())
    # if a.string == start_outgoingstring:
    #     print('yes')
# b_name = bs_data.find_all('task')
# for task in b_name:
#     print(type(task))
#     print(task.get('name'))

# b_data=bs_data.find('dataObjectReference')


# b_idk = bs_data.find('task')
# print(b_idk)
# print(b_idk.get('name'))
