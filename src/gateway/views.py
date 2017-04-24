from django.shortcuts import render
import requests
from requests import Session
import json
from django.views.decorators.csrf import csrf_exempt
import math

# Create your views here.
def home(request):
    #return HttpResponse("Hola Main")
    #return render(request, "main/home.html")

    return render(request,"gateway/home.html")


def getDevicesCMTS(request):

   urlGetDevicesCMTS = "http://localhost:5052/getDevicesGroup/CMTS/"
   headers = {'Accept': 'application/data+json'}
   req = requests.get(urlGetDevicesCMTS, headers=headers)

   devicesCMTS = req.json()
   devicesCMTS = {"cmts": devicesCMTS}
   devicesCMTS = json.dumps(devicesCMTS)
   context = {
       #'devicesCMTS': '["cbr8-0", "cbr8-1"]'
       'devicesCMTS': devicesCMTS
   }
   return render(request,"gateway/devicesCMTS.html",context)

def getDevicesPE(request):
   urlGetDevicesPE = "http://localhost:5052/getDevicesGroup/PE/"
   headers = {'Accept': 'application/data+json'}
   req = requests.get(urlGetDevicesPE, headers=headers)
   devicesPE = req.json()
   devicesPE = {"pe": devicesPE}
   devicesPE = json.dumps(devicesPE)
   context = {
       #'devicesCMTS': '["cbr8-0", "cbr8-1"]'
       'devicesCMTS': devicesPE
   }
   return render(request,"gateway/devicesCMTS.html",context)

def setLoadBalance(request, cmts,d2LoadBalance,d3LoadBalance):

   urlSetLoadBalance = "http://localhost:5051/setLoadBalance/"+cmts+"/"+d2LoadBalance+"/"+d3LoadBalance
   headers = {'Accept': 'application/data+json'}
   #req = \
   requests.get(urlSetLoadBalance, headers=headers)


   context = {
       #'devicesCMTS': '["cbr8-0", "cbr8-1"]'
       'devicesCMTS': "OK"
   }
   return render(request,"gateway/devicesCMTS.html",context)

@csrf_exempt
def setControllerIntegratedCable(request,numSG,numArq):

    linecards=["1","2","3","6","7","8","9"]

    data=request.body
    data_string=data.decode('utf-8')
    data_Substring=data_string[1:len(data_string)]

    body_data = json.loads(data_string)
    #data_string=json.dumps(body_data, sort_keys=False)

    device=body_data['device']
    numSG=int(numSG)

    if(numArq=="1"):
        numLineCards=math.ceil(numSG/8);
    if(numArq=="2"):
        numLineCards = math.ceil(numSG*2/16);
    if (numArq == "4"):
        numLineCards = math.ceil(numSG *4/16);

    resultado={}

    for x in range(0, numLineCards):
        print(x)
        card=linecards[x]
        serviceInstanceName = device + "_" + card + "-0-0_contIntegratedCable"
        cardName= '"card": '+ '"' + card + '"'
        serviceData = cardName + "," + data_Substring
        service = '{"controllerIntegratedCable:controllerIntegratedCable": [' \
                  '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
        print(service)
        urlSetControllerIntegratedCable = "http://localhost:5054/setService/controllerIntegratedCable/" + serviceInstanceName
        print(urlSetControllerIntegratedCable)

        headers = {'Content-Type': 'application/vnd.yang.data+json'}
        s = Session()
        req = requests.Request('POST', urlSetControllerIntegratedCable,
                               data=service,
                               headers=headers
                               )
        prepped = s.prepare_request(req)
        resp = s.send(prepped)

        print("respuesta======================>")
        algo= resp.text
        algo= json.dumps(algo)
        algo=type(algo)
        respuesta={card:resp.text}
        #respuesta = {card: service}
        print(respuesta)
        print("statuscode======================>")
        print(algo)
        resultado.update(respuesta)

    print("resultado======================>")
    print(resultado)
    context = {'devicesCMTS': resultado}
    return render(request, "gateway/devicesCMTS.html", context)

    card=body_data['card']
    serviceInstanceName=device+"_"+card+"-0-0_contIntegratedCable"

    #context = {'devicesCMTS': serviceInstanceName}
    #return render(request, "gateway/devicesCMTS.html", context)


    #service.update(body_data)
    #service= dict(service, **body_data)



    # Arch 1:1
    # ptoDS = PtoUS
    # 0  = 0
    # 1 = 2
    # 2 = 4
    # 3 = 6
    # 4 = 8
    # 5 = 10
    # 6 = 12
    # 7 = 14

    # Arch 1:2
    # ptoDS = PtoUS
    # 0  = 0,1
    # 1 = 2,3
    # 2 = 4,5
    # 3 = 6,7
    # 4 = 8,9
    # 5 = 10,11
    # 6 = 12,13
    # 7 = 14,15

    # Arch 1:4
    # ptoDS = PtoUS
    # 0 = 0,1,2,3
    # 1 = 4,5,6,7
    # 2 = 8,9,10,11
    # 3 = 12,13,14,15


