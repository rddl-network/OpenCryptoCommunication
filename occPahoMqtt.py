# python3.10

import time
import random
import signal
import lanbox
import json

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

BOXHOST = '172.16.20.9'
BOXPORT = 777
BOXPASSWORD = '777'

HOSTNAME = "172.16.21.153 nestor
"
PORT = 1883

USERNAME = 'nestor'
PASSWORD = 'nestor'

light = {
	"0xE7D3" : 0,     # magnolia
	"0x995E" : 0,    # mirto
	'cocina' : 0, 
	"0x709A" : 0,    # salongrande
	'saloncito' : 0,
	"0x7FBB" : 0,     # piano
	'entrada' : 0,
	"0x92FE" : 0,     # adrian
	"0xE334" : 0,     # adriancama
	"0xE438" : 0,     # priam
	"0x3ED5" : 0,     # sofia
    "0x3400" : 0,     # laura
	'0x5BD0' : 0,     # anaplantabaja
	'0x46B3' : 0,          # anaplantaalta
	'anaaltaentrada' : 0,
	'0x1E69' : 0,         # anaplantabano
	"0x6690" : 0,     # lauracabezero
	'lauranochewc' : 0,
    "0xFE19" : 0,     # magnoliacabazero
	'magnoliacabezero' : 0,
	'magnoliabano' : 0,
	"0x1D8F" : 0,    # mirtocabezero
	'mirtowc' : 0,
	"0x882A" : 0,     # pianobano
	"0x86D8" : 0,     # priamcabazero
	'priambano' : 0,
	'sofiaaltacabezero' : 0,
}

box = lanbox.Lanbox(BOXHOST, BOXPORT, BOXPASSWORD)



