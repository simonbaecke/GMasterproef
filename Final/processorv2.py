import html
import math
from bs4 import BeautifulSoup
import json

local_dict = {}
endparameters=[]
errorloop = True

def convertformula(node):
    return str(html.unescape(node['name']))

with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\parameters2.json", 'r') as database:
    database = json.load(database)

bpmn = open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\BPMN\testrandom2.bpmn",'r').read()
bsdata=BeautifulSoup(bpmn,'xml')
data = bsdata.process
graphics=bsdata.BPMNPlane
start = data.startEvent

shapecolorid=[start['id']]
linecolorid=[]
wrongoutputlineid=[]
continuenext = True

next = start
while next.name != "endEvent" and errorloop:
    for node in data:
        try:
            incoming = node.find_all('incoming')
            all_incoming = [x.string for x in incoming]
            if next.outgoing.string in all_incoming:                
                if continuenext:
                    next = node
                    shapecolorid.append(next['id'])
                continuenext = True

                annotationassociation = data.find("association", attrs={"sourceRef" : next["id"]})
                if annotationassociation:
                    annotationnode = data.find("textAnnotation", attrs = {"id" : annotationassociation["targetRef"]})
                    annotation  = annotationnode.text


                if next.name == "receiveTask":
                    dataobject = data.find('dataObjectReference',attrs = {'id' : next.dataInputAssociation.sourceRef.string})
                    dataobjectid = dataobject["name"]
                    #colors
                    shapecolorid.append(dataobject["id"])
                    linecolorid.append(next.dataInputAssociation["id"])

                    if dataobjectid[-1:] == "M":
                        endparameters.append(dataobjectid)
                    else:
                        databasevalue = database[int(dataobjectid[1:])-1]['value']
                        if databasevalue:
                            local_dict[dataobjectid] = databasevalue
                        else:
                            print('nee moat')
                            errorloop = False

                elif next.name == "sendTask":
                    dataobject = data.find('dataObjectReference',attrs = {'id' : next.dataOutputAssociation.targetRef.string})
                    print(dataobject)
                    database[int(dataobject['name'][1:])-1]['value'] = local_dict[dataobject['name']]
                    #colors
                    shapecolorid.append(dataobject["id"])
                    linecolorid.append(next.dataOutputAssociation["id"])

                elif next.name == "exclusiveGateway":
                    outgoing = next.find_all('outgoing')
                    all_outgoing = [x.string for x in outgoing]
                    options = [data.find("sequenceFlow", attrs = {"id" : x}) for x in all_outgoing]
                    test_dict = dict(local_dict)
                    for flow in options:
                        formula = convertformula(flow)
                        if eval(formula,test_dict) == True:
                            print(formula)
                            next = data.find(attrs={"id" : flow['targetRef']})
                            continuenext = False
                            #colors
                            shapecolorid.append(next['id'])
              
                elif next.name == "scriptTask":
                    print('gedaan')
                    formula = convertformula(next)
                    test_dict = dict(local_dict)
                    exec(formula,test_dict,local_dict)

                elif next.name == "serviceTask":
                    formula = convertformula(next)
                    test_dict = dict(local_dict)
                    if eval(formula,test_dict) == False:
                        print(annotation.format(**local_dict))
                        errorloop = False
                      
        
        except:
            pass

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
        if shape.name == "BPMNShape" and id not in shapecolorid:
            shape['bioc:stroke']="#B7B7B7"
                # shape["bioc:fill"]="#F8F8F8"
                # shape["color:background-color"]="#F8F8F8"
            shape["color:border-color"]="#B7B7B7"
        elif shape.name == "BPMNEdge"and id not in linecolorids:
            shape['bioc:stroke']="#B7B7B7"
            shape["color:border-color"]="#B7B7B7"
    except:
        pass

print(next)
print(local_dict)

#exporteren van aangepaste database & bpmn
finished_database = json.dumps(database, indent = 4, sort_keys=True)
with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\parametersfinished.json", 'w') as json_file:
  json_file.write(finished_database)

with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\bpmnedited.bpmn","w") as new:
    new.write(str(bsdata))