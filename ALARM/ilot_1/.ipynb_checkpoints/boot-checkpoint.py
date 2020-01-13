import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient


def getConfig():
    f = open("config.yaml")
    config = f.read()
    f.close()
    choix = config.split("\n")
    config = {}
    for kv in choix:
        key,val = kv.split(":")
        config[key]=val
    print(config)
    return config

def getIdents():
    f = open("idents.txt")
    config = f.read()
    f.close()
    choix = config.split("\n")
    idents = []
    for kv in choix:
        idents.append(kv.strip())
    print(idents)
    return idents

Idents = getIdents()
print("Idents :",Idents)
nbleds = len(Idents)

nom_esp32 = b"esp32" 
ilot = b"/element"
chariot = b"/x"
brocker = b'10.3.141.1'


Leds=neopixel.NeoPixel(machine.Pin(4),nbleds,bpp=4)
ActiveLeds = set([i for i in range(len(Idents))])
sta_if = network.WLAN(network.STA_IF)
client = MQTTClient(nom_esp32+ilot+chariot,broker,port=1883)
on = (0,0,0,100)
off = (0,0,0,0)
 

TOPIC_OFF = ilot+"/off"
TOPIC_BLINK = ilot+"/blink"

def blink_active_leds():
    for i in ActiveLeds:
        Leds[i]=on
        utime.sleep_ms(500)
        Leds.write()
    for i in ActiveLeds:
        Leds[i]=off
        utime.sleep_ms(500)
        Leds.write()

def sub_cb(topic,payload):
    global Leds
    global nbleds
    print(topic)
    if topic == TOPIC_BLINK:
        blink_active_leds()
    if topic == TOPIC_OFF:
        for i in range(nbleds):
            Leds[i]=off
        ActiveLeds.clear()
    else:
        for pos in range(nbleds):
            if topic == ilot+"/"+Idents[pos]:
                ActiveLeds.add(pos)
                Leds[pos]=on
    utime.sleep_ms(100)
    Leds.write()

def init_mqtt(client,Idents,ilot):
    print("connect mqtt...")
    res = client.connect()

    if not res :
        client.set_callback(sub_cb)
        client.subscribe(TOPIC_OFF)
        client.subscribe(TOPIC_BLINK)
        for _id in Idents:
            _nom = ilot+"/"+str(_id)
            client.subscribe(_nom)

def infoleds(color):
    utime.sleep_ms(500)
    Leds[0] = color
    Leds.write()
    print(".")
    utime.sleep_ms(500)
    Leds[0] = off
    Leds.write()

def connection(sta_if, Leds):
    sta_if.active(True)
    while 1:
        print("scan Wlan...")
        _reseaux = sta_if.scan()
        utime.sleep_ms(2000)
        print("found: %s" % _reseaux)
        trouve = False
        for n in _reseaux:
            if b"raspi-poste1" in n[0]:
                infoleds((0,50,0,0))
                print("trouvé")
                trouve = True
                break 
            else:
                infoleds((50,0,0,0))
                print("Pas de RPi !!")

        if trouve:
            print("connection to raspi-poste1")
            while not sta_if.isconnected():
                sta_if.connect("raspi-poste1", "Burkert67")
                utime.sleep_ms(1000)
                infoleds((0,0,0,50))
                print(".")
            print("Ready: ", sta_if.ifconfig())
            break
    
blink_active_leds()
connection(sta_if,Leds)
init_mqtt(client, Idents,ilot)
client.publish(ilot+chariot,b"ok")