def switch_light(light_name):

    if light_name ==  '0x3ED5':          # sofia
        print(F"Switch signal for room Sofia")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({161:150})
            box.channelSetData({172:250})
            box.channelSetData({168:150})
            box.channelSetData({166:200})
            box.channelSetData({170:150})
            box.channelSetData({167:150})
            box.channelSetData({169:150})
            box.channelSetData({190:150})
            light[light_name] = 1
        else:
            box.channelSetData({161:0})
            box.channelSetData({172:0})
            box.channelSetData({168:0})
            box.channelSetData({166:0})
            box.channelSetData({170:0})
            box.channelSetData({167:0})
            box.channelSetData({169:0})
            box.channelSetData({190:0})
            light[light_name] = 0

    if light_name ==  '0x1E69':          # anaplantabano
        print(F"Switch signal for room Ana Planta Bano")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({224:150})
            box.channelSetData({225:250})
            light[light_name] = 1
        else:
            box.channelSetData({224:0})
            box.channelSetData({225:0})
            light[light_name] = 0

    if light_name ==  '0x46B3':          # anaplantaalta
        print(F"Switch signal for room Ana Planta Alta")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({201:250, 202:0, 203:250, 204:0})
            box.channelSetData({215:250})
            box.channelSetData({227:150})
            box.channelSetData({226:150})
            box.channelSetData({223:150})
            light[light_name] = 1
        else:
            box.channelSetData({201:0, 202:0, 203:0, 204:0})
            box.channelSetData({215:0})
            box.channelSetData({227:0})
            box.channelSetData({226:0})
            box.channelSetData({223:0})
            light[light_name] = 0

    if light_name ==  '0x5BD0':          # anaplantabaja
        print(F"Switch signal for room Ana Planta Baja")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({197:250, 198:0, 199:250, 200:0})
            box.channelSetData({228:150})
            box.channelSetData({230:150})
            box.channelSetData({210:150})
            box.channelSetData({239:150})
            box.channelSetData({216:250})
            box.channelSetData({231:150})
            box.channelSetData({222:200})
            light[light_name] = 1
        else:
            box.channelSetData({197:0, 198:0, 199:0, 200:0})
            box.channelSetData({228:0})
            box.channelSetData({230:0})
            box.channelSetData({210:0})
            box.channelSetData({239:0})
            box.channelSetData({216:0})
            box.channelSetData({231:0})
            box.channelSetData({222:0})
            light[light_name] = 0
    
    if light_name ==  '0x92FE':          # adrian
        print(F"Switch signal for room Adrian")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({235:150})
            box.channelSetData({236:150})
            box.channelSetData({214:250})
            box.channelSetData({209:150})
            light[light_name] = 1
            light['0xE334'] = 1
        else:
            box.channelSetData({235:0})
            box.channelSetData({236:0})
            box.channelSetData({214:0})
            box.channelSetData({209:0})
            light[light_name] = 0
            light['0xE334'] = 0

    if light_name ==  '0xE334':          # adriancama
        print(F"Switch signal for room Adrian Cama")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({235:150})
            box.channelSetData({236:150})
            box.channelSetData({214:250})
            box.channelSetData({209:150})
            light[light_name] = 1
            light['0x92FE'] = 1
        else:
            box.channelSetData({235:0})
            box.channelSetData({236:0})
            box.channelSetData({214:0})
            box.channelSetData({209:0})
            light[light_name] = 0
            light['0x92FE'] = 0

    if light_name ==  '0xE7D3':          # magnolia
        print(F"Switch signal for room Magnolia")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({14:190})
            box.channelSetData({15:190})
            box.channelSetData({17:190})
            box.channelSetData({18:190})
            box.channelSetData({19:190})
            box.channelSetData({20:190})
            box.channelSetData({21:190})
            box.channelSetData({28:190})
            box.channelSetData({1:20, 2:75, 3:210, 4:160})
            light[light_name] = 1
            light['0xFE19'] = 1
        else:
            box.channelSetData({14:0})
            box.channelSetData({15:0})
            box.channelSetData({17:0})
            box.channelSetData({18:0})
            box.channelSetData({19:0})
            box.channelSetData({20:0})
            box.channelSetData({21:0})
            box.channelSetData({28:0})
            box.channelSetData({1:0, 2:0, 3:0, 4:0})
            light[light_name] = 0
            light['0xFE19'] = 0

    if light_name ==  '0xFE19':          # magnoliacabazero
        print(F"Switch signal for room Magnolia Cabazero")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({14:190})
            box.channelSetData({15:190})
            box.channelSetData({17:190})
            box.channelSetData({18:190})
            box.channelSetData({19:190})
            box.channelSetData({20:190})
            box.channelSetData({21:190})
            box.channelSetData({28:190})
            box.channelSetData({1:20, 2:75, 3:210, 4:160})
            light[light_name] = 1
            light['0xE7D3'] = 1
        else:
            box.channelSetData({14:0})
            box.channelSetData({15:0})
            box.channelSetData({17:0})
            box.channelSetData({18:0})
            box.channelSetData({19:0})
            box.channelSetData({20:0})
            box.channelSetData({21:0})
            box.channelSetData({28:0})
            box.channelSetData({1:0, 2:0, 3:0, 4:0})
            light[light_name] = 0
            light['0xE7D3'] = 0

    if light_name ==  '0x1D8F':          # mirtocabazero
        print(F"Switch signal for room Mirto Cabazero")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({24:150})
            box.channelSetData({25:150})
            box.channelSetData({26:150})
            box.channelSetData({27:150})
            box.channelSetData({23:150})
            box.channelSetData({16:150})
            box.channelSetData({37:0, 38:0, 39:0, 40:0})
            light[light_name] = 1
            light['0x995E'] = 1
        else:
            box.channelSetData({24:0})
            box.channelSetData({25:0})
            box.channelSetData({26:0})
            box.channelSetData({27:0})
            box.channelSetData({23:0})
            box.channelSetData({16:0})
            light[light_name] = 0
            light['0x995E'] = 0

    if light_name ==  '0x995E':          # mirto
        print(F"Switch signal for room Mirto")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({24:150})
            box.channelSetData({25:150})
            box.channelSetData({26:150})
            box.channelSetData({27:150})
            box.channelSetData({23:150})
            box.channelSetData({16:150})
            box.channelSetData({37:0, 38:0, 39:0, 40:0})
            light[light_name] = 1
            light['0x1D8F'] = 1
        else:
            box.channelSetData({24:0})
            box.channelSetData({25:0})
            box.channelSetData({26:0})
            box.channelSetData({27:0})
            box.channelSetData({23:0})
            box.channelSetData({16:0})
            light[light_name] = 0
            light['0x1D8F'] = 0

    if light_name ==  '0x882A':          # pianobano
        print(F"Switch signal for room Piano Bano")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({144:150})
            box.channelSetData({132:150})
            box.channelSetData({135:100})
            box.channelSetData({113:250, 114:0, 115:250, 116:0})
            light[light_name] = 1
        else:
            box.channelSetData({144:0})
            box.channelSetData({132:0})
            box.channelSetData({135:0})
            box.channelSetData({113:0, 114:0, 115:0, 116:0})
            light[light_name] = 0

    if light_name ==  '0x7FBB':          # piano
        print(F"Switch signal for room Piano")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({144:150})
            box.channelSetData({132:150})
            box.channelSetData({135:100})
            box.channelSetData({113:250, 114:0, 115:250, 116:0})
            light[light_name] = 1
        else:
            box.channelSetData({144:0})
            box.channelSetData({132:0})
            box.channelSetData({135:0})
            box.channelSetData({113:0, 114:0, 115:0, 116:0})
            light[light_name] = 0

    if light_name ==  '0x86D8':          # priamcabazero
        print(F"Switch signal for room Priam Cabazero")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({178:150})
            box.channelSetData({192:150})
            box.channelSetData({183:150})
            box.channelSetData({179:150})
            box.channelSetData({176:250})
            box.channelSetData({182:250})
            box.channelSetData({181:150})
            box.channelSetData({184:150})
            box.channelSetData({177:150})
            box.channelSetData({149:250, 150:0, 151:250, 152:0})
            box.channelSetData({182:150})
            light[light_name] = 1
        else:
            box.channelSetData({178:0})
            box.channelSetData({192:0})
            box.channelSetData({183:0})
            box.channelSetData({179:0})
            box.channelSetData({176:0})
            box.channelSetData({182:0})
            box.channelSetData({181:0})
            box.channelSetData({184:0})
            box.channelSetData({177:0})
            box.channelSetData({149:0, 150:0, 151:0, 152:0})
            box.channelSetData({182:0})
            light[light_name] = 0

    if light_name ==  '0xE438':          # priam
        print(F"Switch signal for room Priam")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({178:150})
            box.channelSetData({192:150})
            box.channelSetData({183:150})
            box.channelSetData({179:150})
            box.channelSetData({176:250})
            box.channelSetData({182:250})
            box.channelSetData({181:150})
            box.channelSetData({184:150})
            box.channelSetData({177:150})
            box.channelSetData({149:250, 150:0, 151:250, 152:0})
            box.channelSetData({182:150})
            light[light_name] = 1
        else:
            box.channelSetData({178:0})
            box.channelSetData({192:0})
            box.channelSetData({179:0})
            box.channelSetData({176:0})
            box.channelSetData({182:0})
            box.channelSetData({181:0})
            box.channelSetData({184:0})
            box.channelSetData({177:0})
            box.channelSetData({149:0, 150:0, 151:0, 152:0})
            box.channelSetData({182:0})
            light[light_name] = 0

    #if light_name ==  '0x3ED5':          # laura
        #print(F"Switch signal for room Laura")
        #print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        #if light[light_name] == 0:
            #box.channelSetData({161:150})
            #box.channelSetData({172:250})
            #box.channelSetData({168:150})
            #box.channelSetData({166:200})
            #box.channelSetData({170:150})
            #box.channelSetData({167:150})
            #box.channelSetData({169:150})
            #box.channelSetData({190:150})
            #light[light_name] = 1
        #else:
            #box.channelSetData({161:0})
            #box.channelSetData({172:0})
            #box.channelSetData({168:0})
            #box.channelSetData({166:0})
            #box.channelSetData({170:0})
            #box.channelSetData({167:0})
            #box.channelSetData({169:0})
            #box.channelSetData({190:0})
            #light[light_name] = 0

    if light_name ==  '0x3400':          # lauraalta
        print(F"Switch signal for room Laura Alta")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({188:150})
            box.channelSetData({159:150})
            box.channelSetData({163:200})
            box.channelSetData({158:200})
            box.channelSetData({164:150})
            box.channelSetData({189:150})
            box.channelSetData({165:200})
            box.channelSetData({160:150})
            box.channelSetData({162:200})
            box.channelSetData({161:150})
            box.channelSetData({180:250})
            box.channelSetData({187:200})
            box.channelSetData({145:250, 146:0, 147:250, 148:0})
            light[light_name] = 1
        else:
            box.channelSetData({188:0})
            box.channelSetData({159:0})
            box.channelSetData({163:0})
            box.channelSetData({158:0})
            box.channelSetData({164:0})
            box.channelSetData({189:0})
            box.channelSetData({165:0})
            box.channelSetData({160:0})
            box.channelSetData({162:0})
            box.channelSetData({161:0})
            box.channelSetData({180:0})
            box.channelSetData({187:0})
            box.channelSetData({145:0, 146:0, 147:0, 148:0})
            light[light_name] = 0

    if light_name ==  '0x6690':          # lauracabezero
        print(F"Switch signal for room Laura Cabazero")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({188:150})
            box.channelSetData({159:150})
            box.channelSetData({163:200})
            box.channelSetData({158:200})
            box.channelSetData({164:150})
            box.channelSetData({189:150})
            box.channelSetData({165:200})
            box.channelSetData({160:150})
            box.channelSetData({162:200})
            box.channelSetData({161:150})
            box.channelSetData({180:250})
            box.channelSetData({187:200})
            box.channelSetData({145:250, 146:0, 147:250, 148:0})
            light[light_name] = 1
        else:
            box.channelSetData({188:0})
            box.channelSetData({159:0})
            box.channelSetData({163:0})
            box.channelSetData({158:0})
            box.channelSetData({164:0})
            box.channelSetData({189:0})
            box.channelSetData({165:0})
            box.channelSetData({160:0})
            box.channelSetData({162:0})
            box.channelSetData({161:0})
            box.channelSetData({180:0})
            box.channelSetData({187:0})
            box.channelSetData({145:0, 146:0, 147:0, 148:0})
            light[light_name] = 0

    if light_name == "0x709A":  # salongrande
        print(F"Switch signal for room Salon Grande")
        print(F"Hour: {time.localtime()[3]}, Minute: {time.localtime()[4]}, Second: {time.localtime()[5]}")
        if light[light_name] == 0:
            box.channelSetData({93:250, 94:0, 95:250, 96:0})
            box.channelSetData({117:250, 118:0, 119:250, 120:0})
            box.channelSetData({97:250, 98:0, 99:250, 100:0})
            box.channelSetData({105:250, 106:0, 107:250, 108:0})
            box.channelSetData({85:250, 86:0, 87:250, 88:0})
            box.channelSetData({101:250, 102:0, 103:250, 104:0})
            box.channelSetData({45:250, 46:0, 47:250, 48:0})
            box.channelSetData({109:250, 110:0, 111:250, 112:0})
            box.channelSetData({41:250, 42:0, 43:250, 44:0})
            box.channelSetData({49:250, 50:0, 51:250, 52:0})
            box.channelSetData({81:250, 82:0, 83:250, 84:0})
            box.channelSetData({89:250, 90:0, 91:250, 92:0})
            box.channelSetData({73:250, 74:0, 75:250, 76:0})
            box.channelSetData({136:150})
            box.channelSetData({126:150})
            box.channelSetData({127:150})
            box.channelSetData({128:150})
            box.channelSetData({124:80})
            box.channelSetData({121:80})
            box.channelSetData({138:150})
            box.channelSetData({122:80})
            box.channelSetData({125:150})
            box.channelSetData({141:80})
            box.channelSetData({140:150})
            box.channelSetData({137:150})
            box.channelSetData({130:150})
            box.channelSetData({142:80})
            box.channelSetData({131:150})
            box.channelSetData({139:250})
            box.channelSetData({143:80})
            box.channelSetData({123:80})
            light[light_name] = 1
        else:
            box.channelSetData({93:0, 94:0, 95:0, 96:0})
            box.channelSetData({117:0, 118:0, 119:0, 120:0})
            box.channelSetData({97:0, 98:0, 99:0, 100:0})
            box.channelSetData({105:0, 106:0, 107:0, 108:0})
            box.channelSetData({85:0, 86:0, 87:0, 88:0})
            box.channelSetData({101:0, 102:0, 103:0, 104:0})
            box.channelSetData({45:0, 46:0, 47:0, 48:0})
            box.channelSetData({109:0, 110:0, 111:0, 112:0})
            box.channelSetData({41:0, 42:0, 43:0, 44:0})
            box.channelSetData({49:0, 50:0, 51:0, 52:0})
            box.channelSetData({81:0, 82:0, 83:0, 84:0})
            box.channelSetData({89:0, 90:0, 91:0, 92:0})
            box.channelSetData({73:0, 74:0, 75:0, 76:0})
            box.channelSetData({136:0})
            box.channelSetData({126:0})
            box.channelSetData({127:0})
            box.channelSetData({128:0})
            box.channelSetData({124:0})
            box.channelSetData({121:0})
            box.channelSetData({138:0})
            box.channelSetData({122:0})
            box.channelSetData({125:0})
            box.channelSetData({141:0})
            box.channelSetData({140:0})
            box.channelSetData({137:0})
            box.channelSetData({130:0})
            box.channelSetData({142:0})
            box.channelSetData({131:0})
            box.channelSetData({139:0})
            box.channelSetData({143:0})
            box.channelSetData({123:0})
            light[light_name] = 0




