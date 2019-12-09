import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient


def getConfig():
    f = open(config.yaml)
    config = f.read()
    f.close()
	choix = config.split("\n")
    idents = []
	for kv in choix[1:]:
        idents.append(strip(kv))
    return idents

Idents = getConfig()
nbleds = len(Idents)
ilot = b"/Element"
chariot = b"/A"


Leds=neopixel.NeoPixel(machine.Pin(4),nbleds,bpp=4)

sta_if = network.WLAN(network.STA_IF)
client = MQTTClient(b'esp32_01'+ilot+chariot,b'10.3.141.1')
 

topic_off =  

def sub_cb(topic,payload):
    global Leds
    global nbleds
    on = (0,0,0,100)
    off = (0,0,0,0)
    if topic==b"/off":
        for i in range(nbleds):
            Leds[i]=off
    else:
        for pos in range(nbleds):
            if topic == Idents[pos]:
                Leds[pos]=on
    utime.sleep_ms(100)
    Leds.write()

def blinkLeds():
    on = (0,0,0,100)
    off = (0,0,0,0)
    for i in range(nbleds):
        Leds[i]=on
        utime.sleep_ms(1000)
        Leds.write()
    for i in range(nbleds):
        Leds[i]=off
        utime.sleep_ms(1000)
        Leds.write()
    
def init_mqtt():
    global client
    print("connect mqtt...")

    res = client.connect()
    if not res :
        client.set_callback(sub_cb)
        for id in Idents
            client.subscribe(id)

def connection():
    global sta_if
    sta_if.active(True)
    while 1:
        _reseaux = sta_if.scan()
        print("scan Wlan...%s" %_reseaux)
        utime.sleep(1)
        trouve = False
        for n in _reseaux:
            if b"raspi-poste1" in n[0]:
                print("trouvé")
                trouve = True
                break 
        if trouve:
            print("connection to raspi-poste1")
            sta_if.connect("raspi-poste1","Burkert67")
            led = 0
            while not sta_if.isconnected():
                Leds[led]=(0,0,0,100)
                Leds.write()
                if led >= nbleds:
                    led = 0
                print(".")
                utime.sleep(1)
                Leds[led]=(0,0,0,0)
                Leds.write()
                led = led+1
                
            print("Ready: ", sta_if.ifconfig())
            break
    
blinkLeds()
connection()
init_mqtt()
client.publish(ilot+chariot,"ok")
