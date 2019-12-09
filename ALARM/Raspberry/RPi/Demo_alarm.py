#!/usr/bin/python3

from threading import Thread
import paho.mqtt.client as mqtt
import pandas as pd
import os


broker_url = "localhost"
broker_port = 1883

fichiers={
"ilot1_560387":"casdemplois/export.cas emploi 560387 SX.XLSX"
,"ilot1_560740":"casdemplois/export.cas emploi 560740 SX.XLSX"
,"ilot1_560388":"casdemplois/export.cas emploi 560388 SX.XLSX"
,"ilot1_564739":"casdemplois/export.cas emploi 564739 SX.XLSX"
,"ilot1_564741":"casdemplois/export.cas emploi 564741 SX.XLSX"
}#,"ilot1_555555":"casdemplois/export.cas emploi 555555 SX.XLSX"}

cle = "Composante"
leds={"ilot1_560387":("ilot1","1"),"ilot1_560740":("ilot1","2")
	,"ilot1_560388":("ilot1","3"),"ilot1_564739":("ilot1","4")
,"ilot1_564741":("ilot1","5")}
def parse_casemploi():
	donnees = pd.DataFrame()
	for f in fichiers.keys():
		table = pd.read_excel(fichiers[f])
		table[cle] = table[cle].astype(str)
		table["ident"]=f
		donnees = donnees.append(table)
	return donnees

class Montage:
	pass

class Machine(Thread):
	fini = False
	ident = ""
	product_idents =[]

	def __init__(self):
		Thread.__init__(self)
		self.client = mqtt.Client()
		#self.client.on_connect = on_connect
		#self.client.on_message = on_message
		self.client.connect(broker_url, broker_port)
		self.donnees = parse_casemploi()
		print(self.donnees["Composante"])
		
   
	def get_id_from_of(self,of):
		id = "pas un id"
		if len(of) > 18 :
			id = str(of)[12:18]
		return id
		
	def getidents(self,of):
		self.product_idents = list(self.donnees["ident"][self.donnees[cle]==of])
		#print(self.donnees["ident"][self.donnees[cle]==of])
		#print("self.product_idents",self.product_idents)
		return self.product_idents
   
	def run(self):
		self.state = "scan"
		while not self.fini:
			if self.state=="scan":
				scan_of = input("scanner:")  
				self.ident = self.get_id_from_of(scan_of)
				print("ok : ",self.ident)
				self.client.publish(topic="off", payload="0", qos=1, retain=False)
				start_operation = False
				
				for id in self.getidents(self.ident):
					#print("publish : {}".format(id))
					if start_operation == False:
							self.client.publish(topic="/stats/start/", payload="1", qos=1, retain=False)
							start_operation = True
					print("publish:",leds[id][0],leds[id][1])
					self.client.publish(topic=str(leds[id][0]), payload=str(leds[id][1]), qos=1, retain=False)

			#	self.state == ""

			self.client.loop()

if __name__ == "__main__":
	m=Machine()
	m.start()
