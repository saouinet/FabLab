#!/usr/bin/python3

from threading import Thread
import paho.mqtt.client as mqtt
import pandas as pd
import os


broker_url = "localhost"
broker_port = 1883

class Machine(Thread):
	fini = False
	ident = ""
	product_idents =[]
	

	def __init__(self):
		Thread.__init__(self)
		self.client = mqtt.Client()
		self.client.connect(broker_url, broker_port)
		self.state = "test"
		self.Etats={"test":{"Action":self.tests,"EtatSuivant":"enAttente"},
		"enCours":{"Action":self.ofEnCours,"EtatSuivant":"enCours"},
		"fini":{"Action":self.ofFini,"EtatSuivant":"enAttente"},
		"enAttente":{"Action":self.enAttente,"EtatSuivant":"enAttente"}}	

	def enAttente(self):
		print(".",end=" ")
		
	def tests(self):
		print("Test")
	
	def ofEnCours(self):
		pass
		
	def ofFini(self):
		pass
		
	def run(self):
		self.state = "test"
		while not self.fini:
			self.Etats[self.state]["Action"]()
			self.state = self.Etats[self.state]["EtatSuivant"]
			self.client.loop()
			
if __name__ == "__main__":
	m=Machine()
	m.start()