@csrf_exempt
def setControllerUpstreamCable(request,numSG,numArq):

    linecards=["1","2","3","6","7","8","9"]
    ptosUS1 = ["0","2","4","6","8","10","12","14"]
    ptosUS2 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14"]
    ptosUS4 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]



    data=request.body
    data_string=data.decode('utf-8')
    data_Substring=data_string[1:len(data_string)]

    body_data = json.loads(data_string)
    #data_string=json.dumps(body_data, sort_keys=False)

    device=body_data['device']
    numSG=int(numSG)

    if(numArq=="1"):
        numLineCards=math.ceil(numSG/8)
        ptoUS = ptosUS1
    if(numArq=="2"):
        numLineCards = math.ceil(numSG*2/16)
        ptoUS = ptosUS2
    if (numArq == "4"):
        numLineCards = math.ceil(numSG *4/16)
        ptoUS = ptosUS4

    resultado={}

    for x in range(0, numLineCards):
        print(x)
        card=linecards[x]
        cardName = '"card": ' + '"' + card + '"'
        for y in range(0,len(ptoUS)):
            print(y)
            pto=ptoUS[y]
            serviceInstanceName = device + "_" + card + "-0-"+pto+"_contUpstream"
            portName = '"port": ' + '"' + pto + '"'
            serviceData = cardName + "," + portName + "," + data_Substring
            service = '{"controllerUpstreamCable:controllerUpstreamCable": [' \
                  '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
            print(service)
            urlSetControllerUpstreamCable = "http://localhost:5054/setService/controllerUpstreamCable/" + serviceInstanceName
            print(urlSetControllerUpstreamCable)
            headers = {'Content-Type': 'application/vnd.yang.data+json'}
            s = Session()
            req = requests.Request('POST', urlSetControllerUpstreamCable,
                               data=service,
                               headers=headers
                               )
            prepped = s.prepare_request(req)
            resp = s.send(prepped)
            respuesta={card+"-"+pto:resp.text}
            #respuesta = {card: service}
            resultado.update(respuesta)


    context = {'devicesCMTS': resultado}
    #context = {'devicesCMTS': "OK"}
    return render(request, "gateway/devicesCMTS.html", context)

