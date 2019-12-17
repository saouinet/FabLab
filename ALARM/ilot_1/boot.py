import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient


def getConfig():
    f = open("idents.txt")
    config = f.read()
    f.close()
    choix = config.split("\n")
    idents = []
    for kv in choix:
        idents.append(kv.strip())
    return idents

Idents = getConfig()
print("Idents :",Idents)
nbleds = len(Idents)

ilot = b"/Element"
chariot = b"/A"


Leds=neopixel.NeoPixel(machine.Pin(4),nbleds,bpp=4)
ActiveLeds = set([i for i in range(len(Idents))])
sta_if = network.WLAN(network.STA_IF)
client = MQTTClient(b'esp32_01'+ilot+chariot,b'10.3.141.1')
 

TOPIC_OFF =  b"/off"
TOPIC_BLINK = b"/blink"

def blink_active_leds():
    on = (0,0,0,100)
    off = (0,0,0,0)
    for i in ActiveLeds:
        Leds[i]=on
        utime.sleep_ms(1000)
        Leds.write()
    for i in ActiveLeds:
        Leds[i]=off
        utime.sleep_ms(1000)
        Leds.write()

def sub_cb(topic,payload):
    global Leds
    global nbleds
    on = (0,0,0,100)
    off = (0,0,0,0)
    print(topic)
    if topic==TOPIC_BLINK:
        blink_active_leds()
    if topic==TOPIC_OFF:
        for i in range(nbleds):
            Leds[i]=off
        ActiveLeds=clear()
    else:
        for pos in range(nbleds):
            if topic == Idents[pos]:
                ActiveLeds.add(pos)
                Leds[pos]=on
    utime.sleep_ms(100)
    Leds.write()

def init_mqtt():
    global client
    global Idents
    print("connect mqtt...")

    res = client.connect()
    if not res :
        client.subscribe(TOPIC_OFF)
        client.subscribe(TOPIC_BLINK)
        for id in Idents:
            client.subscribe(id)
        client.set_callback(sub_cb)


def connection():
    global sta_if
    global Leds
    sta_if.active(True)
    while 1:
        print("scan Wlan...")
        _reseaux = sta_if.scan()
        print("found: %s" %_reseaux)
        utime.sleep(1)
        trouve = False
        for n in _reseaux:
            if b"raspi-poste1" in n[0]:
                print("trouvé")
                trouve = True
                break 
            else:
                print("Pas de RPi !!")

        if trouve:
            print("connection to raspi-poste1")
            sta_if.connect("raspi-poste1","Burkert67")
            led = 0
            while not sta_if.isconnected():
                utime.sleep_ms(500)
                Leds[led]=(0,0,0,100)
                Leds.write()
                if led >= nbleds:
                    led = 0
                print(".")
                utime.sleep_ms(500)
                Leds[led]=(0,0,0,0)
                Leds.write()
                led = led+1
                
            print("Ready: ", sta_if.ifconfig())
            break
    
blink_active_leds()
connection()
init_mqtt()
client.publish(ilot+chariot,"ok")
