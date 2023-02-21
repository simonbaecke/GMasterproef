import html
from bs4 import BeautifulSoup

from data import idvalue

bestand = open('diagramv3.bpmn','r').read()
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
print(idvalue)
next = start
while next.name != "endEvent":
    for content in data:
        try:
            incoming = content.find_all('incoming')
            all_incoming = [x.string for x in incoming]
            if next.outgoing.string in all_incoming:
                # x = next['name'] #afhankelijk van hoe men formule opstelt ofwel verandert men eerste waarde door juiste waarde ofwel checkt men via x welke waarde moet getoestst worden aangezien dit voor de gateway komt 
                next = content
                # print(next.prettify()) #alle nodes buiten nodes na gateway
                
                #bekijken of het een gateway is, anders gewoon doorgaan
                if next.name in ["exclusiveGateway","x","y"]:
                    idgateway=next['id']
                    formula = str(html.unescape(next['name']))
                    value = idvalue[formula[0]]
                    formula = formula.replace(formula[0],str(value))
                    answer = str(eval(formula))
                    nextevent = data.find('sequenceFlow',attrs = {'sourceRef' : idgateway,'name':answer})
                    idtarget=nextevent['targetRef']
                    next = data.find(attrs = {'id' : idtarget})
                    # print(next.prettify()) #node na gateway
        except:
            pass

print(next.prettify())










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