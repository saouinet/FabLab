import machine
import neopixel
import utime
import network
from umqtt.simple import MQTTClient

Leds=neopixel.NeoPixel(machine.Pin(4),5,bpp=4)

sta_if = network.WLAN(network.STA_IF)

client = MQTTClient(b'esp32_01','10.3.141.1')


def sub_cb(topic,payload):
    global Leds
    off = (0,0,0,0)
    on = (100,100,100,0)
    size = len(Idents)
    if topic==b"off":
        for i in range(size):
            Leds[i]=off
    else:
        Leds[int(payload)-1]=on
    utime.sleep_ms(100)
    Leds.write()

def init_mqtt():
    global client
    print("connect mqtt...")

    client.connect()
    client.set_callback(sub_cb)
    client.subscribe(b"off")
    client.subscribe(b"ilot_1")

def connection():
    global sta_if
    sta_if.active(True)
    print("scan Wlan...")
    _reseaux = sta_if.scan()
    if b"raspi-poste1" in _reseaux: 
        sta_if.connect("raspi-poste1","Burkert67")
        while not sta_if.isconnected():
            print(".")
            utime.sleep(1)

connection()
init_mqtt()
client.publish(b"ilot_1","ok")