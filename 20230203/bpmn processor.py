import html
from bs4 import BeautifulSoup
from getCSV import idvalue
print(idvalue) #check waarden van csv

def convertformula(database,source):
    formula = str(html.unescape(source))
    i=1
    while i < len(formula)-1:
        if formula[i] in database.keys() and formula[i-1] not in database.keys()and formula[i+1] not in database.keys():
            formula = formula[:i]+str(database[formula[i]])+formula[i+1:]
        i+=1
    if formula[0] in database.keys() and formula[1] not in database.keys():
        formula = str(database[formula[0]])+formula[1:]
    if formula[len(formula)-1] in database.keys() and formula[len(formula)-2] not in database.keys():
        formula = formula[:len(formula)-1]+str(database[formula[len(formula)-1]])
    
    return formula

bestand = open('diagramdef.bpmn','r').read()
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
                nota = data.find('association',attrs = {'sourceRef' : next['id']})
                if nota:
                    noto=data.find('textAnnotation',attrs = {'id' : nota['targetRef']})
                    shapecolorid.append(noto['id'])
                    print(noto.text)
                
                next = content
                shapecolorid.append(next['id'])

                #bekijken of het een gateway is, anders gewoon doorgaan
                while next.name == "exclusiveGateway":
                    idgateway=next['id']
                    formula = convertformula(idvalue,next['name'])
                    answer = str(eval(formula))
                    for flow in data.find_all('sequenceFlow',attrs = {'sourceRef' : idgateway}):
                        if flow['name'] == answer:
                            nextflow = flow
                        else:
                            wrongoutputlineid.append(flow['id'])
                    idtarget=nextflow['targetRef']
                    next = data.find(attrs = {'id' : idtarget})
                    shapecolorid.append(next['id'])
                
                #nieuwe parameters maken en toevoegen aan idvalue
                if next.name == "intermediateThrowEvent":
                    formula = convertformula(idvalue,next['name'])
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