@csrf_exempt
def setInterfaceCable(request,numSG,numArq,numUS):

    linecards=["1","2","3","6","7","8","9"]
    ptosDS = ["0","1","2","3","4","5","6","7"]

    numUS = int(numUS)
    usString=""
    for i in range(0, numUS):
        iStr = str(i)
        usString = usString + '"us' + iStr + '": "' + iStr + '",'
    usString = usString[0:len(usString)-1]


    data=request.body
    data_string=data.decode('utf-8')
    data_Substring=data_string[1:len(data_string)]

    body_data = json.loads(data_string)
    #data_string=json.dumps(body_data, sort_keys=False)

    device=body_data['device']
    numSG=int(numSG)

    if(numArq=="1"):
        numLineCards=math.ceil(numSG/8)

    if(numArq=="2"):
        numLineCards = math.ceil(numSG*2/16)

    if (numArq == "4"):
        numLineCards = math.ceil(numSG *4/16)

    #"idBondingGroup1": "30000",



    resultado={}

    for x in range(0, numLineCards):
        print(x)
        card=linecards[x]
        cardName = '"card": ' + '"' + card + '"'
        for y in range(0,len(ptosDS)):
            print(y)
            pto=ptosDS[y]
            serviceInstanceName = device + "_" + card + "-0-"+pto+"_intCable"
            portName = '"dsPort": ' + '"' + pto + '"'
            numCard=int(card)
            numPort=int(pto)
            idBondingGroup1 = numCard*10000+numPort*10
            idBondingGroup1 = str(idBondingGroup1)
            bondingData= '"idBondingGroup1": "' + idBondingGroup1 + '"'

            if (numArq == "2"):
                idBondingGroup2 = numCard * 10000 + numPort * 10 +1
                idBondingGroup2 = str(idBondingGroup2)
                bondingData2 = '"idBondingGroup2": "' + idBondingGroup2 + '"'
                bondingData = bondingData + ", " + bondingData2


            serviceData = cardName + "," + portName + "," + bondingData + "," + usString + "," + data_Substring
            service = '{"interfaceCable:interfaceCable": [' \
                  '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
            print(service)


            urlSetInterfaceCable = "http://localhost:5054/setService/interfaceCable/" + serviceInstanceName
            print(urlSetInterfaceCable)
            headers = {'Content-Type': 'application/vnd.yang.data+json'}
            s = Session()
            req = requests.Request('POST', urlSetInterfaceCable,
                               data=service,
                               headers=headers
                               )
            prepped = s.prepare_request(req)
            resp = s.send(prepped)
            respuesta={card+"-"+pto:resp.text}
            #respuesta = {card: service}
            resultado.update(respuesta)


    context = {'devicesCMTS': resultado}
    #context = {'devicesCMTS': "OK"}
    return render(request, "gateway/devicesCMTS.html", context)


@csrf_exempt
def setIntIntegratedCable(request,numSG, numArq,numDS):

    linecards=["1","2","3","6","7","8","9"]
    ptosDS = ["0", "1", "2", "3", "4", "5", "6", "7"]

    data=request.body
    data_string=data.decode('utf-8')
    data_Substring=data_string[1:len(data_string)]

    body_data = json.loads(data_string)
    #data_string=json.dumps(body_data, sort_keys=False)

    device=body_data['device']
    numSG=int(numSG)

    if(numArq=="1"):
        numLineCards=math.ceil(numSG/8)

    if(numArq=="2"):
        numLineCards = math.ceil(numSG*2/16)

    if (numArq == "4"):
        numLineCards = math.ceil(numSG *4/16)

    numDSperSG=int(numDS)

    resultado={}

    for x in range(0, numLineCards):
        print(x)
        card=linecards[x]
        cardName = '"card": ' + '"' + card + '"'
        for y in range(0,len(ptosDS)):
            print(y)
            pto=ptosDS[y]
            portName = '"dsPort": ' + '"' + pto + '"'




            for z in range(0,numDSperSG):

                serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(z) + "_intIntegratedCable"
                dsNumName = '"DSnum": ' + '"' + str(z) + '"'

                serviceData = cardName + "," + portName + "," + dsNumName + "," + data_Substring
                service = '{"intIntegratedCable:intIntegratedCable": [' \
                  '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
                print(service)


                urlSetIntIntegratedCable = "http://localhost:5054/setService/intIntegratedCable/" + serviceInstanceName
                print(urlSetIntIntegratedCable)
                headers = {'Content-Type': 'application/vnd.yang.data+json'}
                s = Session()
                req = requests.Request('POST', urlSetIntIntegratedCable,
                               data=service,
                               headers=headers
                               )
                prepped = s.prepare_request(req)
                resp = s.send(prepped)
                respuesta={card+"-"+pto+"-"+str(z) : resp.text}
                #respuesta = {card + "-" + pto + "-" + str(z): "ok"}
                #respuesta = {card: service}
                resultado.update(respuesta)


    context = {'devicesCMTS': resultado}
    #context = {'devicesCMTS': "OK"}
    return render(request, "gateway/devicesCMTS.html", context)




