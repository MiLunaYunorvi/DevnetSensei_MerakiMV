import requests
import json


#CREDENCIALES DE LA DEMO ALWAYS-ON DE MERAKI
X_Cisco_Meraki_API_Key = input("Ingrese el API Key de Meraki: ")
Camara_serial = input("Ingresa el serial de la cámara que deseas monitorear: ")
Token_bot = input("Ingresa el token del bot: ")
Webex_room = input ("Ingresa el id del room de Webex: ")


url1 = "https://api.meraki.com/api/v1/devices/{serial}/camera/generateSnapshot".format(serial=Camara_serial)
payload = '''{ "fullframe": true }'''
url2 = "https://api.meraki.com/api/v1/devices/{serial}/camera/analytics/live".format(serial=Camara_serial)

headers_meraki= {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": X_Cisco_Meraki_API_Key }

def snapshot2():
    snap = requests.request('POST', url1, headers=headers_meraki)
    snapshot_url = (snap.json())['url']
    return snapshot_url

def alarma(mensaje_webex):
    global  Webex_room, Token_bot
    url=snapshot2()
    url_webex = "https://webexapis.com/v1/messages"
    payload = json.dumps({
        "roomId": Webex_room,
        "files": ["{}".format(url)],
        "text": '{}'.format(mensaje_webex)   
    })
    headers = {
        'Authorization': 'Bearer {token}'.format(token=Token_bot),
        'Content-Type': 'application/json'
    }
    requests.request("POST", url_webex, headers=headers, data=payload)



analitica= requests.request('GET', url2, headers=headers_meraki)
analitica_res = (analitica.json())['zones']
keys=(list(analitica_res.keys()))
for i in range(len(keys)):
    mensaje = "En la zona ",keys[i], ": " , "Se tienen ",analitica_res[keys[i]]['person']," personas."
    mensaje_webex = "En la zona {}, se tienen {} personas".format(keys[i],analitica_res[keys[i]]['person'])
    alarma(mensaje_webex)
    print(mensaje)
#print('*.* Observa la imagen en la siguiente url: ',snapshot_url)
