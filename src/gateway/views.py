from django.shortcuts import render
import requests
#from requests import Session
import json

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
       'devicesPE': devicesPE
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