def createWideBandsFor8DS(device, card,pto,seqWideBand,data_Substring):
    resultado = {}

    cardName = '"card": ' + '"' + card + '"'
    portName = '"dsPort": ' + '"' + pto + '"'

    serviceInstanceName = device + "_" + card + "-0-" + pto + ":"+str(seqWideBand) +"_intWideband"
    wideBandName= '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    #******* 1ER X4
    seqWideBand=seqWideBand+1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 2do X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    return resultado


def createWideBandsFor16DS(device, card,pto,seqWideBand,data_Substring):
    resultado = {}

    cardName = '"card": ' + '"' + card + '"'
    portName = '"dsPort": ' + '"' + pto + '"'

    serviceInstanceName = device + "_" + card + "-0-" + pto + ":"+str(seqWideBand) +"_intWideband"
    wideBandName= '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7",'
    dsStr = dsStr + '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    #******* 1ER X 8
    seqWideBand=seqWideBand+1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 2do x8
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 3ER X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 4do X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 5to X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 6to X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)


    return resultado


def createWideBandsFor24DS(device, card,pto,seqWideBand,data_Substring):
    resultado = {}

    cardName = '"card": ' + '"' + card + '"'
    portName = '"dsPort": ' + '"' + pto + '"'

    serviceInstanceName = device + "_" + card + "-0-" + pto + ":"+str(seqWideBand) +"_intWideband"
    wideBandName= '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7",'
    dsStr = dsStr + '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15",'
    dsStr = dsStr + '"ds16": "16",'
    dsStr = dsStr + '"ds17": "17",'
    dsStr = dsStr + '"ds18": "18",'
    dsStr = dsStr + '"ds19": "19",'
    dsStr = dsStr + '"ds20": "20",'
    dsStr = dsStr + '"ds21": "21",'
    dsStr = dsStr + '"ds22": "22",'
    dsStr = dsStr + '"ds23": "23"'


    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    #******* 1ER X 8
    seqWideBand=seqWideBand+1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 2do x8
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 3er x8
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds16": "16",'
    dsStr = dsStr + '"ds17": "17",'
    dsStr = dsStr + '"ds18": "18",'
    dsStr = dsStr + '"ds19": "19",'
    dsStr = dsStr + '"ds20": "20",'
    dsStr = dsStr + '"ds21": "21",'
    dsStr = dsStr + '"ds22": "22",'
    dsStr = dsStr + '"ds23": "23"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 4to X16
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7",'
    dsStr = dsStr + '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)


    # ******* 5to X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 6to X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 7to X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds16": "16",'
    dsStr = dsStr + '"ds17": "17",'
    dsStr = dsStr + '"ds18": "18",'
    dsStr = dsStr + '"ds19": "19"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 8 X4
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds20": "20",'
    dsStr = dsStr + '"ds21": "21",'
    dsStr = dsStr + '"ds22": "22",'
    dsStr = dsStr + '"ds23": "23"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)



    return resultado

