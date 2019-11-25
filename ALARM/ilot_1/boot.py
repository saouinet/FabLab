import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient


lsize = 5
Leds=neopixel.NeoPixel(machine.Pin(4),lsize,bpp=4)

sta_if = network.WLAN(network.STA_IF)

client = MQTTClient(b'esp32_01',b'10.3.141.1')


def sub_cb(topic,payload):
    global Leds
    global lsize
    off = (0,0,0,0)
    on = (100,100,100,0)
    
    if topic==b"off":
        for i in range(lsize):
            Leds[i]=off
    else:
        Leds[int(payload)-1]=on
    utime.sleep_ms(100)
    Leds.write()

def init_mqtt():
    global client
    print("connect mqtt...")

    res = client.connect()
    if not res :
        client.set_callback(sub_cb)
        client.subscribe(b"off")
        client.subscribe(b"ilot1")

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
            while not sta_if.isconnected():
                print(".")
                utime.sleep(1)
            print("Ready: ", sta_if.ifconfig())
            break

    

connection()
init_mqtt()
client.publish(b"ilot_1","ok")
