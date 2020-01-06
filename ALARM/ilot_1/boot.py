import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient

# constants
chariot = b"/A"
ilot = b"/Element"
TOPIC_OFF = ilot+"/off"
TOPIC_BLINK = ilot+"/blink"

# define idents configuration
Idents = getConfig()
print("Idents :",Idents)

# define LEDs configuration
nbleds = len(Idents)
Leds=neopixel.NeoPixel(machine.Pin(4),nbleds,bpp=4)
ActiveLeds = set([i for i in range(len(Idents))])

# define wifi configuration
sta_if = network.WLAN(network.STA_IF)

# define MQTT configuration
client = MQTTClient(b"esp32_01"+ilot+chariot,b'10.3.141.1',port=1883)

# get the list of idents stored in the configuration file
def getConfig():
    f = open("idents.txt")
    config = f.read()
    f.close()
    choix = config.split("\n")
    idents = []
    for kv in choix:
        idents.append(kv.strip())
    return idents

# make the LEDs blink 1 time
def blink_active_leds():
    on = (0,0,0,100)
    off = (0,0,0,0)
    for i in ActiveLeds:
        Leds[i]=on
        utime.sleep_ms(500)
        Leds.write()
    for i in ActiveLeds:
        Leds[i]=off
        utime.sleep_ms(500)
        Leds.write()

# mqtt callback
def sub_cb(topic,payload,Leds,nbleds):
    on = (0,0,0,100)
    off = (0,0,0,0)
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

# initialize mqtt subscriptions
def init_mqtt(client,Idents,ilot):
    print("connect mqtt...")
    res = client.connect()
    if not res :
        client.subscribe(ilot+TOPIC_OFF)
        client.subscribe(ilot+TOPIC_BLINK)
        for _id in Idents:
            _nom = ilot+"/"+str(_id)
            client.subscribe(_nom)
        client.set_callback(sub_cb)

# make the first LED blink
def infoleds():
    utime.sleep_ms(500)
    Leds[0] = (100, 0, 0, 0)
    Leds.write()
    print(".")
    utime.sleep_ms(500)
    Leds[0] = (0, 0, 0, 0)
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

blink_active_leds()
connection(sta_if,Leds)
init_mqtt(client, Idents,ilot)
client.publish(ilot+chariot,b"ok")

