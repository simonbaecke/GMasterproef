import html
from bs4 import BeautifulSoup

from csvtest import idvalue

bestand = open('diagramv5.bpmn','r').read()
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
# startoutgoing = start.outgoing.string
print(idvalue)
next = start
while next.name != "endEvent":
    for content in data:
        try:
            if content.incoming.string == next.outgoing.string:
                x = next['name'] #afhankelijk van hoe men formule opstelt ofwel verandert men eerste waarde door juiste waarde ofwel checkt men via x welke waarde moet getoestst worden aangezien dit voor de gateway komt 
                next = content.incoming.parent
                print(next.prettify())
                if next.name in ["exclusiveGateway","bla"]:
                    idgateway=next['id']
                    print(idgateway)
                    formula = str(html.unescape(next['name']))
                    value = idvalue[formula[0]]
                    formula = formula.replace(formula[0],str(value))
                    answer = str(eval(formula))
                    nextevent = data.find('sequenceFlow',attrs = {'sourceRef' : idgateway,'name':answer})
                    idtarget=nextevent['targetRef']
                    next = data.find(attrs = {'id' : idtarget})
                    print(next)
        except:
            pass










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