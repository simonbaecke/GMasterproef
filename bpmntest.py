import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

import os
print (os.getcwd())

from csvtest import idvalue

bestand = open('diagramv2.bpmn','r').read()
bsdata=BeautifulSoup(bestand,'xml')
data = bsdata.process

#ZOEK TASKS EN MAAK DICT MET TASKID EN NAAM
# tasks = data.find_all('task')
# taskslib = {}
# for task in tasks:
#     print(task.dataInputAssociation.sourceRef.string) #bijhorende dataid
#     taskslib[task.get('id')] = task.get('name')
# print(taskslib)

start = data.startEvent
startoutgoing = start.outgoing.string
next = start
print(next.name)
while next.name != "endEvent":
    for content in data:
        try:
            if content.incoming.string == startoutgoing:
                next = content.incoming.parent
                next = data.endEvent
        except:
            pass
print(next)










# start_outgoingstring = start.outgoing.text
# print(start_outgoingstring)

# next = bsdata.find_all(string=start_outgoingstring)
# inenuit = []


# for tag in next:
#     print(tag.parent.parent.prettify())
#     inenuit.append(tag.parent.parent)
# # print(inenuit)
# for tag in inenuit:
#     a = tag.find('incoming',string=start_outgoingstring)
#     if a is not None:
#         print(a.prettify())
#     # if a.string == start_outgoingstring:
#     #     print('yes')