def createWideBandsFor32DS(device, card,pto,seqWideBand,data_Substring):
    resultado = {}

    cardName = '"card": ' + '"' + card + '"'
    portName = '"dsPort": ' + '"' + pto + '"'

    serviceInstanceName = device + "_" + card + "-0-" + pto + ":"+str(seqWideBand) +"_intWideband"
    wideBandName= '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7",'
    dsStr = dsStr + '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15",'
    dsStr = dsStr + '"ds16": "16",'
    dsStr = dsStr + '"ds17": "17",'
    dsStr = dsStr + '"ds18": "18",'
    dsStr = dsStr + '"ds19": "19",'
    dsStr = dsStr + '"ds20": "20",'
    dsStr = dsStr + '"ds21": "21",'
    dsStr = dsStr + '"ds22": "22",'
    dsStr = dsStr + '"ds23": "23",'
    dsStr = dsStr + '"ds24": "24",'
    dsStr = dsStr + '"ds25": "25",'
    dsStr = dsStr + '"ds26": "26",'
    dsStr = dsStr + '"ds27": "27",'
    dsStr = dsStr + '"ds28": "28",'
    dsStr = dsStr + '"ds29": "29",'
    dsStr = dsStr + '"ds30": "30",'
    dsStr = dsStr + '"ds31": "31"'


    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    #******* 1ER X 24
    seqWideBand=seqWideBand+1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7",'
    dsStr = dsStr + '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15",'
    dsStr = dsStr + '"ds16": "16",'
    dsStr = dsStr + '"ds17": "17",'
    dsStr = dsStr + '"ds18": "18",'
    dsStr = dsStr + '"ds19": "19",'
    dsStr = dsStr + '"ds20": "20",'
    dsStr = dsStr + '"ds21": "21",'
    dsStr = dsStr + '"ds22": "22",'
    dsStr = dsStr + '"ds23": "23"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 2do x16
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7",'
    dsStr = dsStr + '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-"+str(seqWideBand) : resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 3er x16
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds16": "16",'
    dsStr = dsStr + '"ds17": "17",'
    dsStr = dsStr + '"ds18": "18",'
    dsStr = dsStr + '"ds19": "19",'
    dsStr = dsStr + '"ds20": "20",'
    dsStr = dsStr + '"ds21": "21",'
    dsStr = dsStr + '"ds22": "22",'
    dsStr = dsStr + '"ds23": "23",'
    dsStr = dsStr + '"ds24": "24",'
    dsStr = dsStr + '"ds25": "25",'
    dsStr = dsStr + '"ds26": "26",'
    dsStr = dsStr + '"ds27": "27",'
    dsStr = dsStr + '"ds28": "28",'
    dsStr = dsStr + '"ds29": "29",'
    dsStr = dsStr + '"ds30": "30",'
    dsStr = dsStr + '"ds31": "31"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 4to x 8
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds0": "0",'
    dsStr = dsStr + '"ds1": "1",'
    dsStr = dsStr + '"ds2": "2",'
    dsStr = dsStr + '"ds3": "3",'
    dsStr = dsStr + '"ds4": "4",'
    dsStr = dsStr + '"ds5": "5",'
    dsStr = dsStr + '"ds6": "6",'
    dsStr = dsStr + '"ds7": "7"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)


    # ******* 5to X 8
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11",'
    dsStr = dsStr + '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 6to X 8 16-13
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds16": "16",'
    dsStr = dsStr + '"ds17": "17",'
    dsStr = dsStr + '"ds18": "18",'
    dsStr = dsStr + '"ds19": "19",'
    dsStr = dsStr + '"ds20": "20",'
    dsStr = dsStr + '"ds21": "21",'
    dsStr = dsStr + '"ds22": "22",'
    dsStr = dsStr + '"ds23": "23"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 7to X 8 23-31
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds23": "23",'
    dsStr = dsStr + '"ds24": "24",'
    dsStr = dsStr + '"ds25": "25",'
    dsStr = dsStr + '"ds26": "26",'
    dsStr = dsStr + '"ds27": "27",'
    dsStr = dsStr + '"ds28": "28",'
    dsStr = dsStr + '"ds29": "29",'
    dsStr = dsStr + '"ds30": "30",'
    dsStr = dsStr + '"ds31": "31"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 8vo X 4 8-11
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds8": "8",'
    dsStr = dsStr + '"ds9": "9",'
    dsStr = dsStr + '"ds10": "10",'
    dsStr = dsStr + '"ds11": "11"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 9o X 4 12-15
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds12": "12",'
    dsStr = dsStr + '"ds13": "13",'
    dsStr = dsStr + '"ds14": "14",'
    dsStr = dsStr + '"ds15": "15"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 10o X 4 16-19
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds16": "16",'
    dsStr = dsStr + '"ds17": "17",'
    dsStr = dsStr + '"ds18": "18",'
    dsStr = dsStr + '"ds19": "19"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    # ******* 10o X 4 20-23
    seqWideBand = seqWideBand + 1
    serviceInstanceName = device + "_" + card + "-0-" + pto + ":" + str(seqWideBand) + "_intWideband"
    wideBandName = '"wideBandNum": ' + '"' + str(seqWideBand) + '"'
    dsStr = '"ds20": "20",'
    dsStr = dsStr + '"ds21": "21",'
    dsStr = dsStr + '"ds22": "22",'
    dsStr = dsStr + '"ds23": "23"'

    serviceData = cardName + "," + wideBandName + "," + dsStr + "," + portName + "," + data_Substring
    service = '{"intWideband:intWideband": [' \
              '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
    print(service)

    urlSetIntWideband = "http://localhost:5054/setService/intWideband/" + serviceInstanceName
    print(urlSetIntWideband)
    headers = {'Content-Type': 'application/vnd.yang.data+json'}
    s = Session()
    req = requests.Request('POST', urlSetIntWideband,
                           data=service,
                           headers=headers
                           )
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    respuesta = {card + "-" + pto + "-" + str(seqWideBand): resp.text}
    #respuesta = {card + "-" + pto + "-" + str(seqWideBand): "ok"}
    resultado.update(respuesta)

    return resultado