import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe


########################################
"""

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    payload = json.loads(message.payload)
    if payload["ZbReceived"]["0x709A"]:
        switch_light("0x709A")

"""
########################################


def broker(msg):
    payload = json.loads(msg.payload)
    print(payload["ZbReceived"])
    payload_name = list(payload.items())[0][1]
    payload_sensor = list(payload_name)[0]
    print(payload_sensor)
    if (not 'ModelId' in payload['ZbReceived'][payload_sensor] and not 'BatteryPercentage' in payload['ZbReceived'][payload_sensor] and not 'BatteryVoltage' in payload['ZbReceived'][payload_sensor]):
        if payload_sensor == "0x709A":
            switch_light("0x709A")
        if payload_sensor == "0x6690":
            switch_light("0x6690")
        if payload_sensor == "0x3400":
            switch_light("0x3400")
        if payload_sensor == "0x3ED5":
            switch_light("0x3ED5")
        if payload_sensor == "0xE438":
            switch_light("0xE438")
        if payload_sensor == "0x86D8":
            switch_light("0x86D8")
        if payload_sensor == "0x7FBB":
            switch_light("0x7FBB")
        if payload_sensor == "0x882A":
            switch_light("0x882A")
        if payload_sensor == "0x995E":
            switch_light("0x995E")
        if payload_sensor == "0x1D8F":
            switch_light("0x1D8F")
        if payload_sensor == "0xE7D3":
            switch_light("0xE7D3")
        if payload_sensor == "0xFE19":
            switch_light("0xFE19")
        if payload_sensor == "0x92FE":
            switch_light("0x92FE")
        if payload_sensor == "0xE334":
            switch_light("0xE334")
        if payload_sensor == "0x5BD0":
            switch_light("0x5BD0")
        if payload_sensor == "0x46B3":
            switch_light("0x46B3")
        if payload_sensor == "0x1E69":
            switch_light("0x1E69")

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        # client.loop_stop() #stop the loop
        exit(1)

signal.signal(signal.SIGINT, handler)

def run():
    msg = subscribe.simple(topics=['tele/tasmota_ladonaira_light/SENSOR'], hostname= HOSTNAME, port=1883, auth={'username':USERNAME,'password':PASSWORD}, msg_count=1)
    # tele/tasmota_10B408/SENSOR
    
    broker(msg)
    while True:
        run()

if __name__== '__main__':
    run()