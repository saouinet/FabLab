import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient


#get the configuration dictionary from yaml file
def getConfig():
    f = open("config.yaml")
    contenu = f.read()
    f.close()
    choix = contenu.split("\n")
    config = {}
    for kv in choix:
        if kv != '':
            key,val = kv.split(":")
            key = key.strip()
            config[key]=bytes(val.strip()[1:-1],"utf-8")
    return config

# get the list of idents stored in the configuration file
def getIdents():
    f = open("idents.txt")
    config = f.read()
    f.close()
    choix = config.split("\n")
    idents = []
    for kv in choix:
        idents.append(bytes(kv.strip(),"utf-8"))
    return idents

# make the LEDs blink 1 time
def blink_active_leds():
    for i in ActiveLeds:
        Leds[i]=LED_WHITE
        utime.sleep_ms(500)
        Leds.write()
    for i in ActiveLeds:
        Leds[i]=LED_OFF
        utime.sleep_ms(500)
        Leds.write()

# mqtt callback
def sub_cb(topic,payload,Leds,nbleds):
    print(topic)
    if topic == TOPIC_BLINK:
        blink_active_leds()
    if topic == TOPIC_OFF:
        for i in range(nbleds):
            Leds[i]=LED_OFF
        ActiveLeds.clear()
    else:
        for pos in range(nbleds):
            if topic == ilot+"/"+Idents[pos]:
                ActiveLeds.add(pos)
                Leds[pos]=LED_WHITE
    utime.sleep_ms(100)
    Leds.write()

# initialize mqtt subscriptions
def init_mqtt(client,Idents,ilot):
    print("connect mqtt...")
    res = client.connect()
    utime.sleep_ms(1000)
    client.set_callback(sub_cb)
    if not res :
        print("sub:",TOPIC_OFF)
        client.subscribe(TOPIC_OFF)
        print("sub:",TOPIC_BLINK)
        client.subscribe(TOPIC_BLINK)
        for _id in Idents:
            _nom = ilot+b"/"+_id
            print("sub:",_nom)
            client.subscribe(_nom)

# make the first LED blink red
def infoleds():
    utime.sleep_ms(500)
    Leds[0] = LED_RED
    Leds.write()
    print(".")
    utime.sleep_ms(500)
    Leds[0] = LED_OFF
    Leds.write()

# connect to Wifi
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
                print("trouvé")
                trouve = True
                break 
            else:
                print("Pas de RPi !!")

        if trouve:
            print("connection to raspi-poste1")
            while not sta_if.isconnected():
                sta_if.connect("raspi-poste1", "Burkert67")
                utime.sleep_ms(1000)
                infoleds()
                print(".")
            print("Ready: ", sta_if.ifconfig())
            break
#start ESP32 ok


def set_esp_leds(leds,color=LED_GREEN):
    print(leds,col)
    for l in leds:
        l=color
    ESP32leds.write()
# ESP32 ok
def blink_green(leds):
    set_esp_leds(leds,LED_GREEN)
    utime.sleep_ms(500)
    set_esp_leds(leds,LED_OFF)
    utime.sleep_ms(500)

# constants
configuration = getConfig()
chariot = configuration["chariot"]
ilot = configuration["ilot"]
TOPIC_OFF = ilot+"/off"
TOPIC_BLINK = ilot+"/blink"
LED_OFF =(0,0,0,0)
LED_WHITE = (0,0,0,100)
LED_RED = (100, 0, 0, 0)
LED_BLUE = (0,0,20,0)
LED_GREEN = (0, 20, 0, 0)

# define idents configuration
Idents = getIdents()
print("Idents :",Idents)

# define LEDs configuration
nbleds = len(Idents)
Leds=neopixel.NeoPixel(machine.Pin(4),nbleds,bpp=4)
ActiveLeds = set([i for i in range(len(Idents))])
ESP32leds=neopixel.NeoPixel(machine.Pin(2),2,bpp=4)
set_esp_leds(ESP32leds[:1],LED_GREEN)
set_esp_leds(ESP32leds[1:],LED_BLUE)

# define wifi configuration
sta_if = network.WLAN(network.STA_IF)

# define MQTT configuration
client = MQTTClient(b"esp32_01"+ilot+chariot,configuration["broker"],port=1883)

blink_active_leds()
connection(sta_if,Leds)
init_mqtt(client, Idents,ilot)
client.publish(ilot+chariot,b"ok")
set_esp_leds(ESP32leds,LED_GREEN)