@csrf_exempt
def setIntWideBand(request,numSG, numArq,numDS):

    linecards=["1","2","3","6","7","8","9"]
    ptosDS = ["0", "1", "2", "3", "4", "5", "6", "7"]

    data=request.body
    data_string=data.decode('utf-8')
    data_Substring=data_string[1:len(data_string)]

    body_data = json.loads(data_string)
    #data_string=json.dumps(body_data, sort_keys=False)

    device=body_data['device']
    numSG=int(numSG)

    if(numArq=="1"):
        numLineCards=math.ceil(numSG/8)

    if(numArq=="2"):
        numLineCards = math.ceil(numSG*2/16)

    if (numArq == "4"):
        numLineCards = math.ceil(numSG *4/16)

    numDSperSG=int(numDS)

    resultado={}
    respuesta = {}

    for x in range(0, numLineCards):
        print(x)
        card=linecards[x]
        seqWideBand=0
        for y in range(0,len(ptosDS)):
            print(y)
            pto=ptosDS[y]
            if(numDS=="8"):
                resPot=createWideBandsFor8DS(device,card,pto,seqWideBand,data_Substring)
                seqWideBand=seqWideBand+3
                respuesta={card+"-"+pto+"=": resPot}
                resultado.update(respuesta)
            if(numDS=="16"):
                resPot = createWideBandsFor16DS(device, card, pto, seqWideBand, data_Substring)
                seqWideBand = seqWideBand + 7
                respuesta = {card + "-" + pto + "=": resPot}
                resultado.update(respuesta)
            if (numDS == "24"):
                resPot = createWideBandsFor24DS(device, card, pto, seqWideBand, data_Substring)
                seqWideBand = seqWideBand + 9
                respuesta = {card + "-" + pto + "=": resPot}
                resultado.update(respuesta)
            if (numDS == "32"):
                resPot = createWideBandsFor32DS(device, card, pto, seqWideBand, data_Substring)
                seqWideBand = seqWideBand + 12
                respuesta = {card + "-" + pto + "=": resPot}
                resultado.update(respuesta)

    context = {'devicesCMTS': resultado}
    #context = {'devicesCMTS': "OK"}
    return render(request, "gateway/devicesCMTS.html", context)

