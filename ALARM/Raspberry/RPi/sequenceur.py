#!/usr/bin/python3

from threading import Thread
import paho.mqtt.client as mqtt
import pandas as pd
import os


broker_url = "localhost"
broker_port = 1883
def on_message(client, userdata, message):
	print("Test_Reçu:{}".format(message.payload))

def receptionMessages():
	client = mqtt.Client()
	client.connect(broker_url, broker_port)
	client.on_message = on_message
	client.subscribe("scanner/#")
	client.loop_start()
	while 1:
		pass

	
def initialiser_idents():
	return pd.read_csv("idents.csv",encoding='utf-8')

def idents_pour(id_produit):
	DF_Idents = initialiser_idents()
	return list(DF_Idents["ident"][DF_Idents["ID objet"] == id_produit])
	
def Scan2Ident(scanvalue):
	"43487459001056660600010000001000"
	if len(scanvalue) == 32:
		return int(scanvalue[12:18])
	else:
		return None
		
class Machine(Thread):
	fini = False
	ident = ""
	df_idents =[]
	product_ident = None

	def on_message(self,client, userdata, message):
		print("Reçu:{}".format(message.payload))
		if message.payload == b"fin d'of":
			print("publier fin d'of et off des leds")
			self.client.publish(topic="/stat/end/{}".format(self.NomIlot), payload=str(self.product_ident), qos=1, retain=False)
			self.client.publish(topic="/{}/off".format(self.NomIlot) , payload="1", qos=0, retain=False)
			self.product_ident = None
		else:
			print("publier liste des idents/leds")
			_id = Scan2Ident(message.payload)
			if _id != None:
				if _id == self.product_ident:
					print("ident en cours:{}".format(_id))
					self.client.publish(topic="/{}/blink".format(self.NomIlot) , payload="1", qos=0, retain=False)
				else:
					self.product_ident = _id
					print("nouvel ident:{}".format(_id))
					self.scan()

	def __init__(self,NomIlot="element"):
		Thread.__init__(self)
		self.NomIlot = NomIlot
		self.client = mqtt.Client()
		self.client.connect(broker_url, broker_port)
		self.client.on_message = self.on_message
		self.client.subscribe("scanner/#")
		
		self.state = "enCours"
		self.Etats={"enCours":{"Action":self.enCours,"EtatSuivant":"enCours"}}
		self.df_idents = pd.read_csv("idents.csv",encoding='utf-8')
		
		self.client.loop_start()

	def scan(self):
		_idents = list(self.df_idents["ident"][self.df_idents["ID objet"] == self.product_ident])
		print("idents ",_idents)
		self.client.publish(topic="/stat/start/{}/of/".format(self.NomIlot), payload="{}".format(self.product_ident), qos=0, retain=False)# fait par scanner

		for _id in _idents:
			print("A envoyer: {} a {}".format(_id,self.NomIlot),"/{}/{}".format(self.NomIlot,str(_id)))
			self.client.publish(topic="/{}/{}".format(self.NomIlot,_id) , payload=b"1", qos=0, retain=False)
		
	def enCours(self):
		pass #Attente d'un scan
		

	def run(self):
		while not self.fini:
			self.Etats[self.state]["Action"]()
			self.state = self.Etats[self.state]["EtatSuivant"]
			#self.client.loop() loop_start à la place ?
		self.client.loop_stop()
		
def testMachine():
	m=Machine()
	m.start()
	
def testIdents():
	print("idents_pour(566606)",idents_pour(566606))
	print("idents_pour(566602)",idents_pour(566602))
	print("idents_pour(563457)",idents_pour(563457))

def testFunction():
	receptionMessages()
	
if __name__ == "__main__":
	#testFunction()
	#testIdents()
	testMachine()
