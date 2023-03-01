import html
from bs4 import BeautifulSoup
from dataimport import idvalue
print(idvalue) #check waarden van csv

bestand = open('diagramv8.bpmn','r').read()
bsdata=BeautifulSoup(bestand,'xml')
data = bsdata.process
graphics=bsdata.BPMNPlane

start = data.startEvent

shapecolorid=[start['id']]
linecolorid=[]
wrongoutputlineid=[]

next = start
while next.name != "endEvent":
    for content in data:
        try:
            incoming = content.find_all('incoming')
            all_incoming = [x.string for x in incoming]
            if next.outgoing.string in all_incoming:
                next = content
                shapecolorid.append(next['id'])
                # print(next.prettify()) #alle nodes buiten nodes na gateway
                print(next['name'])
                #bekijken of het een gateway is, anders gewoon doorgaan
                if next.name in ["exclusiveGateway"]:
                    idgateway=next['id']
                    formula = str(html.unescape(next['name']))
                    l=1
                    while l < len(formula)-1:
                        if formula[l] in idvalue.keys() and formula[l-1] not in idvalue.keys()and formula[l+1] not in idvalue.keys():
                            formula = formula[:l]+str(idvalue[formula[l]])+formula[l+1:]
                        l+=1
                    if formula[0] in idvalue.keys() and formula[1] not in idvalue.keys():
                        formula = str(idvalue[formula[0]])+formula[1:]
                    if formula[len(formula)-1] in idvalue.keys() and formula[len(formula)-2] not in idvalue.keys():
                        formula = formula[:len(formula)-1]+str(idvalue[formula[len(formula)-1]])
                    print(formula)
                    answer = str(eval(formula))
                    for flow in data.find_all('sequenceFlow',attrs = {'sourceRef' : idgateway}):
                        if flow['name'] == answer:
                            nextflow = flow
                        else:
                            wrongoutputlineid.append(flow['id'])
                    idtarget=nextflow['targetRef']
                    next = data.find(attrs = {'id' : idtarget})
                    shapecolorid.append(next['id'])
                    # print(next.prettify()) #node na gateway
                
                #nieuwe parameters maken en toevoegen aan idvalue
                if next.name == "intermediateThrowEvent":
                    formula = str(html.unescape(next['name']))
                    for l in formula:
                        if l in idvalue.keys():
                            formula = formula.replace(l,str(idvalue[l]))
                    exec(formula)
                    idvalue[formula[0]]=eval(formula[0])

        except:
            pass
print(next.prettify())

#kleuren van tasks die niet uitgevoerd worden
for content in data:
    try:
        if content['sourceRef'] in shapecolorid and content['targetRef'] in shapecolorid:
            linecolorid.append(content['id'])
    except:
        pass
linecolorids = [x for x in linecolorid if x not in wrongoutputlineid]

for shape in graphics:
    try:
        id = shape['bpmnElement']
        if shape.name == "BPMNShape" and id not in shapecolorid and id[0:19] != "DataObjectReference":
            shape['bioc:stroke']="#831311"
            shape["bioc:fill"]="#ffcdd2"
            shape["color:background-color"]="#ffcdd2"
            shape["color:border-color"]="#831311"
        elif shape.name == "BPMNEdge"and id not in linecolorids and id[0:20] != "DataInputAssociation":
            shape['bioc:stroke']="#831311"
            shape["color:border-color"]="#831311"
    except:
        pass

# exporteren van aangepaste bpmn
with open("./Output/edited.bpmn","w") as new:
    new.write(str(bsdata))

print(idvalue)