@csrf_exempt
def setCableFiberNode(request,numSG,numArq):

    linecards=["1","2","3","6","7","8","9"]


    ptosDS = ["0","1","2","3","4","5","6","7"]
    ptosDS4 = ["0", "1", "2", "3"]
    ptosUS1 = ["0", "2", "4", "6", "8", "10", "12", "14"]
    ptosUS2 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
    ptosUS4 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]


    data=request.body
    data_string=data.decode('utf-8')
    data_Substring=data_string[1:len(data_string)]

    body_data = json.loads(data_string)
    #data_string=json.dumps(body_data, sort_keys=False)

    device=body_data['device']
    numSG=int(numSG)

    if(numArq=="1"):
        numLineCards=math.ceil(numSG/8)
        ptosUS=ptosUS1

    if(numArq=="2"):
        numLineCards = math.ceil(numSG*2/16)
        ptosUS = ptosUS2

    if (numArq == "4"):
        numLineCards = math.ceil(numSG *4/16)
        ptosUS = ptosUS4
        ptosDS = ptosDS4

    resultado={}
    seqFN=1
    seqUSport=0;

    for x in range(0, numLineCards):
        print(x)
        seqUSport = 0;
        card=linecards[x]
        for y in range(0,len(ptosDS)):
            print(y)
            pto=ptosDS[y]
            usPto=ptosUS[seqUSport]
            serviceInstanceName = device + "_" + card + "-0-"+pto+"_FN_"+str(seqFN)+"_cableFiberNode"
            fiberNodeName = '"fiberNodeNumber": ' + '"' + str(seqFN) + '"'
            dsIntCableName = card + "/0/" + pto
            dsIntCableName = '"'+ dsIntCableName + '"'
            dsIntCableName = '"dsIntegratedCable": ' + dsIntCableName

            usCableName0 = card + "/0/" + usPto
            usCableName0 = '"'+ usCableName0 + '"'
            usCableName0 = '"usCable0": ' + usCableName0

            if (numArq == "1"):
                usCableName = usCableName0


            usCableName1=""
            if (numArq == "2"):
                seqUSport=seqUSport+1
                usPto = ptosUS[seqUSport]
                usCableName1 = card + "/0/" + usPto
                usCableName1 = '"' + usCableName1 + '"'
                usCableName1 = '"usCable1": ' + usCableName1
                usCableName = usCableName0 + ", " +usCableName1

            usCableName2 = ""
            usCableName3 = ""
            if (numArq == "4"):
                seqUSport = seqUSport + 1
                usPto = ptosUS[seqUSport]
                usCableName1 = card + "/0/" + usPto
                usCableName1 = '"' + usCableName1 + '"'
                usCableName1 = '"usCable1": ' + usCableName1
                seqUSport = seqUSport + 1
                usPto = ptosUS[seqUSport]
                usCableName2 = card + "/0/" + usPto
                usCableName2 = '"' + usCableName2 + '"'
                usCableName2 = '"usCable2": ' + usCableName2
                seqUSport = seqUSport + 1
                usPto = ptosUS[seqUSport]
                usCableName3 = card + "/0/" + usPto
                usCableName3 = '"' + usCableName3 + '"'
                usCableName3 = '"usCable3": ' + usCableName3
                usCableName = usCableName0 + ", " + usCableName1 + ", " + usCableName2 + ", " + usCableName3



            serviceData = dsIntCableName + "," + usCableName + ","+ fiberNodeName + "," + data_Substring
            service = '{"cableFiberNode:cableFiberNode": [' \
                  '{"servicename": "' + serviceInstanceName + '",' + serviceData + "]}"
            print(service)

            urlSetCableFiberNode = "http://localhost:5054/setService/cableFiberNode/" + serviceInstanceName
            print(urlSetCableFiberNode)
            headers = {'Content-Type': 'application/vnd.yang.data+json'}
            s = Session()
            req = requests.Request('POST', urlSetCableFiberNode,
                               data=service,
                               headers=headers
                               )
            prepped = s.prepare_request(req)
            resp = s.send(prepped)
            respuesta={card+"-"+pto:resp.text}
            #respuesta = {card: "ok"}
            resultado.update(respuesta)
            seqUSport = seqUSport + 1
            seqFN = seqFN + 1

    context = {'devicesCMTS': resultado}
    #context = {'devicesCMTS': "OK"}
    return render(request, "gateway/devicesCMTS.html", context)