#!/usr/bin/python3

import pandas as pd
import glob

def listeFichiers():
	liste = glob.glob("./casdemplois/*.csv")
	print(liste)
	return liste
	 	
def listeIdents():
	liste = listeFichiers()
	#print (liste)
	for f in liste:
		yield f[-10:-4]

def parse_casemploi():
	donnees = pd.DataFrame()
	for f in listeFichiers():
		table = pd.read_csv(f,encoding='utf-16',skiprows=7)
		table["ID objet"] = table["ID objet"].astype(str)
		table["ident"]=f[-10:-4]
		donnees = donnees.append(table)
	donnees = donnees[["ident","ID objet"]]
	return donnees
	
if __name__ == "__main__":
	table = pd.read_csv("configuration.csv",encoding='utf-8',sep=";")
	print(table["indent"])
	
	#print(parse_casemploi())

