import html
from bs4 import BeautifulSoup

from data import idvalue
print(idvalue) #check waarden van csv


bestand = open('diagramv3.bpmn','r').read()
bsdata=BeautifulSoup(bestand,'xml')
data = bsdata.process
graphics=bsdata.BPMNPlane

start = data.startEvent

shapecolorid=[start['id']]
linecolorid=[]

next = start
while next.name != "endEvent":
    for content in data:
        try:
            incoming = content.find_all('incoming')
            all_incoming = [x.string for x in incoming]
            if next.outgoing.string in all_incoming:
                # x = next['name'] #afhankelijk van hoe men formule opstelt ofwel verandert men eerste waarde door juiste waarde ofwel checkt men via x welke waarde moet getoestst worden aangezien dit voor de gateway komt 
                if next.name == "intermediateThrowEvent": #info weergeven
                    print(next['name'])
                next = content
                shapecolorid.append(next['id'])
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
                    shapecolorid.append(next['id'])
                    # print(next.prettify()) #node na gateway
        except:
            pass
print(next.prettify())

for content in data:
    try:
        if content['sourceRef'] in shapecolorid and content['targetRef'] in shapecolorid:
            linecolorid.append(content['id'])
    except:
        pass

#kleuren van tasks die niet uitgevoerd worden
for shape in graphics:
    try:
        id = shape['bpmnElement']
        if shape.name == "BPMNShape" and id not in shapecolorid and id[0:19] != "DataObjectReference":
            shape['bioc:stroke']="#831311"
            shape["bioc:fill"]="#ffcdd2"
            shape["color:background-color"]="#ffcdd2"
            shape["color:border-color"]="#831311"
        elif shape.name == "BPMNEdge"and id not in linecolorid and id[0:20] != "DataInputAssociation":
            shape['bioc:stroke']="#831311"
            shape["color:border-color"]="#831311"
    except:
        pass


with open("edited.bpmn","w") as new:
    new.write(str(bsdata))

