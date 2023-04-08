bpmnnames = ["gebouw","perceel"]
import html
import math
import json
from bs4 import BeautifulSoup
import pandas as pd

from flask import (Blueprint, jsonify, request)

bp = Blueprint('bpmn',__name__)
@bp.route('/bpmn', methods=['GET','POST'])



def bpmn():

    dataframe=pd.read_csv("./public/parameters.csv")
    ids = list(dataframe['id'])

    dataframe_id = dataframe.set_index('id') #originele dataframe niet aanpassen
    idvalue={}
    for letter in ids:
        idvalue[letter]=dataframe_id.loc[letter,'value']


    keys='AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn'

    def round_up(n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

    def convertformula(database,source):
        formula = str(html.unescape(source))
        i=1
        while i < len(formula)-1:
            if formula[i] in database.keys() and formula[i-1] not in keys and formula[i+1] not in keys:
                formula = formula[:i]+str(database[formula[i]])+formula[i+1:]
            i+=1
        if formula[0] in database.keys() and formula[1] not in keys:
            formula = str(database[formula[0]])+formula[1:]
        if formula[len(formula)-1] in database.keys() and formula[len(formula)-2] not in keys:
            formula = formula[:len(formula)-1]+str(database[formula[len(formula)-1]])
        
        return formula

    for diagram in bpmnnames:
        bestand = open("./public/" +diagram+".bpmn",'r').read()
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

                        #bekijken of het een gateway is, anders gewoon doorgaan
                        while next.name in ["exclusiveGateway","intermediateThrowEvent"]:
                            nota = data.find('association',attrs = {'sourceRef' : next['id']})
                            noto = data.find('textAnnotation',attrs = {'id' : nota['targetRef']})
                            shapecolorid.append(noto['id'])
                            print(noto.text)
                            idgateway=next['id']
                            formula = convertformula(idvalue,noto.text)
                            print(formula)
                            if next.name == "exclusiveGateway":
                                answer = str(eval(formula))
                                print(answer)
                                for flow in data.find_all('sequenceFlow',attrs = {'sourceRef' : idgateway}):
                                    if flow['name'] == answer:
                                        nextflow = flow
                                    else:
                                        wrongoutputlineid.append(flow['id'])
                                idtarget=nextflow['targetRef']
                                next = data.find(attrs = {'id' : idtarget})
                                shapecolorid.append(next['id'])
                            else:
                                exec(formula)
                                idvalue[formula[1]]=eval(formula[1])
                                break
                                

                except:
                    pass
        print(next)

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
                    shape['bioc:stroke']="#B7B7B7"
                    # shape["bioc:fill"]="#F8F8F8"
                    # shape["color:background-color"]="#F8F8F8"
                    shape["color:border-color"]="#B7B7B7"
                elif shape.name == "BPMNEdge"and id not in linecolorids and id[0:20] != "DataInputAssociation":
                    shape['bioc:stroke']="#B7B7B7"
                    shape["color:border-color"]="#B7B7B7"
            except:
                pass

        # exporteren van aangepaste bpmn
        with open("./public/" + diagram + "edited.bpmn","w") as new:
            new.write(str(bsdata))
        print(idvalue)
        
        
    for value in idvalue:
        if value.isupper():
            print(value + ": " + str(idvalue[value]))

    return json.dumps(idvalue)