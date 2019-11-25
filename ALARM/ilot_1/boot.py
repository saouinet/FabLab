import machine
import neopixel
import utime
import network
from umqtt.robust import MQTTClient

f = open(config.yaml)
config = f.read()

def getConfig(key):
	choix = config.split("\n")
	for kv in choix:
		cle_valeur = kv.split(":")
		if key == cle_valeur[0]:
			return strip(cle_valeur[1]

lsize = getConfig("leds")
ilot = getConfig("ilot")
charriot = getConfig("charriot")

Leds=neopixel.NeoPixel(machine.Pin(4),lsize,bpp=4)

sta_if = network.WLAN(network.STA_IF)
client = MQTTClient(b'esp32_01'+ilot+chariot,b'10.3.141.1')

rouge = 100
vert = 100
bleu = 100

 

topic_rouge = ilot+b"/"+charriot+b"/"+b"config"+b"/"+b"rouge"
topic_vert = ilot+b"/"+charriot+b"/"+b"config"+b"/"+b"vert"
topic_bleu = ilot+b"/"+charriot+b"/"+b"config"+b"/"+b"bleu"
topic_off =  ilot+b"/"+charriot+b"/off"

def sub_cb(topic,payload):
    global Leds
    global lsize
    global rouge, topic_rouge
    global vert, topic_vert
    global bleu, topic_bleu
    global topic_off

    off = (0,0,0,0)

    if topic==topic_rouge:
	rouge=int(payload)	
    if topic==topic_vert:
	vert=int(payload)
    if topic==topic_bleu:
	bleu=int(payload)
    if topic==topic_off:
        for i in range(lsize):
            Leds[i]=off
    else:
        Leds[int(payload)-1]=(rouge,vert,bleu,0)
    utime.sleep_ms(100)
    Leds.write()

def init_mqtt():
    global client
    print("connect mqtt...")

    res = client.connect()
    if not res :
        client.set_callback(sub_cb)
        client.subscribe(topic_off)
        client.subscribe(topic_rouge)
        client.subscribe(topic_vert)
        client.subscribe(topic_bleu)

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
client.publish(ilot+b"/"+charriot,"ok")
