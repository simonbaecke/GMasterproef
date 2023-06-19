import html
import math
from bs4 import BeautifulSoup
import json
import requests


def convertformula(node):
    return str(html.unescape(node['name']))

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\parameters2.json", 'r') as database:
    database = json.load(database)

bpmn = open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\BPMN\test parcelscale2.bpmn",'r').read()
bsdata=BeautifulSoup(bpmn,'xml')
data = bsdata.process
graphics=bsdata.BPMNPlane
start = data.startEvent

local_dict = {}
global_dict=globals()
endparameters=[] #parameters noted with M that have to be filled in in the end
errorloop = True
ms = None
shapecolorid=[start['id']]
linecolorid=[]
wrongoutputlineid = []
continuenext = True #otherwise a node is skipped after a gateway
allcallactivities = data.findAll("callActivity") #list of all microservices
print(len(allcallactivities))

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


                if next.name == "receiveTask": #validation vanuit database nog proberen te fiksen
                    dataobject = data.find('dataObjectReference',attrs = {'id' : next.dataInputAssociation.sourceRef.string})
                    dataobjectid = dataobject["name"]
                    #colors
                    shapecolorid.append(dataobject["id"])
                    linecolorid.append(next.dataInputAssociation["id"])


                    for call in allcallactivities:
                        if call.find('targetRef',string=next.dataInputAssociation.sourceRef.string):
                            ms = call
                            msurl = ms["name"]
                            print(msurl)

                    if dataobjectid[-1:] == "M":
                        endparameters.append(dataobjectid)

                    elif ms: #kleuren van associations nog doen
                        print(local_dict)
                        parameterms = data.find(attrs= {'id' : ms.dataInputAssociation.sourceRef.string})["name"]
                        print(parameterms)
                        parameterms = eval(parameterms,global_dict,local_dict)
                        print(parameterms)
                        try:             
                            response = requests.post(msurl,data=json.dumps(parameterms))
                            if response.status_code == 200:
                                msvalue = response.json()
                                local_dict[dataobjectid] = msvalue
                                database[int(dataobjectid[1:])-1]['value']= local_dict[dataobjectid]
                        
                        except:
                            print('da werkt nie he')
                            errorloop = False
                        
                        shapecolorid.append(ms["id"])
                        ms = None
                        print(local_dict)                        

                    else:
                        databasevalue = database[int(dataobjectid[1:])-1]['value']
                        print(databasevalue)
                        if databasevalue is not None:
                            local_dict[dataobjectid] = databasevalue
                        else:
                            print('nee moat da klopt hier nie he '+ dataobjectid)
                            errorloop = False
                    

                elif next.name == "sendTask":
                    dataobject = data.find('dataObjectReference',attrs = {'id' : next.dataOutputAssociation.targetRef.string})
                    database[int(dataobject['name'][1:])-1]['value'] = local_dict[dataobject['name']]
                    #colors
                    shapecolorid.append(dataobject["id"])
                    linecolorid.append(next.dataOutputAssociation["id"])

                elif next.name == "exclusiveGateway":
                    outgoing = next.find_all('outgoing')
                    all_outgoing = [x.string for x in outgoing]
                    options = [data.find("sequenceFlow", attrs = {"id" : x}) for x in all_outgoing]
                    for flow in options:
                        formula = convertformula(flow)
                        if eval(formula,global_dict,local_dict) == True:
                            print(formula)
                            next = data.find(attrs={"id" : flow['targetRef']})
                            continuenext = False
                            #colors
                            shapecolorid.append(next['id'])
                        else:
                            wrongoutputlineid.append(flow["id"])
              
                elif next.name == "scriptTask":
                    formula = convertformula(next)
                    print(formula)
                    exec(formula,global_dict,local_dict)

                elif next.name == "serviceTask":
                    formula = convertformula(next)
                    print(formula)
                    if eval(formula,global_dict,local_dict) == False:
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
    
    linecolorid = [x for x in linecolorid if x not in wrongoutputlineid]

for shape in graphics: #nog iets maken van textvakken als dat bij een shape hoort
    try:
        id = shape['bpmnElement']
        if shape.name == "BPMNShape" and id not in shapecolorid:
            shape['bioc:stroke']="#B7B7B7"
            shape["color:border-color"]="#B7B7B7"
        elif shape.name == "BPMNEdge"and id not in linecolorid:
            shape['bioc:stroke']="#B7B7B7"
            shape["color:border-color"]="#B7B7B7"
    except:
        pass

print(next)
print(local_dict)
print(endparameters)

#exporteren van aangepaste database & bpmn
finished_database = json.dumps(database, indent = 4, sort_keys=True)
with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\parametersfinished.json", 'w') as json_file:
  json_file.write(finished_database)

with open(r"C:\Users\simon_w3\OneDrive - UGent\School\Ugent\2de ma ing.-arch\Masterproef\GMasterproef\Final\tests\bpmnedited.bpmn","w") as new:
    new.write(str(bsdata))